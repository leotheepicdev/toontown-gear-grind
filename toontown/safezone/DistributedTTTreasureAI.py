from . import DistributedSZTreasureAI
from toontown.toonbase import ToontownGlobals
import random

class DistributedTTTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):
    SUGAR_RUSH_CHANCE = 0.12
    SUGAR_RUSH_HEAL_AMOUNT = 4

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        self.variations = [0, 1, 2, 3]

    def healAvatar(self, av):
        if av.hp >= av.maxHp:
            return
        if av.hp == -1:
            av.hp = 0
            
        healAmount = self.healAmount    
        extraStrCode = -1
        if random.random() <= self.SUGAR_RUSH_CHANCE:
            healAmount = self.SUGAR_RUSH_HEAL_AMOUNT
            extraStrCode = 0
        if ToontownGlobals.VALENTINES_DAY in simbase.air.holidayManager.currentHolidays:
            av.toonUp(healAmount * 2, extraStrCode=extraStrCode)
        else:
            av.toonUp(healAmount, extraStrCode=extraStrCode)