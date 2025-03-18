from panda3d.core import *

from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.suit import SuitDNA
from toontown.suit import SuitDialog
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.tutorial.DistributedBattleTutorialAI import DistributedBattleTutorialAI

class TutorialBattleManagerAI:
    def __init__(self, avId):
        self.avId = avId

    def destroy(self, battle):
        if battle.suitsKilledThisBattle:
            if self.avId in simbase.air.tutorialManager.playerDict:
                simbase.air.tutorialManager.playerDict[self.avId].preparePlayerForHQ()
        battle.requestDelete()

class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = directNotify.newCategory('DistributedTutorialSuitAI')

    def __init__(self, air):
        DistributedSuitBaseAI.__init__(self, air, None)
        
    def destroy(self):
        del self.dna

    def createSuit(self, name, level):
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit(name)
        self.dna = suitDNA
        self.setLevel(level)

    def requestBattle(self, x, y, z, h, p, r):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        if av.getBattleId() > 0:
            self.notify.warning('Avatar %d tried to request a battle, but is already in one.' % avId)
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle(avId)
            return

        battle = DistributedBattleTutorialAI(self.air, TutorialBattleManagerAI(avId), Point3(35, 20, -0.5), self, avId, 20001)
        battle.battleCellId = 0
        battle.generateWithRequired(self.zoneId)

    def getConfrontPosHpr(self):
        return (self.confrontPos, self.confrontHpr)