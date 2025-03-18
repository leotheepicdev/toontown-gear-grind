from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI


class DistributedPartyDanceActivityBaseAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyDanceActivityBaseAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        self.toons = []
        self.headings = []

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])

    def updateDancingToon(self, state, anim):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to update their state while not dancing!')
            return

        self.sendUpdate('setDancingToonState', [avId, state, anim])

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to enter dance activity twice!')
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to interact with a party activity from a different district!')
            return

        self.toons.append(avId)
        self.headings.append(av.getH())
        self.sendUpdate('setToonsPlaying', [self.toons, self.headings])

    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.toons:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to exit a dance floor they\'re not on!')
            return

        index = self.toons.index(avId)
        self.toons.remove(avId)
        self.headings.pop(index)
        self.sendUpdate('setToonsPlaying', [self.toons, self.headings])
