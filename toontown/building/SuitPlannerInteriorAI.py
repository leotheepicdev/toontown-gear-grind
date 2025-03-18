from otp.ai.AIBaseGlobal import *
import random, functools
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedSuitAI
from . import CogBuildingGlobals, CogBuildingGlobalsAI

class SuitPlannerInteriorAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitPlannerInteriorAI')

    def __init__(self, numFloors, bldgLevel, bldgDepts, bldgType, zone, respectInvasions=1, toonLen=4):
        self.dbg_nSuits1stRound = config.GetBool('n-suits-1st-round', 0)
        self.dbg_4SuitsPerFloor = config.GetBool('4-suits-per-floor', 0)
        self.dbg_1SuitPerFloor = config.GetBool('1-suit-per-floor', 0)
        self.zoneId = zone
        self.numFloors = numFloors
        self.bldgType = bldgType
        self.respectInvasions = respectInvasions
        dbg_defaultSuitName = simbase.config.GetString('suit-type', 'random')
        if dbg_defaultSuitName == 'random':
            self.dbg_defaultSuitType = None
        else:
            self.dbg_defaultSuitType = SuitDNA.getSuitType(dbg_defaultSuitName)
        if isinstance(bldgLevel, str):
            self.notify.warning('bldgLevel is a string!')
            bldgLevel = int(bldgLevel)
        self.depts = bldgDepts
        self.toonLen = toonLen
        self._genSuitInfos(numFloors, bldgLevel)

    def __genJoinChances(self, num):
        joinChances = []
        for currChance in range(num):
            joinChances.append(random.randint(1, 100))

        joinChances.sort(key=functools.cmp_to_key(cmp))
        return joinChances

    def _genSuitInfos(self, numFloors, bldgLevel):
    
        def chooseDept():
            deptLen = len(self.depts)
            if deptLen == 1:
                return self.depts[0]
            return random.choices(self.depts, weights=CogBuildingGlobalsAI.MIXED_LEN_2_CHANCES[deptLen])[0]
            
    
        self.suitInfos = {
          0: None,
          1: None,
          2: None,
          3: None,
          4: None,
          5: None,
          6: None,
        }
        self.notify.debug('\n\ngenerating suitsInfos with numFloors (' + str(numFloors) + ') bldgLevel (' + str(bldgLevel) + '+1) and depts (' + str(self.depts) + ')')
        floors = range(numFloors)
        for currFloor in floors:
            posFloor = abs(currFloor)
            infoDict = {}
            lvls = self.__genLevelList(bldgLevel, posFloor, numFloors)
            activeDicts = []
            maxActive = min(4, len(lvls))
            if self.dbg_nSuits1stRound:
                numActive = min(self.dbg_nSuits1stRound, maxActive)
            else:
                numActive = random.randint(1, maxActive)
            if currFloor + 1 == numFloors and len(lvls) > 1:
                origBossSpot = len(lvls) - 1
                if numActive == 1:
                    newBossSpot = numActive - 1
                else:
                    newBossSpot = numActive - 2
                tmp = lvls[newBossSpot]
                lvls[newBossSpot] = lvls[origBossSpot]
                lvls[origBossSpot] = tmp
            bldgInfo = CogBuildingGlobalsAI.CogBuildingInfo[self.toonLen][bldgLevel]
            if len(bldgInfo) > CogBuildingGlobalsAI.SUIT_BLDG_INFO_REVIVES:
                revives = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_REVIVES][0]
            else:
                revives = 0
            for currActive in range(numActive - 1, -1, -1):
                level = lvls[currActive]
                type = self.__genNormalSuitType(level)
                activeDict = {}
                activeDict['type'] = type
                activeDict['track'] = chooseDept()
                activeDict['level'] = level
                activeDict['revives'] = revives
                activeDicts.append(activeDict)

            infoDict['activeSuits'] = activeDicts
            reserveDicts = []
            numReserve = len(lvls) - numActive
            joinChances = self.__genJoinChances(numReserve)
            for currReserve in range(numReserve):
                level = lvls[currReserve + numActive]
                type = self.__genNormalSuitType(level)
                reserveDict = {}
                reserveDict['type'] = type
                reserveDict['track'] = chooseDept()
                reserveDict['level'] = level
                reserveDict['revives'] = revives
                reserveDict['joinChance'] = joinChances[currReserve]
                reserveDicts.append(reserveDict)

            infoDict['reserveSuits'] = reserveDicts
            self.suitInfos[currFloor] = infoDict

    def __genNormalSuitType(self, lvl):
        if self.dbg_defaultSuitType != None:
            return self.dbg_defaultSuitType
        return SuitDNA.getRandomSuitType(lvl)

    def __genLevelList(self, bldgLevel, currFloor, numFloors):
        bldgInfo = CogBuildingGlobalsAI.CogBuildingInfo[self.toonLen][bldgLevel]
        if self.dbg_1SuitPerFloor:
            return [1]
        if self.dbg_4SuitsPerFloor:
            return [5, 6, 7, 10]
        lvlPoolRange = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_LVL_POOL]
        maxFloors = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_FLOORS][1]
        lvlPoolMults = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_LVL_POOL_MULTS]
        floorIdx = min(currFloor, maxFloors - 1)
        lvlPoolMin = lvlPoolRange[0] * lvlPoolMults[floorIdx]
        lvlPoolMax = lvlPoolRange[1] * lvlPoolMults[floorIdx]
        lvlPool = random.randint(int(lvlPoolMin), int(lvlPoolMax))
        lvlMin = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_SUIT_LVLS][0]
        lvlMax = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_SUIT_LVLS][1]
        self.notify.debug('Level Pool: ' + str(lvlPool))
        lvlList = []
        while lvlPool >= lvlMin:
            newLvl = random.randint(lvlMin, min(lvlPool, lvlMax))
            lvlList.append(newLvl)
            lvlPool -= newLvl

        if currFloor + 1 == numFloors:
            bossLvlRange = bldgInfo[CogBuildingGlobalsAI.SUIT_BLDG_INFO_BOSS_LVLS]
            newLvl = random.randint(bossLvlRange[0], bossLvlRange[1])
            lvlList.append(newLvl)
        lvlList.sort(key=functools.cmp_to_key(cmp))
        self.notify.debug('LevelList: ' + repr(lvlList))
        return lvlList

    def __setupSuitInfo(self, floor, suit, bldgTrack, suitLevel, suitType):
        suitName, skeleton = simbase.air.suitInvasionManager.getInvadingCog()
        if suitName and self.respectInvasions:
            suitType = SuitDNA.getSuitType(suitName)
            bldgTrack = SuitDNA.getSuitDept(suitName)
            suitLevel = min(max(suitLevel, suitType), suitType + 4)
        else:
            if self.bldgType == CogBuildingGlobals.SUIT_BLDG_UNDERGROUND:
                chance = 0.15
            else:
                chance = 0.65
        dna = SuitDNA.SuitDNA()
        if suitName and self.respectInvasions:
            dna.newSuitRandom(suitType, bldgTrack)
        else:
            dna.newSuitBuilding(suitLevel, bldgTrack, chance)
        suit.dna = dna
        self.notify.debug('Creating suit type ' + suit.dna.name + ' of level ' + str(suitLevel) + ' from type ' + str(suitType) + ' and track ' + str(bldgTrack))
        suit.setLevel(suitLevel)
        return skeleton

    def __genSuitObject(self, floor, suitZone, suitType, bldgTrack, suitLevel, revives=0):
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, None)
        skel = self.__setupSuitInfo(floor, newSuit, bldgTrack, suitLevel, suitType)
        if skel:
            newSuit.setSkelecog(1)
        newSuit.setSkeleRevives(revives)
        newSuit.generateWithRequired(suitZone)
        newSuit.node().setName('suit-%s' % newSuit.doId)
        return newSuit

    def genFloorSuits(self, floor):
        suitHandles = {}
        floorInfo = self.suitInfos[floor]
        activeSuits = []
        for activeSuitInfo in floorInfo['activeSuits']:
            suit = self.__genSuitObject(floor, self.zoneId, activeSuitInfo['type'], activeSuitInfo['track'], activeSuitInfo['level'], activeSuitInfo['revives'])
            activeSuits.append(suit)

        suitHandles['activeSuits'] = activeSuits
        reserveSuits = []
        for reserveSuitInfo in floorInfo['reserveSuits']:
            suit = self.__genSuitObject(floor, self.zoneId, reserveSuitInfo['type'], reserveSuitInfo['track'], reserveSuitInfo['level'], reserveSuitInfo['revives'])
            reserveSuits.append((suit, reserveSuitInfo['joinChance']))

        suitHandles['reserveSuits'] = reserveSuits
        return suitHandles