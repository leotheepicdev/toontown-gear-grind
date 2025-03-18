from panda3d.core import UniqueIdAllocator

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfoAI

import datetime

# TODO: CLEANUP PROPERLY AND HANDLE PARTY STOPPING AND GOING DOWN

class Party:

    def __init__(self):
        self.zoneId = 0
        self.shardId = 0
        self.partyMgr = 0
        self.partyInfo = None
        self.partyStruct = None
        self.inviteeIds = None
        self.inviteKey = 0

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def getZoneId(self):
        return self.zoneId

    def setShardId(self, shardId):
        self.shardId = shardId

    def getShardId(self):
        return self.shardId

    def setPartyInfo(self, partyInfo):
        self.partyInfo = partyInfo

    def getPartyInfo(self):
        return self.partyInfo

    def setPartyStruct(self, partyStruct):
        self.partyStruct = partyStruct

    def getPartyStruct(self):
        return self.partyStruct

    def setInviteeIds(self, inviteeIds):
        self.inviteeIds = inviteeIds

    def getInviteeIds(self):
        return self.inviteeIds

    def setInviteKey(self, inviteKey):
        self.inviteKey = inviteKey

    def getInviteKey(self):
        return self.inviteKey

class DistributedPartyManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedPartyManagerUD')
    START_PARTY_TASK_NAME = 'startPartyTask-%s'

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.partyAllocator = UniqueIdAllocator(10000000, 30000000)

        self.host2Party = {}
        self.publicParties = {}
        self.shard2PartyMgr = {}

        self.wantInstantParties = config.GetBool('want-instant-parties', True)

        # TODO: handle parties when they are finished.
        # TODO: when a party is done, deallocate me so we don't uh cause any server problems.
        # also, create a case for when we are out of invite keys
        self.inviteKeyAllocator = UniqueIdAllocator(1, 65535)
        self.partyTasks = [] # TODO: am i needed?

        # TODO: upon starting a party, check if its too late.

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

    def delete(self):
        for task in self.partyTasks:
            taskMgr.remove(task)

        DistributedObjectGlobalUD.delete(self)

    def startPartyTask(self, partyInfo):
        if self.wantInstantParties:
            seconds = 0.1
        else:
            seconds = (datetime.datetime.now(tz=self.air.toontownTimeManager.serverTimeZone) - partyInfo.startTime).total_seconds()
        taskMgr.doMethodLater(seconds, self.partyIsReady, self.START_PARTY_TASK_NAME % partyInfo.partyId, extraArgs=[partyInfo.hostId])

    def partyIsReady(self, hostId, task=None):
        partyInfo = self.host2Party[hostId].getPartyInfo()
        if partyInfo.status == PartyGlobals.PartyStatus.Pending:
            partyInfo.status = PartyGlobals.PartyStatus.CanStart
            partyStruct = self.host2Party[hostId].getPartyStruct()
            self.sendUpdateToAV(hostId, 'setHostedParties', [[partyStruct]])
            self.sendUpdateToAV(hostId, 'setPartyCanStart', [partyInfo.partyId])
        if task:
            return task.done

    def isTooLate(self, partyInfo):
        now = datetime.datetime.now(tz=self.air.toontownTimeManager.serverTimeZone)
        delta = datetime.timedelta(minutes=15)
        endStartable = partyInfo.startTime + delta
        return endStartable > now

    def addParty(self, hostId, removeMePlease, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds, todo0):
        partyDoId = self.air.getMsgSender()
        if hostId in self.host2Party:
            self.sendUpdateToAI(partyDoId, 'addPartyResponseUdToAi', [hostId, PartyGlobals.AddPartyErrorCode.TooManyHostedParties, self.host2Party[hostId].getInviteKey()])
            return
        partyTimeFormat = '%Y-%m-%d %H:%M:%S'
        startDate = datetime.datetime.strptime(startTime, partyTimeFormat)
        endDate = datetime.datetime.strptime(endTime, partyTimeFormat)

        partyId = self.partyAllocator.allocate()

        self.host2Party[hostId] = Party()
        self.host2Party[hostId].setInviteKey(self.inviteKeyAllocator.allocate())

        partyInfo = PartyInfoAI(partyId, hostId, startDate.year, startDate.month, startDate.day,
                                startDate.hour, startDate.minute, endDate.year, endDate.month, endDate.day,
                                endDate.hour, endDate.minute, isPrivate, inviteTheme, activities, decorations,
                                PartyGlobals.PartyStatus.Pending)

        partyStruct = [
            partyId,
            hostId,
            startDate.year,
            startDate.month,
            startDate.day,
            startDate.hour,
            startDate.minute,
            endDate.year,
            endDate.month,
            endDate.day,
            endDate.hour,
            endDate.minute,
            isPrivate,
            inviteTheme,
            activities,
            decorations,
            PartyGlobals.PartyStatus.Pending
        ]

        self.host2Party[hostId].setPartyInfo(partyInfo)
        self.host2Party[hostId].setPartyStruct(partyStruct)
        self.host2Party[hostId].setInviteeIds(inviteeIds)

        self.sendUpdateToAI(partyDoId, 'addPartyResponseUdToAi',
                            [hostId, PartyGlobals.AddPartyErrorCode.AllOk,
                             self.host2Party[hostId].getInviteKey()])
        self.startPartyTask(partyInfo)

    def markInviteAsReadButNotReplied(self, todo0, todo1):
        pass

    def respondToInvite(self, partyDoId, avId, inviteKey, partyId, response):
        inviteeIds = []
        for partyIndices in list(self.host2Party.values()):
            if partyIndices[0] == partyId:
                inviteeIds = partyIndices[3]
                break

        if not inviteeIds:
            return

        if avId not in inviteeIds:
            return

        self.sendUpdateToAI(partyDoId, 'respondToInviteResponse',
                            [avId, inviteKey, partyId, response, 0])

    def changePrivateRequest(self, todo0, todo1):
        pass

    def changePrivateRequestAiToUd(self, hostId, partyId, newPrivateStatus):
        party = self.host2Party.get(hostId)
        partyStruct = party.getPartyStruct()

        if party is None:
            self.changePrivateResponseUdToAi(hostId, partyId, newPrivateStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.ValidationError)
            return
        if partyStruct[1] != hostId:
            self.changePrivateResponseUdToAi(hostId, partyId, newPrivateStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.ValidationError)
            return
        if partyStruct[16] not in (PartyGlobals.PartyStatus.CanStart, PartyGlobals.PartyStatus.Pending):
            self.changePrivateResponseUdToAi(hostId, partyId, newPrivateStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.AlreadyStarted)
            return

        partyStruct[12] = newPrivateStatus
        self.host2Party[hostId] = party

        if partyId in list(self.publicParties.keys()):
            publicPartyInfo = self.publicParties[partyId]
            minLeft = int((PartyGlobals.PARTY_DURATION - (datetime.datetime.now() - publicPartyInfo['started']).seconds) / 60)
            self.updateToPublicPartyInfoUdToAllAi(publicPartyInfo['shardId'], publicPartyInfo['zoneId'], partyId,
                                                  hostId, publicPartyInfo['numberOfGuests'],
                                                  publicPartyInfo['hostName'], partyStruct[14], minLeft,
                                                  partyStruct[12])

        self.sendUpdateToAV(hostId, 'setHostedParties', [[partyStruct]])
        self.changePrivateResponseUdToAi(hostId, partyId, newPrivateStatus,
                                         PartyGlobals.ChangePartyFieldErrorCode.AllOk)

    def changePrivateResponseUdToAi(self, hostId, partyId, newPrivateStatus, errorCode):
        partyDoId = self.air.getMsgSender()
        self.sendUpdateToAI(partyDoId, 'changePrivateResponseUdToAi', [hostId, partyId, newPrivateStatus, errorCode])

    def changePrivateResponse(self, todo0, todo1, todo2):
        pass

    def changePartyStatusRequest(self, todo0, todo1):
        pass

    def changePartyStatusRequestAiToUd(self, hostId, partyId, newPartyStatus):
        # TODO
        return
        party = self.host2Party.get(hostId)
        partyStruct = party.getPartyStruct()

        if party is None:
            self.changePrivateResponseUdToAi(hostId, partyId, newPartyStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.ValidationError)
            return
        if partyStruct[1] != hostId:
            self.changePrivateResponseUdToAi(hostId, partyId, newPartyStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.ValidationError)
            return
        if partyStruct[16] not in (PartyGlobals.PartyStatus.CanStart, PartyGlobals.PartyStatus.Pending):
            self.changePrivateResponseUdToAi(hostId, partyId, newPartyStatus,
                                             PartyGlobals.ChangePartyFieldErrorCode.AlreadyStarted)
            return

        partyStruct[16] = newPartyStatus
        self.sendUpdateToAV(hostId, 'setHostedParties', [[partyStruct]])

        beansRefunded = 0
        if newPartyStatus == PartyGlobals.PartyStatus.Cancelled:
            beansRefunded = PartyGlobals.getCostOfParty(party.getPartyInfo()) * PartyGlobals.PartyRefundPercentage
            if hostId in self.host2Party:
                inviteKey = self.host2Party[hostId].getInviteKey()
                self.inviteKeyAllocator.free(inviteKey)
                del self.host2Party[hostId]
            if taskMgr.hasTaskNamed(self.START_PARTY_TASK_NAME % partyId):
                taskMgr.remove(self.START_PARTY_TASK_NAME % partyId)
        else:
            self.host2Party[hostId] = party
            self.updateToPublicPartyInfoUdToAllAi(0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.changePartyStatusResponseUdToAi(partyId, newPartyStatus, PartyGlobals.ChangePartyFieldErrorCode.AllOk,
                                             beansRefunded)
        if newPartyStatus == PartyGlobals.PartyStatus.Cancelled:
            self.partyHasFinishedUdToAllAi(partyId)

    def changePartyStatusResponseUdToAi(self, partyId, newPartyStatus, errorCode, beansRefunded):
        partyDoId = self.air.getMsgSender()
        self.sendUpdateToAI(partyDoId, 'changePartyStatusResponseUdToAi', [partyId, newPartyStatus, errorCode, beansRefunded])

    def changePartyStatusResponse(self, todo0, todo1, todo2, todo3):
        pass

    def partyInfoOfHostRequestAiToUd(self, partyMgrDoId, hostId):
        senderId = self.air.getAvatarIdFromSender()
        if hostId in self.host2Party:
            partyInfo = self.host2Party[hostId].getPartyInfo()
            if partyInfo.status == PartyGlobals.PartyStatus.CanStart:
                partyStruct = self.host2Party[hostId].getPartyStruct()
                inviteeIds = self.host2Party[hostId].getInviteeIds()
                self.sendUpdateToAI(partyMgrDoId, 'partyInfoOfHostResponseUdToAi', [partyStruct, inviteeIds])
                return
            partyId = self.host2Party[hostId].getPartyInfo().partyId
            zoneId = self.host2Party[hostId].getZoneId()
        else:
            partyId = 0
            zoneId = 0
        self.sendUpdateToAvatarId(senderId, 'receivePartyZone', [hostId, partyId, zoneId], doId=partyMgrDoId)

    def partyInfoOfHostFailedResponseUdToAi(self, todo0):
        pass

    def givePartyRefundResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def freeZoneIdFromPlannedParty(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitParty(self, todo0):
        pass

    def removeGuest(self, todo0, todo1):
        pass

    def partyManagerAIStartingUp(self, partyMgrDoId, shardId):
        self.shard2PartyMgr[shardId] = partyMgrDoId

    def partyManagerAIGoingDown(self, partyMgrDoId, shardId):
        del self.shard2PartyMgr[shardId]

    def partyHasStartedAiToUd(self, partyId, shardId, zoneId, hostId, hostName):
        self.publicParties[partyId] = {
            'shardId': shardId,
            'zoneId': zoneId,
            'hostId': hostId,
            'numberOfGuests': 1,
            'hostName': hostName,
            'started': datetime.datetime.now()}

        party = self.host2Party.get(hostId)
        party.setZoneId(zoneId)
        party.getPartyInfo().status = PartyGlobals.PartyStatus.Started
        partyStruct = party.getPartyStruct()
        self.sendUpdateToAV(hostId, 'setHostedParties', [[partyStruct]])
        minLeft = int((PartyGlobals.PARTY_DURATION - (datetime.datetime.now() - self.publicParties[partyId]['started']).seconds) / 60)
        self.updateToPublicPartyInfoUdToAllAi(shardId, zoneId, partyId, hostId, 0, hostName, partyStruct[14], minLeft,
                                              partyStruct[12])

    def toonHasEnteredPartyAiToUd(self, avId, partyId, gateId):
        if partyId not in self.publicParties:
            return
        party = self.publicParties[partyId]
        if avId != party['hostId'] and party['numberOfGuests'] >= PartyGlobals.MaxToonsAtAParty:
            return
        party['numberOfGuests'] += 1
        shardId = party['shardId']
        zoneId = party['zoneId']
        hostId = party['hostId']
        hostName = party['hostName']
        minLeft = int((PartyGlobals.PARTY_DURATION - (datetime.datetime.now() - party['started']).seconds) / 60)
        partyStruct = self.host2Party.get(hostId).getPartyStruct()
        self.updateToPublicPartyInfoUdToAllAi(shardId, zoneId, partyId, hostId, 0, hostName, partyStruct[14], minLeft,
                                              partyStruct[12])

        actIds = []
        for activity in partyStruct[14]:
            actIds.append(activity[0])

        recipient = self.GetPuppetConnectionChannel(avId)
        sender = simbase.air.getAvatarIdFromSender()
        dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('setParty').aiFormatUpdate(gateId, recipient, sender, [hostId, shardId, zoneId])
        self.air.send(dg)

    def toonHasExitedPartyAiToUd(self, todo0):
        pass

    def partyHasFinishedUdToAllAi(self, partyId):
        self.sendUpdateToAllAI('partyHasFinishedUdToAllAi', [partyId])

    def updateToPublicPartyInfoUdToAllAi(self, shardId, zoneId, partyId, hostId, numberOfGuests, hostName, activityIds,
                                         minLeft, isPrivate):
        actIds = []
        for activity in activityIds:
            actIds.append(activity[0])
        self.sendUpdateToAllAI('updateToPublicPartyInfoUdToAllAi', [hostId, partyId, shardId, zoneId, numberOfGuests,
                                                                    isPrivate, hostName, actIds, minLeft])
    def updateToPublicPartyCountUdToAllAi(self, todo0, todo1):
        pass

    def requestShardIdZoneIdForHostId(self, hostId):
        avId = self.air.getAvatarIdFromSender()
        partyId = self.host2Party[hostId].getPartyInfo().partyId
        shardId = self.host2Party[hostId].getShardId()
        zoneId = self.host2Party[hostId].getZoneId()
        self.sendShardIdZoneIdToAvatar(shardId, zoneId)

    def sendShardIdZoneIdToAvatar(self, shardId, zoneId):
        avId = self.air.getAvatarIdFromSender()
        partyMgrDoId = self.air.getAccountIdFromSender()
        self.sendUpdateToAvatarId(avId, 'sendShardIdZoneIdToAvatar', [shardId, zoneId], doId=partyMgrDoId)

    def partyManagerUdStartingUp(self):
        pass

    def updateAllPartyInfoToUd(self, hostId, partyId, zoneId, isPrivate, inviteTheme, status, hostName, activityIds, shardId): # TODO
        if hostId not in self.host2Party:
            self.host2Party[hostId] = Party()
            self.host2Party[hostId].setPartyId(partyId)
            self.host2Party[hostId].setShardId(shardId)

    def forceCheckStart(self):
        pass

    def requestMw(self, todo0, todo1, todo2, todo3):
        pass

    def mwResponseUdToAllAi(self, todo0, todo1, todo2, todo3):
        pass

    def sendUpdateToAV(self, avId, field, args = []):
        dg = self.air.dclassesByName['DistributedToonUD'].getFieldByName(field).aiFormatUpdate(avId, avId, simbase.air.ourChannel,args)
        self.air.send(dg)

    def sendUpdateToAvatarId(self, avId, field, args=[], doId=None):
        if not doId:
            doId = self.doId
        channel = self.GetPuppetConnectionChannel(avId)
        dg = self.dclass.aiFormatUpdate(field, doId, channel, self.air.ourChannel, args)
        self.air.send(dg)

    def sendUpdateToAI(self, doId, field, args = []):
        dg = self.dclass.aiFormatUpdate(field, doId, doId, self.doId, args)
        self.air.send(dg)

    def sendUpdateToAllAI(self, field, args = []):
        for partyMgrDoId in self.shard2PartyMgr.values():
            self.sendUpdateToAI(partyMgrDoId, field, args)
