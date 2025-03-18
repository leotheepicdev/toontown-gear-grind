from otp.ai.AIBaseGlobal import *
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedSuitAI
import random

class CogTowerPlannerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('CogTowerPlannerAI')

    def __init__(self, zoneId):
        self.zoneId = zoneId
		
    def genFloorSuits(self, floor):
        revives = 0
        skelecog = 0
        executive = 0
        if floor >= 0 and floor <= 8:
            possibleSuits = (3, 7)
            levelRange = (1, 4)
        elif floor >= 9 and floor <= 18:
            possibleSuits = (4, 8)
            levelRange = (3, 6)
            skelecog = 1
        elif floor >= 19 and floor <= 38:
            possibleSuits = (5, 9)
            levelRange = (5, 8)
            skelecog = 1
        elif floor >= 39 and floor <= 58:
            possibleSuits = (6, 10)
            levelRange = (7, 10)
            skelecog = 1
        elif floor >= 59 and floor <= 98:
            possibleSuits = (7, 11)
            levelRange = (8, 12)
            skelecog = 1
        elif floor >= 99:
            possibleSuits = (8, 12)
            levelRange = (9, 12)
            skelecog = 1
            revives = 1
        suits = random.randint(possibleSuits[0], possibleSuits[1])
        activeSuits = random.randint(1, min(suits, 4))
        
        reserveSuits = 0
        joinChance = 1
        if activeSuits != suits:
            reserveSuits = suits - activeSuits
        suitHandles = {}
        activeSuitArray = []
        reserveSuitArray = []
        for i in range(activeSuits):
            level = random.randint(levelRange[0], levelRange[1])
            suit = self.__genSuitObject(level, skelecog, revives)
            activeSuitArray.append(suit)
        suitHandles['activeSuits'] = activeSuitArray
        for i in range(reserveSuits):
            level = random.randint(levelRange[0], levelRange[1])
            suit = self.__genSuitObject(level, skelecog, revives)
            reserveSuitArray.append([suit, 1])
        suitHandles['reserveSuits'] = reserveSuitArray
        return suitHandles

    def __genSuitObject(self, level, skelecog, revives):
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, None)
        dna = SuitDNA.SuitDNA()
        if skelecog:
            if random.random() <= 0.1:
                dna.newSuitNull(level)
                newSuit.dna = dna
                newSuit.setupNullCog(level)
                revives = 0
            else:
                dna.newSuitRandom(SuitDNA.getRandomSuitType(level), random.choice(['c', 'l', 's', 'm']))
                newSuit.dna = dna
                newSuit.setLevel(level)
        else:
            dna.newSuitRandom(SuitDNA.getRandomSuitType(level), random.choice(['c', 'l', 's', 'm']))
            newSuit.dna = dna
            newSuit.setLevel(level)
        newSuit.generateWithRequired(self.zoneId)
        if revives:
            if random.random() <= 0.1:
                newSuit.b_setSkeleRevives(1)
        newSuit.node().setName('suit-%s' % newSuit.doId)
        return newSuit
        
