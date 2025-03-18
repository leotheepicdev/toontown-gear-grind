from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.parties import PartyGlobals

class DistributedPartyCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyCannonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.activityDoId = 0
        self.posHpr = [0, 0, 0, 0, 0, 0]
        self.avId = 0

    def delete(self):
        taskMgr.remove(self.uniqueName('remove-toon'))
        DistributedObjectAI.delete(self)

    def setActivityDoId(self, activityDoId):
        self.activityDoId = activityDoId

    def d_setActivityDoId(self, activityDoId):
        self.sendUpdate('setActivityDoId', [activityDoId])

    def b_setActivityDoId(self, activityDoId):
        self.setActivityDoId(activityDoId)
        self.d_setActivityDoId(activityDoId)

    def getActivityDoId(self):
        return self.activityDoId

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = [x, y, z, h, p, r]

    def d_setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [x, y, z, h, p, r])

    def b_setPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(x, y, z, h, p, r)
        self.d_setPosHpr(x, y, z, h, p, r)

    def getPosHpr(self):
        return self.posHpr

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if not self.avId:
            self.avId = avId
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_LOAD, self.avId)

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.avId == avId:
            self.sendUpdate('setCannonExit', [avId])
            self.avId = 0

    def d_setMovie(self, movie, avId):
        self.sendUpdate('setMovie', [movie, avId])

    def setCannonPosition(self, rot, angle):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId == self.avId:
            self.sendUpdate('updateCannonPosition', [avId, rot, angle])

    def setCannonLit(self, rot, angle):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId == self.avId:
            activity = self.air.doId2do.get(self.getActivityDoId())
            if not activity:
                return

            activity.toonsPlaying.append(avId)
            activity.cloudsHit[avId] = 0
            activity.b_setCannonWillFire(self.getDoId(), rot, angle)
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_CLEAR, avId)
            self.sendUpdate('setCannonExit', [avId])
            self.avId = 0

    def setFired(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to call unused setFired!')

    def setLanded(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if not senderId:
            return

        if avId != senderId:
            self.air.writeServerEvent('suspicious', senderId=senderId,
                                      issue='Toon claimed to be another toon in cannon!')
            return

        self.d_setMovie(PartyGlobals.CANNON_MOVIE_LANDED, senderId)

    def setTimeout(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to start timer for someone else!')
            return

        taskMgr.doMethodLater(PartyGlobals.CANNON_TIMEOUT, self.removeToon, self.uniqueName('remove-toon'),
                              extraArgs=[avId], appendTask=True)

    def removeToon(self, avId, task):
        if avId != self.avId:
            return task.done

        self.avId = 0
        self.d_setMovie(PartyGlobals.CANNON_MOVIE_FORCE_EXIT, avId)
        self.sendUpdate('setCannonExit', [avId])
        return task.done
