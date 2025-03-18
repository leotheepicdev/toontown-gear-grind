from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta

from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI

from toontown.estate import HouseGlobals

class DistributedFireworksCannonAI(DistributedFireworkShowAI):
    notify = directNotify.newCategory('DistributedFireworksCannonAI')

    def __init__(self, air):
        DistributedFireworkShowAI.__init__(self, air)

        self.pos = (22.334, -70.012, 0.786)
    
    def announceGenerate(self):
        DistributedFireworkShowAI.announceGenerate(self)

        self.d_setPosition(*self.pos)

    def __verifyAvatarInMyZone(self, av):
        return av.getLocation() == self.getLocation()

    def getPosition(self):
        return self.pos

    def setPosition(self, x, y, z):
        self.pos = (x, y, z)

    def b_setPosition(self, x, y, z):
        self.setPosition(x, y, z)
        self.d_setPosition(x, y, z)

    def d_setPosition(self, x, y, z):
        self.sendUpdate('setPosition', [x, y, z])

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Not in same shard as Fireworks Cannon!')
            return

        if not self.__verifyAvatarInMyZone(av):
            self.air.writeServerEvent('suspicious', avId, 'Not in same zone as Fireworks Cannon!')
            return

        self.d_setMovie(HouseGlobals.FIREWORKS_MOVIE_GUI, avId, globalClockDelta.getRealNetworkTime(bits = 16))

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()

        if not avId:
            return

        self.d_freeAvatar(avId)
        self.resetMovie(avId)

    def resetMovie(self, avId):
        taskMgr.doMethodLater(2, self.d_setMovie, 'resetMovie-{0}'.format(self.doId), extraArgs = [HouseGlobals.FIREWORKS_MOVIE_CLEAR, avId, 0])

    def d_freeAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])

    def d_setMovie(self, mode, avId, time):
        self.sendUpdate('setMovie', [mode, avId, time])
