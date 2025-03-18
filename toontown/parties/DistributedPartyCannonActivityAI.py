from direct.directnotify import DirectNotifyGlobal

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.toonbase import TTLocalizer


class DistributedPartyCannonActivityAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyCannonActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        self.cloudColors = {}
        self.cloudsHit = {}
        self.cannonWillFire = (0, 0, 0)

    def setLanded(self, avId):
        if not avId:
            return

        senderId = self.air.getAvatarIdFromSender()
        if not senderId:
            return

        if senderId != avId:
            self.air.writeServerEvent('suspicious', senderId=senderId, issue='Toon tried to land someone else!')
            return

        if senderId not in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', senderId=senderId,
                                      issue='Toon tried to land while not playing the cannon activity!')
            return

        self.toonsPlaying.remove(senderId)
        reward = self.getTotalReward(self.cloudsHit[senderId] * PartyGlobals.CannonJellyBeanReward)
        if reward > PartyGlobals.CannonMaxTotalReward:
            reward = PartyGlobals.CannonMaxTotalReward

        av = self.air.doId2do.get(senderId)
        if not av:
            self.air.writeServerEvent('suspicious', senderId=senderId,
                                      issue='Toon tried to award beans while not in district!')
            return

        if reward > 0:
            self.sendUpdateToAvatarId(senderId, 'showJellybeanReward', [reward, av.getMoney(),
                                                                        TTLocalizer.PartyCannonResults % (
                                                                            reward, self.cloudsHit[senderId])])
            av.addMoney(reward)

        self.sendUpdate('setMovie', [PartyGlobals.CANNON_MOVIE_LANDED, senderId])
        del self.cloudsHit[senderId]

    def setCannonWillFire(self, cannonId, rot, angle):
        self.cannonWillFire = (cannonId, rot, angle)

    def d_setCannonWillFire(self, cannonId, rot, angle):
        self.sendUpdate('setCannonWillFire', [cannonId, rot, angle])

    def b_setCannonWillFire(self, cannonId, rot, angle):
        self.setCannonWillFire(cannonId, rot, angle)
        self.d_setCannonWillFire(cannonId, rot, angle)

    def getCannonWillFire(self):
        return self.cannonWillFire

    def cloudsColorRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.sendUpdateToAvatarId(avId, 'cloudsColorResponse', [list(self.cloudColors.values())])

    def requestCloudHit(self, cloudId, r, g, b):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to hit cloud in cannon activity they\'re not using!')
            return

        self.cloudColors[cloudId] = [cloudId, r, g, b]
        self.sendUpdate('setCloudHit', [cloudId, r, g, b])
        self.cloudsHit[avId] += 1

    def setToonTrajectoryAi(self, launchTime, x, y, z, h, p, r, velX, velY, velZ):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.sendUpdate('setToonTrajectory', [avId, launchTime, x, y, z, h, p, r, velX, velY, velZ])

    def updateToonTrajectoryStartVelAi(self, velX, velY, velZ):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.sendUpdate('updateToonTrajectoryStartVel', [avId, velX, velY, velZ])
