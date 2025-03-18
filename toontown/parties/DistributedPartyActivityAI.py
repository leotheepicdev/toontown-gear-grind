from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.parties import PartyGlobals
from toontown.parties import PartyUtils
from toontown.toonbase import ToontownGlobals


class DistributedPartyActivityAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyActivityAI')

    def __init__(self, air, parent, activity):
        DistributedObjectAI.__init__(self, air)
        self.parent = parent
        self.x = PartyUtils.convertDistanceFromPartyGrid(activity.x, 0)
        self.y = PartyUtils.convertDistanceFromPartyGrid(activity.y, 1)
        self.h = activity.h * PartyGlobals.PartyGridHeadingConverter
        self.partyDoId = self.parent
        self.toonsPlaying = []

    def setX(self, x):
        self.x = x

    def d_setX(self, x):
        self.sendUpdate('setX', [x])

    def b_setX(self, x):
        self.setX(x)
        self.d_setX(x)

    def getX(self):
        return self.x

    def setY(self, y):
        self.y = y

    def d_setY(self, y):
        self.sendUpdate('setY', [y])

    def b_setY(self, y):
        self.setY(y)
        self.d_setY(y)

    def getY(self):
        return self.y

    def setH(self, h):
        self.h = h

    def d_setH(self, h):
        self.sendUpdate('setH', [h])

    def b_setH(self, h):
        self.setH(h)
        self.d_setH(h)

    def getH(self):
        return self.h

    def setPartyDoId(self, partyDoId):
        self.partyDoId = partyDoId

    def d_setPartyDoId(self, partyDoId):
        self.sendUpdate('setPartyDoId', [partyDoId])

    def b_setPartyDoId(self, partyDoId):
        self.setPartyDoId(partyDoId)
        self.d_setPartyDoId(partyDoId)

    def getPartyDoId(self):
        return self.partyDoId

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to enter activity from another shard!')
            return

        if avId in self.toonsPlaying:
            return

        self.toonsPlaying.append(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to exit activity from another shard!')
            return

        if avId not in self.toonsPlaying:
            return

        self.toonsPlaying.remove(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to exit activity from another shard!')
            return

        if avId not in self.toonsPlaying:
            return

        self.toonsPlaying.remove(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def setToonsPlaying(self, toonsPlaying):
        self.toonsPlaying = toonsPlaying

    def d_setToonsPlaying(self, toonsPlaying):
        self.sendUpdate('setToonsPlaying', [toonsPlaying])

    def b_setToonsPlaying(self, toonsPlaying):
        self.setToonsPlaying(toonsPlaying)
        self.d_setToonsPlaying(toonsPlaying)

    def getToonsPlaying(self):
        return self.toonsPlaying

    def getTotalReward(self, reward):
        totalReward = reward
        if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY) or self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH):
            totalReward *= 2

        return totalReward
