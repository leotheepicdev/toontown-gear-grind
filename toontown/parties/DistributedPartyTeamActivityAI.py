from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.activityFSMs import TeamActivityAIFSM


class DistributedPartyTeamActivityAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyTeamActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        self.fsm = TeamActivityAIFSM(self)
        self.avIds = ([], [])
        self.responses = set()
        self.startDelay = PartyGlobals.TeamActivityStartDelay
        self.conclusionDuration = PartyGlobals.TeamActivityDefaultConclusionDuration
        self.clientWaitDelay = PartyGlobals.TeamActivityClientWaitDelay

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.b_setState('WaitForEnough')

    def delete(self):
        taskMgr.remove(self.uniqueName('start-game'))
        taskMgr.remove(self.uniqueName('client-ready'))
        taskMgr.remove(self.uniqueName('game-finished'))
        taskMgr.remove(self.uniqueName('handle-conclusion'))
        DistributedPartyActivityAI.delete(self)

    def toonJoinRequest(self, team):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='toonJoinRequest called while on a different district!')
            return

        if self.fsm.state not in ('WaitForEnough', 'WaitToStart'):
            self.sendUpdateToAvatarId(avId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if len(self.avIds[team]) >= self.getPlayersPerTeam()[1]:
            self.sendUpdateToAvatarId(avId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Full])
            return

        if avId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to join party team activity again!')
            self.sendUpdateToAvatarId(avId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        self.avIds[team].append(avId)
        if avId not in self.toonsPlaying:
            self.toonsPlaying.append(avId)

        self.update()

    def toonExitRequest(self, team):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='toonJoinRequest called while on a different district!')
            return

        if self.fsm.state not in ('WaitForEnough', 'WaitToStart'):
            self.sendUpdateToAvatarId(avId, 'exitRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if not (avId in self.avIds[0] or avId in self.avIds[1]):
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to exit DistributedPartyTeamActivityAI team, but not in one!')
            self.sendUpdateToAvatarId(avId, 'exitRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        currentTeam = (1, 0)[avId in self.avIds[0]]
        self.avIds[currentTeam].remove(avId)
        if avId in self.toonsPlaying:
            self.toonsPlaying.remove(avId)

        self.update()

    def toonSwitchTeamRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='toonJoinRequest called while on a different district!')
            return

        if not self.getCanSwitchTeams():
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to switch DistributedPartyTeamActivityAI team when not allowed!')
            self.sendUpdateToAvatarId(avId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if not (avId in self.avIds[0] or avId in self.avIds[1]):
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to switch DistributedPartyTeamActivityAI team, but not in one!')
            self.sendUpdateToAvatarId(avId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        currentTeam = (1, 0)[avId in self.avIds[0]]
        otherTeam = (1, 0)[currentTeam]
        if len(self.avIds[otherTeam]) >= self.getPlayersPerTeam()[1]:
            self.sendUpdateToAvatarId(avId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Full])
            return

        self.avIds[currentTeam].remove(avId)
        self.avIds[otherTeam].append(avId)
        self.update()

    def getDuration(self):
        return PartyGlobals.TeamActivityDefaultDuration

    def getCanSwitchTeams(self):
        return self.fsm.state in ('Off', 'WaitForEnough', 'WaitToStart')

    def d_setState(self, state, data=0):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime(), data])

    def b_setState(self, state, data=0):
        self.fsm.request(state, data)
        self.d_setState(state, data)

    def getPlayersPerTeam(self):
        return PartyGlobals.TeamActivityDefaultMinPlayersPerTeam, PartyGlobals.TeamActivityDefaultMaxPlayersPerTeam

    def update(self):
        self.sendUpdate('setToonsPlaying', self.getToonsPlaying())
        if self.fsm.state == 'WaitForEnough':
            if self.areTeamsCorrect():
                self.b_setState('WaitToStart')
        elif self.fsm.state == 'WaitToStart':
            if not self.areTeamsCorrect():
                self.b_setState('WaitForEnough')

    def startWaitForEnough(self, data):
        pass

    def finishWaitForEnough(self):
        pass

    def startWaitToStart(self, data):
        def advance(task):
            self.fsm.request('WaitClientsReady')
            self.d_setState('Rules')
            return task.done

        taskMgr.doMethodLater(self.startDelay, advance, self.uniqueName('start-game'))

    def finishWaitToStart(self):
        taskMgr.remove(self.uniqueName('start-game'))

    def __startGame(self, task=None):
        self.b_setState('Active')
        if task:
            return task.done

    def startWaitClientsReady(self):
        self.responses = set()
        taskMgr.doMethodLater(self.clientWaitDelay, self.__startGame, self.uniqueName('client-ready'))

    def finishWaitClientsReady(self):
        taskMgr.remove(self.uniqueName('client-ready'))

    def toonReady(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        self.responses.add(avId)
        if self.responses == set(self.toonsPlaying):
            self.__startGame()

    def startActive(self, data):
        taskMgr.doMethodLater(self.getDuration(), self.__gameFinished, self.uniqueName('game-finished'))

    def finishActive(self):
        taskMgr.remove(self.uniqueName('game-finished'))

    def __gameFinished(self, task):
        self.calcReward()
        self.b_setState('Conclusion')
        return task.done

    def areTeamsCorrect(self):
        minPlayers = self.getPlayersPerTeam()[0]
        return all(len(self.avIds[i]) >= minPlayers for i in range(2))

    def getToonsPlaying(self):
        return self.avIds

    def calcReward(self):
        raise NotImplementedError('calcReward')  # Must be overridden by subclass.

    def startConclusion(self, data):
        taskMgr.doMethodLater(self.conclusionDuration, self.handleConclusion, self.uniqueName('handle-conclusion'))

    def finishConclusion(self):
        taskMgr.remove(self.uniqueName('handle-conclusion'))

    def handleConclusion(self, task):
        raise NotImplementedError('handleConclusion')  # Must be overridden by subclass.
