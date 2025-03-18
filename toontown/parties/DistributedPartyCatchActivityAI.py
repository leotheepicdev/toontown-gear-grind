from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.DistributedPartyCatchActivityBase import DistributedPartyCatchActivityBase
from toontown.toonbase import TTLocalizer

class DistributedPartyCatchActivityAI(DistributedPartyActivityAI, DistributedPartyCatchActivityBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyCatchActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        self.startTimestamp = globalClockDelta.getRealNetworkTime(bits=32)
        self.generations = []
        self.player2catches = {}
        self.playing = False
        self.numGenerations = 1

    def delete(self):
        taskMgr.remove(self.uniqueName('new-generation'))
        DistributedPartyActivityAI.delete(self)

    def setStartTimestamp(self, startTimestamp):
        self.startTimestamp = startTimestamp

    def d_setStartTimestamp(self, startTimestamp):
        self.sendUpdate('setStartTimestamp', [startTimestamp])

    def b_setStartTimestamp(self, startTimestamp):
        self.setStartTimestamp(startTimestamp)
        self.d_setStartTimestamp(startTimestamp)

    def getStartTimestamp(self):
        return self.startTimestamp

    def setGenerations(self, generations):
        self.generations = generations

    def d_setGenerations(self, generations):
        self.sendUpdate('setGenerations', [generations])

    def b_setGenerations(self, generations):
        self.setGenerations(generations)
        self.d_setGenerations(generations)

    def getGenerations(self):
        return self.generations

    def claimCatch(self, generation, objNum, objType):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to catch while not playing!')
            return

        if PartyGlobals.DOTypeId2Name[objType] != 'anvil':
            self.player2catches[avId] += 1

        self.sendUpdate('setObjectCaught', [avId, generation, objNum])

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to enter activity from another shard!')
            return

        if avId in self.toonsPlaying:
            return

        self.player2catches[avId] = 0
        if not self.playing:
            self.startGame()
            self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])

        self.toonsPlaying.append(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId not in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to exit the catch activity but they\'re not currently playing!')
            return

        catches = self.getTotalReward(self.player2catches[avId])
        del self.player2catches[avId]
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to award beans while not in district!')
            return

        if catches > PartyGlobals.CatchMaxTotalReward:
            catches = PartyGlobals.CatchMaxTotalReward

        self.sendUpdateToAvatarId(avId, 'showJellybeanReward',
                                  [catches, av.getMoney(), TTLocalizer.PartyCatchRewardMessage % (catches, catches)])
        av.addMoney(catches)
        DistributedPartyActivityAI.toonExitDemand(self)

    def startGame(self):
        self.playing = True
        self.calcDifficultyConstants(len(self.toonsPlaying))
        self.generations.append(
            [self.numGenerations, globalClockDelta.getRealNetworkTime(bits=32), len(self.toonsPlaying)])
        self.numGenerations += 1
        self.b_setGenerations(self.generations)
        taskMgr.doMethodLater(self.generationDuration, self.newGeneration, self.uniqueName('new-generation'))

    def newGeneration(self, task):
        if self.toonsPlaying:
            self.startGame()
        else:
            self.playing = False

        return task.done
