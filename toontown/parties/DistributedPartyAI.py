from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.parties import PartyGlobals
from toontown.parties import PartyUtils
from toontown.parties.DistributedPartyCannonAI import DistributedPartyCannonAI
from toontown.parties.DistributedPartyCannonActivityAI import DistributedPartyCannonActivityAI
from toontown.parties.DistributedPartyCatchActivityAI import DistributedPartyCatchActivityAI
from toontown.parties.DistributedPartyCogActivityAI import DistributedPartyCogActivityAI
from toontown.parties.DistributedPartyDance20ActivityAI import DistributedPartyDance20ActivityAI
from toontown.parties.DistributedPartyDanceActivityAI import DistributedPartyDanceActivityAI
from toontown.parties.DistributedPartyFireworksActivityAI import DistributedPartyFireworksActivityAI
from toontown.parties.DistributedPartyJukebox40ActivityAI import DistributedPartyJukebox40ActivityAI
from toontown.parties.DistributedPartyJukeboxActivityAI import DistributedPartyJukeboxActivityAI
from toontown.parties.DistributedPartyTrampolineActivityAI import DistributedPartyTrampolineActivityAI
from toontown.parties.DistributedPartyTugOfWarActivityAI import DistributedPartyTugOfWarActivityAI
from toontown.parties.DistributedPartyValentineDance20ActivityAI import DistributedPartyValentineDance20ActivityAI
from toontown.parties.DistributedPartyValentineDanceActivityAI import DistributedPartyValentineDanceActivityAI
from toontown.parties.DistributedPartyValentineJukebox40ActivityAI import DistributedPartyValentineJukebox40ActivityAI
from toontown.parties.DistributedPartyValentineJukeboxActivityAI import DistributedPartyValentineJukeboxActivityAI
from toontown.parties.DistributedPartyValentineTrampolineActivityAI import DistributedPartyValentineTrampolineActivityAI
from toontown.parties.DistributedPartyWinterCatchActivityAI import DistributedPartyWinterCatchActivityAI
from toontown.parties.DistributedPartyWinterCogActivityAI import DistributedPartyWinterCogActivityAI
from toontown.parties.DistributedPartyWinterTrampolineActivityAI import DistributedPartyWinterTrampolineActivityAI
from toontown.parties.DistributedPartyVictoryTrampolineActivityAI import DistributedPartyVictoryTrampolineActivityAI

class DistributedPartyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyAI')

    def __init__(self, air, hostId, zoneId, partyInfo):
        DistributedObjectAI.__init__(self, air)
        self.hostId = hostId
        self.zoneId = zoneId
        self.partyInfo = partyInfo
        self.partyClockInfo = (0, 0, 0)
        self.inviteeIds = []
        self.partyState = False
        self.partyInfoTuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], [], 0)
        self.avIdsAtParty = []
        self.partyStartedTime = ''
        self.hostName = ''
        self.activities = set()
        self.cannonActivity = None

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        activityId2class = {
            PartyGlobals.ActivityIds.PartyCog: DistributedPartyCogActivityAI,
            PartyGlobals.ActivityIds.PartyWinterCog: DistributedPartyWinterCogActivityAI,
            PartyGlobals.ActivityIds.PartyJukebox: DistributedPartyJukeboxActivityAI,
            PartyGlobals.ActivityIds.PartyValentineJukebox: DistributedPartyValentineJukeboxActivityAI,
            PartyGlobals.ActivityIds.PartyJukebox40: DistributedPartyJukebox40ActivityAI,
            PartyGlobals.ActivityIds.PartyValentineJukebox40: DistributedPartyValentineJukebox40ActivityAI,
            PartyGlobals.ActivityIds.PartyTrampoline: DistributedPartyTrampolineActivityAI,
            PartyGlobals.ActivityIds.PartyValentineTrampoline: DistributedPartyValentineTrampolineActivityAI,
            PartyGlobals.ActivityIds.PartyVictoryTrampoline: DistributedPartyVictoryTrampolineActivityAI,
            PartyGlobals.ActivityIds.PartyWinterTrampoline: DistributedPartyWinterTrampolineActivityAI,
            PartyGlobals.ActivityIds.PartyCatch: DistributedPartyCatchActivityAI,
            PartyGlobals.ActivityIds.PartyWinterCatch: DistributedPartyWinterCatchActivityAI,
            PartyGlobals.ActivityIds.PartyDance: DistributedPartyDanceActivityAI,
            PartyGlobals.ActivityIds.PartyValentineDance: DistributedPartyValentineDanceActivityAI,
            PartyGlobals.ActivityIds.PartyDance20: DistributedPartyDance20ActivityAI,
            PartyGlobals.ActivityIds.PartyValentineDance20: DistributedPartyValentineDance20ActivityAI,
            PartyGlobals.ActivityIds.PartyTugOfWar: DistributedPartyTugOfWarActivityAI,
            PartyGlobals.ActivityIds.PartyFireworks: DistributedPartyFireworksActivityAI
        }

        for activity in self.partyInfo.activityList:
            activityId = activity.activityId
            if activityId in activityId2class:
                activityObj = activityId2class[activityId](self.air, self.getDoId(), activity)
                activityObj.generateWithRequired(self.zoneId)
                self.activities.add(activityObj)
            elif activityId == PartyGlobals.ActivityIds.PartyCannon:
                if not self.cannonActivity:
                    self.cannonActivity = DistributedPartyCannonActivityAI(self.air, self.getDoId(), activity)
                    self.cannonActivity.generateWithRequired(self.zoneId)

                activityObj = DistributedPartyCannonAI(self.air)
                activityObj.setActivityDoId(self.cannonActivity.getDoId())
                x = PartyUtils.convertDistanceFromPartyGrid(activity.x, 0)
                y = PartyUtils.convertDistanceFromPartyGrid(activity.y, 1)
                h = activity.h * PartyGlobals.PartyGridHeadingConverter
                activityObj.setPosHpr(x, y, 0, h, 0, 0)
                activityObj.generateWithRequired(self.zoneId)
                self.activities.add(activityObj)

    def delete(self):
        for activity in self.activities:
            activity.requestDelete()

        self.activities.clear()
        if self.cannonActivity:
            self.cannonActivity.requestDelete()
            self.cannonActivity = None

        self.ignoreAll()
        DistributedObjectAI.delete(self)

    def setPartyClockInfo(self, x, y, h):
        self.partyClockInfo = (x, y, h)

    def d_setPartyClockInfo(self, x, y, h):
        self.sendUpdate('setPartyClockInfo', [x, y, h])

    def b_setPartyClockInfo(self, x, y, h):
        self.setPartyClockInfo(x, y, h)
        self.d_setPartyClockInfo(x, y, h)

    def getPartyClockInfo(self):
        return self.partyClockInfo

    def setInviteeIds(self, inviteeIds):
        self.inviteeIds = inviteeIds

    def d_setInviteeIds(self, inviteeIds):
        self.sendUpdate('setInviteeIds', [inviteeIds])

    def b_setInviteeIds(self, inviteeIds):
        self.setInviteeIds(inviteeIds)
        self.d_setInviteeIds(inviteeIds)

    def getInviteeIds(self):
        return self.inviteeIds

    def setPartyState(self, partyState):
        self.partyState = partyState

    def d_setPartyState(self, partyState):
        self.sendUpdate('setPartyState', [partyState])

    def b_setPartyState(self, partyState):
        self.setPartyState(partyState)
        self.d_setPartyState(partyState)

    def getPartyState(self):
        return self.partyState

    def setPartyInfoTuple(self, partyInfoTuple):
        self.partyInfoTuple = partyInfoTuple

    def d_setPartyInfoTuple(self, partyInfoTuple):
        self.sendUpdate('setPartyInfoTuple', [partyInfoTuple])

    def b_setPartyInfoTuple(self, partyInfoTuple):
        self.setPartyInfoTuple(partyInfoTuple)
        self.d_setPartyInfoTuple(partyInfoTuple)

    def getPartyInfoTuple(self):
        return self.partyInfoTuple

    def setAvIdsAtParty(self, avIdsAtParty):
        self.avIdsAtParty = avIdsAtParty

    def d_setAvIdsAtParty(self, avIdsAtParty):
        self.sendUpdate('setAvIdsAtParty', [avIdsAtParty])

    def b_setAvIdsAtParty(self, avIdsAtParty):
        self.setAvIdsAtParty(avIdsAtParty)
        self.d_setAvIdsAtParty(avIdsAtParty)

    def getAvIdsAtParty(self):
        return self.avIdsAtParty

    def setPartyStartedTime(self, partyStartedTime):
        self.partyStartedTime = partyStartedTime

    def d_setPartyStartedTime(self, partyStartedTime):
        self.sendUpdate('setPartyStartedTime', [partyStartedTime])

    def b_setPartyStartedTime(self, partyStartedTime):
        self.setPartyStartedTime(partyStartedTime)
        self.d_setPartyStartedTime(partyStartedTime)

    def getPartyStartedTime(self):
        return self.partyStartedTime

    def setHostName(self, hostName):
        self.hostName = hostName

    def d_setHostName(self, hostName):
        self.sendUpdate('setHostName', [hostName])

    def b_setHostName(self, hostName):
        self.setHostName(hostName)
        self.d_setHostName(hostName)

    def getHostName(self):
        return self.hostName

    def avIdEnteredParty(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        if avId in self.avIdsAtParty:
            return

        self.avIdsAtParty.append(avId)
        self.b_setAvIdsAtParty(self.avIdsAtParty)
        self.acceptOnce(av.getZoneChangeEvent(), self.avIdExitedParty, extraArgs=[avId])
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])

    def avIdExitedParty(self, avId, zoneId, oldZoneId):
        # We don't actually care about zoneId or oldZoneId, we only care about avId.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        if avId not in self.avIdsAtParty:
            return

        self.avIdsAtParty.remove(avId)
        self.b_setAvIdsAtParty(self.avIdsAtParty)
        self.ignore(av.getZoneChangeEvent())
        self.ignore(self.air.getAvatarExitEvent(avId))

    def __handleUnexpectedExit(self, avId):
        if avId not in self.avIdsAtParty:
            return

        self.avIdsAtParty.remove(avId)
        self.b_setAvIdsAtParty(self.avIdsAtParty)
        self.ignore('DOChangeZone-%s' % avId)
        self.ignore(self.air.getAvatarExitEvent(avId))
