from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from .DistributedNPCToonBaseAI import *

class DistributedNPCCheesyCleanerAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        self.timedOut = 0

    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        DistributedNPCToonBaseAI.avatarEnter(self)
        av = self.air.doId2do.get(avId)
        if av is None:
            self.notify.warning('toon isnt there! toon: %s' % avId)
            return
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        if self.isBusy():
            self.freeAvatar(avId)
            return
            
        cheesyEffect = av.getCheesyEffect()[0]
        if cheesyEffect != ToontownGlobals.CENormal:
            self.sendStartMovie(avId)
        else:
            self.sendNormalCheesyEffectMovie(avId)

    def sendStartMovie(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_START,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(NPCToons.CLERK_COUNTDOWN_TIME, self.sendTimeoutMovie, self.uniqueName('clearMovie'))

    def sendNormalCheesyEffectMovie(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_NO_MONEY,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)

    def sendTimeoutMovie(self, task):
        self.timedOut = 1
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_TIMEOUT,
         self.npcId,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        self.ignore(self.air.getAvatarExitEvent(self.busy))
        self.busy = 0
        self.timedOut = 0
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_CLEAR,
         self.npcId,
         0,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def completeCheesyEffectClear(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_COMPLETE,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        
    def avatarSaidNo(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_AVATAR_REJECT,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
            
    def receiveResponse(self, response):
        avId = self.air.getAvatarIdFromSender()
        if self.busy != avId:
            if self.busy != 0:
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCCheesyCleanerAI.receiveResponse busy with %s' % self.busy)
                self.notify.warning('receiveResponse from unknown avId: %s busy: %s' % (avId, self.busy))
            return
        if response > 0:
            if avId in self.air.doId2do:
                av = self.air.doId2do[avId]
                av.b_setCheesyEffect(ToontownGlobals.CENormal, 0, 0)
        if self.timedOut:
            return
        taskMgr.remove(self.uniqueName('clearMovie'))
        if response > 0:
            self.completeCheesyEffectClear(avId)
        else:
            self.avatarSaidNo(avId)

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.sendTimeoutMovie(None)
