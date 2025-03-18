from direct.directnotify.DirectNotifyGlobal import directNotify

from direct.showbase.PythonUtil import bound
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyTeamActivityAI import DistributedPartyTeamActivityAI
from toontown.toonbase import TTLocalizer

class DistributedPartyCogActivityAI(DistributedPartyTeamActivityAI):
    notify = directNotify.newCategory('DistributedPartyCogActivityAI')
    SCORE_MULTIPLIER = 25
    PERFECT_WIN_SCORE = 75
    PERFECT_LOSS_SCORE = 0

    def __init__(self, air, parent, activity):
        DistributedPartyTeamActivityAI.__init__(self, air, parent, activity)
        self.startDelay = PartyGlobals.CogActivityStartDelay
        self.conclusionDuration = PartyGlobals.CogActivityConclusionDuration
        self.highScore = ['', 0]
        self.scores = {}
        self.cogDistances = [0, 0, 0]
        self._teamScores = [0, 0]

    def getDuration(self):
        return PartyGlobals.CogActivityDuration

    def getPlayersPerTeam(self):
        return PartyGlobals.CogActivityMinPlayersPerTeam, PartyGlobals.CogActivityMaxPlayersPerTeam

    def pieHitsCog(self, avId, timestamp, hitCogNum, x, y, z, direction, part):
        senderId = self.air.getAvatarIdFromSender()
        if not senderId:
            return

        av = self.air.doId2do.get(senderId)
        if not av:
            self.air.writeServerEvent('suspicious', senderId=senderId,
                                      issue='pieHitsCog called while on a different district!')
            return

        if avId != senderId:
            self.air.writeServerEvent('suspicious', senderId=senderId, avId=avId,
                                      issue='Sent pieHitsCog as someone else!')
            return

        if not (senderId in self.avIds[0] or senderId in self.avIds[1]):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Sent pieHitsCog, but not playing!')
            return

        if hitCogNum > 2:
            self.air.writeServerEvent('suspicious', avId=avId, hitCogNum=hitCogNum,
                                      issue='Invalid hitCogNum received in pieHitsCog!')
            return

        if part:
            pushFactor = PartyGlobals.CogPinataPushHeadFactor
        else:
            pushFactor = PartyGlobals.CogPinataPushBodyFactor

        if avId not in self.scores:
            self.scores[avId] = 0

        self.scores[avId] += pushFactor
        self.cogDistances[hitCogNum] = bound(self.cogDistances[hitCogNum] + direction * pushFactor, -1.0, 1.0)
        self.b_setCogDistances(self.cogDistances)

    def setCogDistances(self, cogDistances):
        self.cogDistances = cogDistances

    def d_setCogDistances(self, cogDistances):
        self.sendUpdate('setCogDistances', [cogDistances])

    def b_setCogDistances(self, cogDistances):
        self.setCogDistances(cogDistances)
        self.d_setCogDistances(cogDistances)

    def getCogDistances(self):
        return self.cogDistances

    def setHighScore(self, toonName, score):
        self.highScore = [toonName, score]

    def d_setHighScore(self, toonName, score):
        self.sendUpdate('setHighScore', [toonName, score])

    def b_setHighScore(self, toonName, score):
        self.setHighScore(toonName, score)
        self.d_setHighScore(toonName, score)

    def getHighScore(self):
        return self.highScore

    def areTeamsCorrect(self):
        minPlayers = self.getPlayersPerTeam()[0]
        return (len(self.avIds[0]) + len(self.avIds[1])) > minPlayers

    def startWaitClientsReady(self):
        self.balanceTeams()
        DistributedPartyTeamActivityAI.startWaitClientsReady(self)

    def startActive(self, data):
        self.cogDistances = [0, 0, 0]
        self.scores = {}
        DistributedPartyTeamActivityAI.startActive(self, data)

    def calcReward(self):
        for avId, score in list(self.scores.items()):
            newScore = int(score / PartyGlobals.CogPinataPushBodyFactor)
            if newScore > self.highScore[1]:
                av = self.air.doId2do.get(avId)
                if av:
                    self.b_setHighScore(av.getName(), newScore)

        scores = [0, 0]
        for distance in self.cogDistances:
            team = 0
            if distance > 0:
                team = 1

            scores[team] += int(round(float(abs(distance) * self.SCORE_MULTIPLIER)))

        self.b_setState('Conclusion', scores[0] * 10000 + scores[1])
        self._teamScores = scores

    def handleConclusion(self, task):
        def handleReward(team):
            otherTeam = 1 - team
            if self._teamScores[otherTeam] == self._teamScores[team]:
                reward = PartyGlobals.CogActivityTieBeans
            elif self._teamScores[otherTeam] == self.PERFECT_WIN_SCORE:
                reward = PartyGlobals.CogActivityPerfectLossBeans
            elif self._teamScores[otherTeam] == self.PERFECT_LOSS_SCORE:
                reward = PartyGlobals.CogActivityPerfectWinBeans
            elif self._teamScores[otherTeam] > self._teamScores[team]:
                reward = PartyGlobals.CogActivityLossBeans
            elif self._teamScores[otherTeam] < self._teamScores[team]:
                reward = PartyGlobals.CogActivityWinBeans
            else:
                return task.done

            winnerTeam = self._teamScores[team] > self._teamScores[otherTeam]
            if winnerTeam:
                message = TTLocalizer.PartyTeamActivityLocalAvatarTeamWins + '\n\n' + TTLocalizer.PartyTeamActivityRewardMessage % reward
            else:
                message = TTLocalizer.PartyTeamActivityRewardMessage % reward

            reward = self.getTotalReward(int(reward))
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

    def balanceTeams(self):
        numPlayersTeamOne = len(self.avIds[0])
        numPlayersTeamTwo = len(self.avIds[1])
        numToMove = int(abs(numPlayersTeamOne - numPlayersTeamTwo) / 2)
        if numToMove > 0:
            index = 0
            if numPlayersTeamTwo > numPlayersTeamOne:
                index = 1

            for i in range(numToMove):
                self.avIds[1 - index].append(self.avIds[index].pop())

        self.sendUpdate('setToonsPlaying', self.getToonsPlaying())
