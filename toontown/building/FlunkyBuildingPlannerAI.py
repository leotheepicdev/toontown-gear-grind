from otp.ai.AIBaseGlobal import *
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedSuitAI
import random

class FlunkyBuildingPlannerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('FlunkyBuildingPlannerAI')

    def __init__(self, zoneId):
        self.zoneId = zoneId
		
    def genFloorSuits(self, floor):
        revives = 0
        skelecog = 0
        
        joinChance = 1
        suitHandles = {}
        activeSuitArray = []
        reserveSuitArray = []
        
        if floor == 0:
            activeSuit1 = self.__genSuitObject(3)
            activeSuitArray.append(activeSuit1)
            activeSuit2 = self.__genSuitObject(4)
            activeSuitArray.append(activeSuit2)
            activeSuit3 = self.__genSuitObject(3)
            activeSuitArray.append(activeSuit3)
            activeSuit4 = self.__genSuitObject(3)
            activeSuitArray.append(activeSuit4)
            reserveSuit1 = self.__genSuitObject(3)
            reserveSuitArray.append([reserveSuit1, 1])
            reserveSuit2 = self.__genSuitObject(2)
            reserveSuitArray.append([reserveSuit2, 1])
            reserveSuit3 = self.__genSuitObject(3)
            reserveSuitArray.append([reserveSuit3, 1])
        else:
            suit1 = self.__genSuitObject(4)
            activeSuitArray.append(suit1)
            flunky = self.__genSpecificSuit('f', 6)
            activeSuitArray.append(flunky)
            suit3 = self.__genSuitObject(3)
            activeSuitArray.append(suit3)
            suit4 = self.__genSuitObject(3)
            activeSuitArray.append(suit4)
            suit5 = self.__genSuitObject(3)
            activeSuitArray.append(suit5)
            reserveSuit1 = self.__genSuitObject(2)
            reserveSuitArray.append([reserveSuit1, 1])
            reserveSuit2 = self.__genSuitObject(2)
            reserveSuitArray.append([reserveSuit2, 1])
        
        suitHandles['activeSuits'] = activeSuitArray
        suitHandles['reserveSuits'] = reserveSuitArray
        return suitHandles
        
    def __genSpecificSuit(self, suitName, level):
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, None)
        dna = SuitDNA.SuitDNA()
        dna.newSuit(suitName)
        newSuit.dna = dna
        newSuit.setLevel(level)
        newSuit.generateWithRequired(self.zoneId)
        newSuit.node().setName('suit-%s' % newSuit.doId)
        return newSuit

    def __genSuitObject(self, level):
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, None)
        dna = SuitDNA.SuitDNA()
        dna.newSuitBuilding(level, random.choice(['c', 'l', 's', 'm']), 0.65)
        newSuit.dna = dna
        newSuit.setLevel(level)
        newSuit.generateWithRequired(self.zoneId)
        newSuit.node().setName('suit-%s' % newSuit.doId)
        return newSuit
        
