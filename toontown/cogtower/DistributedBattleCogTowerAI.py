from panda3d.core import Point3
from toontown.battle.BattleBase import *
from toontown.battle.BattleCalculatorAI import *
from toontown.battle import DistributedBattleBaseAI
from toontown.battle.SuitBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.showbase import PythonUtil
from direct.showbase.PythonUtil import addListsByValue
from direct.task import Task
from otp.ai.AIBase import *
from toontown.toonbase.ToontownBattleGlobals import *


class DistributedBattleCogTowerAI(DistributedBattleBaseAI.DistributedBattleBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleCogTowerAI')

    def __init__(self, air, zoneId, roundCallback=None, finishCallback=None, maxSuits=4, bossBattle=0):
        DistributedBattleBaseAI.DistributedBattleBaseAI.__init__(self, air, zoneId, finishCallback, maxSuits, bossBattle)
        self.streetBattle = 0
        self.roundCallback = roundCallback
        self.fsm.addState(State.State('BuildingReward', self.enterBuildingReward, self.exitBuildingReward, ['Resume']))
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('BuildingReward')
        self.elevatorPos = Point3(0, -30, 0)
        self.resumeNeedUpdate = 0

    def announceGenerate(self):
        DistributedBattleBaseAI.DistributedBattleBaseAI.announceGenerate(self)
        self.registerToons()

    def setInitialMembers(self, toonIds, suits):
        for suit in suits:
            self.addSuit(suit)
        for toonId in toonIds:
            self.addToon(toonId)
        self.fsm.request('FaceOff')

    def registerToons(self):
        for toonId in self.toons:
            toon = simbase.air.doId2do.get(toonId)
            toon.b_setBattleId(self.doId)

    def delete(self):
        del self.roundCallback
        DistributedBattleBaseAI.DistributedBattleBaseAI.delete(self)

    def faceOffDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('faceOffDone() - ignoring toon: %d' % toonId)
            return
        elif self.fsm.getCurrentState().getName() != 'FaceOff':
            self.notify.warning('faceOffDone() - in state: %s' % self.fsm.getCurrentState().getName())
            return
        elif self.toons.count(toonId) == 0:
            self.notify.warning('faceOffDone() - toon: %d not in toon list' % toonId)
            return
        self.responses[toonId] += 1
        self.notify.debug('toon: %d done facing off' % toonId)
        if not self.ignoreFaceOffDone:
            if self.allToonsResponded():
                self.handleFaceOffDone()
            else:
                self.timer.stop()
                self.timer.startCallback(TIMEOUT_PER_USER, self.__serverFaceOffDone)

    def enterFaceOff(self):
        self.notify.debug('enterFaceOff()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        self.timer.startCallback(self.calcToonMoveTime(self.pos, self.elevatorPos) + FACEOFF_TAUNT_T + SERVER_BUFFER_TIME, self.__serverFaceOffDone)

    def __serverFaceOffDone(self):
        self.notify.debug('faceoff timed out on server')
        self.ignoreFaceOffDone = 1
        self.handleFaceOffDone()

    def exitFaceOff(self):
        self.timer.stop()
        self.resetResponses()

    def handleFaceOffDone(self):
        for suit in self.suits:
            self.activeSuits.append(suit)
        for toon in self.toons:
            self.activeToons.append(toon)
            self.sendEarnedExperience(toon)
        self.d_setMembers()
        self.b_setState('WaitForInput')

    def localMovieDone(self, needUpdate, deadToons, deadSuits, lastActiveSuitDied):
        self.timer.stop()
        self.resumeNeedUpdate = needUpdate
        self.resumeDeadToons = deadToons
        self.resumeDeadSuits = deadSuits
        self.resumeLastActiveSuitDied = lastActiveSuitDied
        if len(self.toons) == 0:
            self.d_setMembers()
            self.b_setState('Resume')
        else:
            totalHp = 0
            for suit in self.suits:
                if suit.currHP > 0:
                    totalHp += suit.currHP
                    continue
            self.roundCallback(self.activeToons, totalHp, deadSuits)

    def handleReviveState(self):
        if self.reviveState == 'Reward':
            self.b_setState('Reward')
        elif self.reviveState == 'BuildingReward':
            self.setRewardState()
        else:
            self.setState('WaitForJoin')        

    def resume(self, currentFloor=0, topFloor=0):
        if len(self.suits) == 0:
            self.d_setMembers()
            self.suitsKilledPerFloor.append(self.suitsKilledThisBattle)
            for toonId in self.activeToons:
                toon = self.getToon(toonId)
                if toon:
                    if toonId in self.avId2SuitsKilled:
                        self.avId2SuitsKilled[toonId] += len(self.suitsKilledThisBattle)
                    else:
                        self.avId2SuitsKilled[toonId] = len(self.suitsKilledThisBattle)
            if topFloor == 0:
                if len(self.deadRevives) > 0:
                    self.reviveState = 'Reward'
                    self.setState('WaitForReviveInput')
                else:
                    self.b_setState('Reward')
            else:
                self.reviveState = 'BuildingReward'
                self.setRewardState()
        else:
            if self.resumeNeedUpdate == 1:
                self.d_setMembers()
                if len(self.resumeDeadSuits) > 0 and self.resumeLastActiveSuitDied == 0 or len(self.resumeDeadToons) > 0:
                    self.needAdjust = 1
            if len(self.deadRevives) > 0:
                self.reviveState = 'WaitForJoin'
                self.setState('WaitForReviveInput')
            else:
                self.setState('WaitForJoin')
        self.resumeNeedUpdate = 0
        self.resumeDeadToons = []
        self.resumeDeadSuits = []
        self.resumeLastActiveSuitDied = 0

    def enterReservesJoining(self, ts=0):
        return None

    def exitReservesJoining(self, ts=0):
        return None

    def enterReward(self):
        self.timer.startCallback(FLOOR_REWARD_TIMEOUT, self.serverRewardDone)

    def exitReward(self):
        self.timer.stop()

    def enterBuildingReward(self):
        self.resetResponses()
        self.assignRewards()
        self.timer.startCallback(BUILDING_REWARD_TIMEOUT, self.serverRewardDone)

    def exitBuildingReward(self):
        self.exitResume()

    def enterResume(self):
        DistributedBattleBaseAI.DistributedBattleBaseAI.enterResume(self)
        self.finishCallback(self.zoneId, self.activeToons)

    def exitResume(self):
        DistributedBattleBaseAI.DistributedBattleBaseAI.exitResume(self)
        taskName = self.taskName('finish')
        taskMgr.remove(taskName)
