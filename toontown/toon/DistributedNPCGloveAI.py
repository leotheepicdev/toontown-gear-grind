from otp.ai.AIBaseGlobal import *
from .DistributedNPCToonBaseAI import *
from . import ToonDNA
from direct.task.Task import Task

class DistributedNPCGloveAI(DistributedNPCToonBaseAI):
    freeClothes = simbase.config.GetBool('free-clothes', 0)

    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        self.timedOut = 0
        self.givesQuests = 0
        self.customerId = None

    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        self.customerId = None
        DistributedNPCToonBaseAI.delete(self)

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.notify.warning('Avatar: %s not found' % avId)
            return
        if self.isBusy():
            self.freeAvatar(avId)
            return
        av = self.air.doId2do[avId]
        self.customerId = avId
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        flag = NPCToons.PURCHASE_MOVIE_START_BROWSE
        if av.getGloveTickets():
            flag = NPCToons.PURCHASE_MOVIE_START
        self.sendShoppingMovie(avId, flag)
        DistributedNPCToonBaseAI.avatarEnter(self)

    def sendShoppingMovie(self, avId, flag):
        self.busy = avId
        self.sendUpdate('setMovie', [flag, self.npcId, avId, ClockDelta.globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(NPCToons.TAILOR_COUNTDOWN_TIME, self.sendTimeoutMovie, self.uniqueName('clearMovie'))

    def rejectAvatar(self, avId):
        pass

    def sendTimeoutMovie(self, task):
        self.timedOut = 1
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_TIMEOUT, self.npcId, self.busy, ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        self.ignore(self.air.getAvatarExitEvent(self.busy))
        self.customerId = None
        self.busy = 0
        self.timedOut = 0
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_CLEAR, self.npcId, 0, ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def completePurchase(self, avId):
        self.busy = 0
        self.timedOut = 0
        self.customerId = 0
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_COMPLETE, self.npcId, avId, ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)

    def requestClearMovie(self):
        avId = self.air.getAvatarIdFromSender()
        if avId == self.customerId:
            taskMgr.remove(self.uniqueName('clearMovie'))
            self.completePurchase(avId)

    def setDNA(self, blob):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.customerId:
            if self.customerId:
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCGloveAI.setDNA customer is %s' % self.customerId)
                self.notify.warning('customerId: %s, but got setDNA for: %s' % (self.customerId, avId))
            return
        testDNA = ToonDNA.ToonDNA()
        if not testDNA.isValidNetString(blob):
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCGloveAI.setDNA: invalid dna: %s' % blob)
            return
        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            if av.removeGloveTicket() == 1 or self.freeClothes:
                av.b_setDNAString(blob)
            else:
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCGloveAI.setDNA bogus clothing ticket')
                self.notify.warning('NPCTailor: setDNA() - client tried to purchase with bogus clothing ticket!')
        else:
            self.notify.warning('no av for avId: %d' % avId)
        if self.timedOut == 1:
            return
        if self.busy == avId:
            taskMgr.remove(self.uniqueName('clearMovie'))
            self.completePurchase(avId)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCGloveAI.setDNA busy with %s' % self.busy)
            self.notify.warning('setDNA from unknown avId: %s busy: %s' % (avId, self.busy))

    def __handleUnexpectedExit(self, avId):
        if self.busy == avId:
            self.sendClearMovie(None)
