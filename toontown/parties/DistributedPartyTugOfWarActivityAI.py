from direct.directnotify import DirectNotifyGlobal

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyTeamActivityAI import DistributedPartyTeamActivityAI
from toontown.toonbase import TTLocalizer

scoreMap = {
    'tie': (PartyGlobals.TugOfWarTieReward, PartyGlobals.TugOfWarTieReward),
    0: (PartyGlobals.TugOfWarWinReward, PartyGlobals.TugOfWarLossReward),
    1: (PartyGlobals.TugOfWarLossReward, PartyGlobals.TugOfWarWinReward),
    10: (PartyGlobals.TugOfWarFallInWinReward, PartyGlobals.TugOfWarFallInLossReward),
    11: (PartyGlobals.TugOfWarFallInLossReward, PartyGlobals.TugOfWarFallInWinReward)
}


class DistributedPartyTugOfWarActivityAI(DistributedPartyTeamActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyTugOfWarActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyTeamActivityAI.__init__(self, air, parent, activity)
        self.startDelay = PartyGlobals.TugOfWarStartDelay
        self.conclusionDuration = PartyGlobals.TugOfWarConclusionDuration
        self.forces = {}
        self.pos = 0
        self._hasFall = 0
        self._winnerTeam = 0
        self._teamScores = (0, 0)

    def getDuration(self):
        return PartyGlobals.TugOfWarDuration

    def getPlayersPerTeam(self):
        return PartyGlobals.TugOfWarMinimumPlayersPerTeam, PartyGlobals.TugOfWarMaximumPlayersPerTeam

    def getCanSwitchTeams(self):
        # Can't switch teams on Tug-Of-War.
        return False

    def reportKeyRateForce(self, keyRate, force):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='reportKeyRateForce called while on a different district!')
            return

        if not (avId in self.avIds[0] or avId in self.avIds[1]):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Sent reportKeyRateForce, but not playing!')
            return

        self.forces[avId] = force
        self.sendUpdate('updateToonKeyRate', [avId, keyRate])
        teamOneForce = self.getTeamForce(0)
        teamTwoForce = self.getTeamForce(1)
        combinedForce = teamOneForce + teamTwoForce
        if combinedForce:
            delta = (teamOneForce - teamTwoForce) / combinedForce
            self.pos += -delta * PartyGlobals.TugOfWarMovementFactor * 2
            self.sendUpdate('updateToonPositions', [self.pos])

    def reportFallIn(self, losingTeam):
        if self.fsm.state != 'Active' or self._hasFall:
            return

        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='reportFallIn called while on a different district!')
            return

        if not (avId in self.avIds[0] or avId in self.avIds[1]):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Sent reportFallIn, but not playing!')
            return

        losers = int(self.pos < 0)
        if losers != losingTeam:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Called reportFallIn with incorrect losingTeam!')
            return

        self._hasFall = 1
        self.calcReward()
        taskMgr.remove(self.uniqueName('game-finished'))  # Mitigate races

    def calcReward(self):
        nobodyWins = abs(self.pos) <= 2
        if nobodyWins:
            self._winnerTeam = 3
            self._teamScores = scoreMap['tie']
        else:
            self._winnerTeam = int(self.pos > 0)
            self._teamScores = scoreMap[self._winnerTeam + self._hasFall * 10]

        self.b_setState('Conclusion', self._winnerTeam)

    def startActive(self, data):
        self.forces = {}
        self.pos = 0
        self._hasFall = 0
        self._winnerTeam = 0
        self._teamScores = (0, 0)
        DistributedPartyTeamActivityAI.startActive(self, data)

    def handleConclusion(self, task):
        def handleReward(team):
            reward = self.getTotalReward(self._teamScores[team])
            message = TTLocalizer.PartyTeamActivityRewardMessage % reward
            for avId in self.avIds[team]:
                av = self.air.doId2do.get(avId)
                if av:
                    self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [reward, av.getMoney(), message])
                    av.addMoney(reward)

        handleReward(0)
        handleReward(1)
        self.toonsPlaying = []
        self.avIds = ([], [])
        self.sendUpdate('setToonsPlaying', self.getToonsPlaying())
        self.b_setState('WaitForEnough')
        return task.done

    def getTeamForce(self, team):
        return sum(self.forces.get(avId, 0) for avId in self.avIds[team])
