from toontown.battle import DistributedBattleWaitersAI
from toontown.battle import DistributedBattleBaseAI

class DistributedBattleVirtualsAI(DistributedBattleWaitersAI.DistributedBattleWaitersAI):

    def __init__(self, air, bossCog, roundCallback, finishCallback, battleSide, battleIndex):
        DistributedBattleWaitersAI.DistributedBattleWaitersAI.__init__(self, air, bossCog, roundCallback, finishCallback, battleSide)
        self.battleIndex = battleIndex

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

            self.roundCallback(self.activeToons, totalHp, deadSuits, self.battleIndex)

    def enterResume(self):
        self.joinableFsm.request('Unjoinable')
        self.runableFsm.request('Unrunable')
        DistributedBattleBaseAI.DistributedBattleBaseAI.enterResume(self)
        self.finishCallback(self.zoneId, self.activeToons, self.battleIndex)