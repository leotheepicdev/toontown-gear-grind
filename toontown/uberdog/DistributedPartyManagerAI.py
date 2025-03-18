from panda3d.core import UniqueIdAllocator
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed.OtpDoGlobals import *

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyAI import DistributedPartyAI
from toontown.parties.InviteInfo import InviteInfoBase
from toontown.parties.PartyInfo import PartyInfoAI

import datetime, time

class Party:

    def __init__(self):
        self.partyId = 0
        self.partyInfo = None
        self.partyStruct = None
        self.inviteeIds = None
        self.zoneId = None
        self.party = None
        self.inviteKey = None
        self.hostName = ''

    def destroy(self):
        # TODO: we need a function to cleanup, deallocate party zone, and properly support canceling a party.
        pass

    def setPartyId(self, partyId):
        self.partyId = partyId

    def getPartyId(self):
        return self.partyId

    def setPartyInfo(self, partyInfo):
        self.partyInfo = partyInfo

    def getPartyInfo(self):
        return self.partyInfo

    def setInviteeIds(self, inviteeIds):
        self.inviteeIds = inviteeIds

    def getInviteeIds(self):
        return self.inviteeIds

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def getZoneId(self):
        return self.zoneId

    def setParty(self, party):
        self.party = party

    def getParty(self):
        return self.party

    def setInviteKey(self, inviteKey):
        self.inviteKey = inviteKey

    def getInviteKey(self):
        return self.inviteKey

class DistributedPartyManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedPartyManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        # TODO: similar to above comment, clean me up properly.
        self.host2Party = {}
        self.party2Host = {}
        self.shardAndZone2Party = {}

        self.publicParties = {}
        self.inviteKey2PartyId = {}
        self.avId2context = {}

        self.wantParties = config.GetBool('want-parties', False)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.sendUpdateToUD('partyManagerAIStartingUp', [self.doId, self.air.districtId])

    def disable(self):
        DistributedObjectAI.disable(self)
        self.sendUpdateToUD('partyManagerAIGoingDown', [self.doId, self.air.districtId])

    def addPartyRequest(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        senderId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(hostId)

        if not av:
            self.air.writeServerEvent('suspicious', avId=senderId,
                                      issue='Toon tried to create a party but does not exist on the server!')
            return
        if hostId != senderId:
            self.air.writeServerEvent('suspicious', avId=senderId,
                                      issue='Toon tried to create a party as someone else!')
            return

        startDate = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

        self.sendUpdateToUD('addParty', [hostId, self.doId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds, 0])

    def addPartyResponseUdToAi(self, hostId, errorCode, inviteKey):
        # TODO
        host = self.air.doId2do.get(hostId)
        if not host:
            return
        self.sendUpdateToAvatarId(hostId, 'addPartyResponse', [hostId, errorCode])

    def markInviteAsReadButNotReplied(self, todo0, todo1):
        pass

    def respondToInviteResponse(self, avId, inviteKey, partyId, response, todo4):
        if not avId:
            return

        context = self.avId2context.get(avId)
        if not context:
            return

    def changePrivateRequest(self, partyId, newPrivateStatus):
        hostId = self.air.getAvatarIdFromSender()
        self.changePrivateRequestAiToUd(hostId, partyId, newPrivateStatus)

    def changePrivateRequestAiToUd(self, hostId, partyId, newPrivateStatus):
        self.sendUpdateToUD('changePrivateRequestAiToUd', [hostId, partyId, newPrivateStatus])

    def changePrivateResponseUdToAi(self, hostId, partyId, newPrivateStatus, errorCode):
        self.changePrivateResponse(hostId, partyId, newPrivateStatus, errorCode)

    def changePrivateResponse(self, hostId, partyId, newPrivateStatus, errorCode):
        av = self.air.doId2do.get(hostId)
        if not av:
            return

        self.sendUpdateToAvatarId(hostId, 'changePrivateResponse', [partyId, newPrivateStatus, errorCode])

    def changePartyStatusRequest(self, partyId, newPartyStatus):
        hostId = self.air.getAvatarIdFromSender()
        self.changePartyStatusRequestAiToUd(hostId, partyId, newPartyStatus)

    def changePartyStatusRequestAiToUd(self, hostId, partyId, newPartyStatus):
        self.sendUpdateToUD('changePartyStatusRequestAiToUd', [hostId, partyId, newPartyStatus])

    def changePartyStatusResponseUdToAi(self, partyId, newPartyStatus, errorCode, beansRefunded):
        self.changePartyStatusResponse(partyId, newPartyStatus, errorCode, beansRefunded)

    def changePartyStatusResponse(self, partyId, newPartyStatus, errorCode, beansRefunded):
        hostId = self.party2host[partyId]

        av = self.air.doId2do.get(hostId)
        if not av:
            return

        av.addMoney(beansRefunded)
        self.sendUpdateToAvatarId(hostId, 'changePartyStatusResponse', [partyId, newPartyStatus, errorCode,
                                                                        beansRefunded])

    def partyInfoOfHostFailedResponseUdToAi(self, todo0):
        pass

    def partyInfoOfHostResponseUdToAi(self, partyStruct, inviteeIds):
        partyId = partyStruct[0]
        hostId = partyStruct[1]

        host = self.air.doId2do.get(hostId)

        if not host:
            return

        zoneId = self.air.allocateZone(owner=self)

        self.host2Party[hostId] = Party()
        self.host2Party[hostId].setZoneId(zoneId)
        self.host2Party[hostId].setInviteeIds(inviteeIds)

        # TEMP UNTIL WE SEND THE PARTY INFO VIA UD
        partyInfo = PartyInfoAI(partyId, hostId, partyStruct[2], partyStruct[3], partyStruct[4],
                                partyStruct[5], partyStruct[6], partyStruct[7], partyStruct[8], partyStruct[9],
                                partyStruct[10], partyStruct[11], partyStruct[12], partyStruct[13], partyStruct[14], partyStruct[15],
                                PartyGlobals.PartyStatus.Pending)

        party = DistributedPartyAI(self.air, hostId, zoneId, partyInfo)
        for activity in party.partyInfo.activityList:
            if activity.activityId == PartyGlobals.ActivityIds.PartyClock:
                party.setPartyClockInfo(activity.x, activity.y, activity.h)

        party.setInviteeIds(self.host2Party[hostId].getInviteeIds())
        party.setPartyState(False)
        party.setPartyInfoTuple(tuple(partyStruct))
        party.setPartyStartedTime(time.strftime('%Y-%m-%d %H:%M:%S'))
        party.setHostName(host.getName())
        party.generateWithRequiredAndId(partyId, self.air.districtId, zoneId)
        self.host2Party[hostId].setParty(party)

        self.partyHasStartedAiToUd(partyId, self.air.districtId, zoneId, hostId, host.getName())

        self.sendUpdateToAvatarId(hostId, 'receivePartyZone', [hostId, partyId, zoneId])

    def givePartyRefundResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def getPartyZone(self, avId, zoneId, planningParty):
        senderId = self.air.getAvatarIdFromSender()
        if planningParty:
            self.sendUpdateToAvatarId(senderId, 'receivePartyZone', [avId, 0, zoneId])
        else:
            self.sendUpdateToUD('partyInfoOfHostRequestAiToUd', [self.doId, avId], sender=self.air.getMsgSender())

    def freeZoneIdFromPlannedParty(self, todo0, todo1):
        pass

    def sendAvToPlayground(self, todo0, todo1):
        pass

    def exitParty(self, todo0):
        pass

    def removeGuest(self, todo0, todo1):
        pass

    def partyHasStartedAiToUd(self, partyId, shardId, zoneId, hostId, hostName):
        self.sendUpdateToUD('partyHasStartedAiToUd', [partyId, shardId, zoneId, hostId, hostName])

    def toonHasEnteredPartyAiToUd(self, avId, partyId, gateId):
        self.sendUpdateToUD('toonHasEnteredPartyAiToUd', [avId, partyId, gateId])

    def toonHasExitedPartyAiToUd(self, todo0):
        pass

    def partyHasFinishedUdToAllAi(self, partyId):
        # TODO: delete our party and send every av to the playground.
        hostId = self.party2Host[partyId]
        zoneId = self.host2Party[hostId].getZoneId()
        inviteKey = self.host2Party[hostId].getInviteKey()
        shardId = 0
        if partyId in self.party2Host:
            del self.party2host[partyId]
        if partyId in self.publicParties:
            shardId = self.publicParties['shardId']
            del self.publicParties[partyId]
        if (shardId, zoneId) in self.shardAndZone2Party:
            del self.shardAndZone2Party[(shardId, zoneId)]
        if hostId in self.host2Party:
            del self.host2Party[hostId]
        if inviteKey in self.inviteKey2PartyId:
            del self.inviteKey2PartyId

    def updateToPublicPartyInfoUdToAllAi(self, hostId, partyId, shardId, zoneId, numberOfGuests, isPrivate, hostName,
                                         activityIds, minLeft):
        self.publicParties[partyId] = {
            'shardId': shardId,
            'zoneId': zoneId,
            'hostId': hostId,
            'numberOfGuests': numberOfGuests,
            'hostName': hostName,
            'activityIds': activityIds,
            'minLeft': minLeft,
            'started': datetime.datetime.now(),
            'isPrivate': isPrivate}
        self.shardAndZone2Party[(shardId, zoneId)] = partyId

    def updateToPublicPartyCountUdToAllAi(self, todo0, todo1):
        pass

    def requestShardIdZoneIdForHostId(self, hostId):
        self.sendUpdateToUD('requestShardIdZoneIdForHostId', [hostId])

    def sendShardIdZoneIdToAvatar(self, shardId, zoneId):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'sendShardIdZoneIdToAvatar', [shardId, zoneId])

    def partyManagerUdStartingUp(self):
        pass

    def forceCheckStart(self):
        pass

    def requestMw(self, todo0, todo1, todo2, todo3):
        pass

    def mwResponseUdToAllAi(self, todo0, todo1, todo2, todo3):
        pass

    def canBuyParties(self):
        return self.wantParties

    def getPublicParties(self):
        publicPartiesList = []
        for partyId in self.publicParties:
            party = self.publicParties[partyId]
            if party['isPrivate']:
                continue
            minLeft = int((PartyGlobals.PARTY_DURATION - (datetime.datetime.now() - party['started']).seconds) / 60)
            if minLeft <= 0:
                #self.closeParty(partyId)
                continue
            guests = max(0, min(party.get('numGuests', 0), 255))
            publicPartiesList.append([party['shardId'], party['zoneId'], guests, party.get('hostName', ''),
                                      party.get('activityIds', []), minLeft])

        return publicPartiesList

    def getPartyIdFromInviteKey(self, inviteKey):
        if inviteKey in self.inviteKey2PartyId[inviteKey]:
            return self.inviteKey2PartyId[inviteKey]
        return None

    def d_respondToInvite(self, avId, response, context, inviteKey):
        partyId = self.getPartyIdFromInviteKey(inviteKey)
        if not partyId:
            return

        if avId in list(self.avId2context.keys()):
            return

        self.avId2context[avId] = context

        self.sendUpdateToUD('respondToInvite', [self.doId, avId, inviteKey, partyId, response])

    def sendUpdateToUD(self, field, args = [], sender=None):
        if not sender:
            sender = self.doId
        dg = self.dclass.aiFormatUpdate(field, OTP_DO_ID_TOONTOWN_PARTY_MANAGER, OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                        sender, args)
        self.air.send(dg)
