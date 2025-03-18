from . import DistributedTreasureAI
from toontown.toonbase import ToontownGlobals

class DistributedSZTreasureAI(DistributedTreasureAI.DistributedTreasureAI):
    SILLY_SURGE_CHANCE = 0.07

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, x, y, z, sillySurgeChance=self.SILLY_SURGE_CHANCE)
        self.healAmount = treasurePlanner.healAmount
        self.moneyAmount = treasurePlanner.moneyAmount

    def validAvatar(self, av):
        if self.sillySurge:
            return True
        return av.hp >= -1 and av.hp < av.maxHp

    def healAvatar(self, av):
        if av.hp >= av.maxHp:
            return
        if av.hp == -1:
            av.hp = 0
        if ToontownGlobals.VALENTINES_DAY in simbase.air.holidayManager.currentHolidays:
            av.toonUp(self.healAmount * 2)
        else:
            av.toonUp(self.healAmount)

    def d_setGrab(self, avId):
        DistributedTreasureAI.DistributedTreasureAI.d_setGrab(self, avId)
        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            if self.validAvatar(av):
                self.healAvatar(av)
                if self.sillySurge:
                    av.addMoney(self.moneyAmount, display=True)
