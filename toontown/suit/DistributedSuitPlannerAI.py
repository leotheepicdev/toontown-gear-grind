from otp.ai.AIBaseGlobal import *
from direct.distributed import DistributedObjectAI
from . import SuitPlannerBase, DistributedSuitAI
from toontown.battle import BattleManagerAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from . import SuitDNA
from toontown.battle import SuitBattleGlobals
from . import SuitTimings
from . import CogPlannerPercentages
from toontown.toon import NPCToons
from toontown.building import HQBuildingAI
from toontown.hood import ZoneUtil
from toontown.building import CogBuildingGlobalsAI
from toontown.building.DistributedBuildingAI import DistributedBuildingAI
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
from panda3d.toontown import DNASuitPoint, SuitLeg
import math, time, random

class DistributedSuitPlannerAI(DistributedObjectAI.DistributedObjectAI, SuitPlannerBase.SuitPlannerBase):
    SuitHoodInfo = [[2100,
      5,
      15,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (1, 2, 3)],
     [2200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (1, 2, 3)],
     [2300,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (1, 2, 3)],
     [1100,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (2, 3, 4)],
     [1200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (3,
       4,
       5,
       6)],
     [1300,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (3,
       4,
       5,
       6)],
     [3100,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (5, 6, 7)],
     [3200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (5, 6, 7)],
     [3300,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (7, 8, 9)],
     [4100,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (2, 3, 4)],
     [4200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (3,
       4,
       5,
       6)],
     [4300,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (4,
       5,
       6,
       7)],
     [5100,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (2, 3, 4)],
     [5200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (3,
       4,
       5,
       6)],
     [5300,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (3,
       4,
       5,
       6)],
     [9100,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (6,
       7,
       8,
       9)],
     [9200,
      3,
      10,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (6,
       7,
       8,
       9)],
     [11000,
      3,
      15,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (4, 5, 6)],
     [11200,
      10,
      20,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (4, 5, 6)],
     [12000,
      10,
      20,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (7, 8, 9)],
     [13000,
      10,
      20,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (8, 9, 10)]]
    SUIT_HOOD_INFO_ZONE = 0
    SUIT_HOOD_INFO_MIN = 1
    SUIT_HOOD_INFO_MAX = 2
    SUIT_HOOD_INFO_SMAX = 3
    SUIT_HOOD_INFO_JCHANCE = 4
    SUIT_HOOD_INFO_LVL = 5
    POP_UPKEEP_DELAY = 10
    POP_ADJUST_DELAY = 300
    PATH_COLLISION_BUFFER = 5
    MAX_SUIT_TYPES = 6
    TOTAL_MAX_SUITS = 50
    MIN_PATH_LEN = 40
    MAX_PATH_LEN = 300
    MIN_TAKEOVER_PATH_LEN = 2
    SUITS_ENTER_BUILDINGS = 1
    SUIT_BUILDING_NUM_SUITS = 1.5
    SUIT_BUILDING_TIMEOUT_TIMER = random.randint(CogBuildingGlobalsAI.COG_BUILDING_TIMER[0], CogBuildingGlobalsAI.COG_BUILDING_TIMER[1])
    defaultSuitName = simbase.config.GetString('suit-type', 'random')
    if defaultSuitName == 'random':
        defaultSuitName = None
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitPlannerAI')

    def __init__(self, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        SuitPlannerBase.SuitPlannerBase.__init__(self)
        self.air = air
        self.zoneId = zoneId
        self.canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)

        self.hoodInfoIdx = -1
        for index in range(len(self.SuitHoodInfo)):
            currHoodInfo = self.SuitHoodInfo[index]
            if currHoodInfo[self.SUIT_HOOD_INFO_ZONE] == self.canonicalZoneId:
                self.hoodInfoIdx = index

        self.currDesired = None
        self.baseNumSuits = (self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_MIN] + self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_MAX]) // 2
        self.wantBuildings = True
        if ZoneUtil.isWelcomeValley(self.zoneId) or ZoneUtil.isCogHQZone(self.zoneId):
            self.wantBuildings = False
        self.suitList = []
        self.numFlyInSuits = 0
        self.numBuildingSuits = 0
        self.numAttemptingTakeover = 0
        self.numAttemptingCogdoTakeover = 0
        self.zoneInfo = {}
        self.zoneIdToPointMap = None
        self.cogHQDoors = []
        self.battleList = []
        self.battleMgr = BattleManagerAI.BattleManagerAI(self.air)
        self.setupDNA()
        if self.notify.getDebug():
            self.notify.debug('Creating a building manager AI in zone' + str(self.zoneId))
        self.buildingMgr = self.air.buildingManagers.get(self.zoneId)
        if self.buildingMgr:
            blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks, animBldgBlocks = self.buildingMgr.getDNABlockLists()
            for currBlock in blocks:
                bldg = self.buildingMgr.getBuilding(currBlock)
                bldg.setSuitPlannerExt(self)

            for currBlock in animBldgBlocks:
                bldg = self.buildingMgr.getBuilding(currBlock)
                bldg.setSuitPlannerExt(self)

        self.dnaStore.resetBlockNumbers()
        self.initBuildingsAndPoints()
        numSuits = simbase.config.GetInt('suit-count', -1)
        if numSuits >= 0:
            self.currDesired = numSuits
        suitHood = simbase.config.GetInt('suits-only-in-hood', -1)
        if suitHood >= 0:
            if self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_ZONE] != suitHood:
                self.currDesired = 0
        self.suitCountAdjust = 0
        return

    def cleanup(self):
        taskMgr.remove(self.taskName('sptUpkeepPopulation'))
        taskMgr.remove(self.taskName('sptAdjustPopulation'))
        for suit in self.suitList:
            suit.stopTasks()
            if suit.isGenerated():
                self.zoneChange(suit, suit.zoneId)
                suit.requestDelete()

        self.suitList = []
        self.numFlyInSuits = 0
        self.numBuildingSuits = 0
        self.numAttemptingTakeover = 0
        self.numAttemptingCogdoTakeover = 0

    def delete(self):
        self.cleanup()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        SuitPlannerBase.SuitPlannerBase.delete(self)

    def initBuildingsAndPoints(self):
        if not self.buildingMgr:
            return
        if self.notify.getDebug():
            self.notify.debug('Initializing building points')
        self.buildingFrontDoors = {}
        self.buildingSideDoors = {}
        for p in self.frontdoorPointList:
            blockNumber = p.getLandmarkBuildingIndex()
            if p.getPointType() < 0:
                self.notify.warning('No landmark building for (%s) in zone %d' % (repr(p), self.zoneId))
            elif blockNumber in self.buildingFrontDoors:
                self.notify.warning('Multiple front doors for building %d in zone %d' % (blockNumber, self.zoneId))
            else:
                self.buildingFrontDoors[blockNumber] = p

        for p in self.sidedoorPointList:
            blockNumber = p.getLandmarkBuildingIndex()
            if p.getPointType() < 0:
                self.notify.warning('No landmark building for (%s) in zone %d' % (repr(p), self.zoneId))
            elif blockNumber in self.buildingSideDoors:
                self.buildingSideDoors[blockNumber].append(p)
            else:
                self.buildingSideDoors[blockNumber] = [
                 p]

    def countNumSuitsPerTrack(self, count):
        for suit in self.suitList:
            if suit.track in count:
                count[suit.track] += 1
            else:
                count[suit.track] = 1

    def formatNumSuitsPerTrack(self, count):
        result = ' '
        for track, num in list(count.items()):
            result += ' %s:%d' % (track, num)

        return result[2:]

    def calcDesiredNumFlyInSuits(self):
        if self.currDesired != None:
            return 0
        return self.baseNumSuits + self.suitCountAdjust

    def getZoneIdToPointMap(self):
        if self.zoneIdToPointMap != None:
            return self.zoneIdToPointMap
        self.zoneIdToPointMap = {}
        for point in self.streetPointList:
            points = self.dnaStore.getAdjacentPoints(point)
            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                p = self.pointIndexes[pi]
                i -= 1
                zoneName = self.dnaStore.getSuitEdgeZone(point.getIndex(), p.getIndex())
                zoneId = int(self.extractGroupName(zoneName))
                if zoneId in self.zoneIdToPointMap:
                    self.zoneIdToPointMap[zoneId].append(point)
                else:
                    self.zoneIdToPointMap[zoneId] = [
                     point]

        return self.zoneIdToPointMap

    def getStreetPointsForBuilding(self, blockNumber):
        pointList = []
        if blockNumber in self.buildingSideDoors:
            for doorPoint in self.buildingSideDoors[blockNumber]:
                points = self.dnaStore.getAdjacentPoints(doorPoint)
                i = points.getNumPoints() - 1
                while i >= 0:
                    pi = points.getPointIndex(i)
                    point = self.pointIndexes[pi]
                    if point.getPointType() == DNASuitPoint.STREETPOINT:
                        pointList.append(point)
                    i -= 1

        if blockNumber in self.buildingFrontDoors:
            doorPoint = self.buildingFrontDoors[blockNumber]
            points = self.dnaStore.getAdjacentPoints(doorPoint)
            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                pointList.append(self.pointIndexes[pi])
                i -= 1

        return pointList

    def createNewSuit(self, blockNumbers, streetPoints, toonBlockTakeover=None, cogdoTakeover=None, minPathLen=None, maxPathLen=None, suitLevel=None, suitType=None, suitTrack=None, suitName=None, skelecog=None, revives=None, summon=False):
        startPoint = None
        blockNumber = None
        if self.notify.getDebug():
            self.notify.debug('Choosing origin from %d+%d possibles.' % (len(streetPoints), len(blockNumbers)))
        while startPoint == None and len(blockNumbers) > 0:
            bn = random.choice(blockNumbers)
            blockNumbers.remove(bn)
            if bn in self.buildingSideDoors:
                for doorPoint in self.buildingSideDoors[bn]:
                    points = self.dnaStore.getAdjacentPoints(doorPoint)
                    i = points.getNumPoints() - 1
                    while blockNumber == None and i >= 0:
                        pi = points.getPointIndex(i)
                        p = self.pointIndexes[pi]
                        i -= 1
                        startTime = SuitTimings.fromSuitBuilding
                        startTime += self.dnaStore.getSuitEdgeTravelTime(doorPoint.getIndex(), pi, self.suitWalkSpeed)
                        if not self.pointCollision(p, doorPoint, startTime):
                            startTime = SuitTimings.fromSuitBuilding
                            startPoint = doorPoint
                            blockNumber = bn

        while startPoint == None and len(streetPoints) > 0:
            p = random.choice(streetPoints)
            streetPoints.remove(p)
            if not self.pointCollision(p, None, SuitTimings.fromSky):
                startPoint = p
                startTime = SuitTimings.fromSky

        if startPoint == None:
            return
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, self)
        newSuit.startPoint = startPoint
        if blockNumber != None:
            newSuit.buildingSuit = 1
            if suitTrack == None:
                tracks = self.buildingMgr.getBuildingTracks(blockNumber)
                trackLen = len(tracks)
                if trackLen == 1:
                    suitTrack = tracks[0]
                else:
                    suitTrack = random.choices(tracks, weights=CogBuildingGlobalsAI.MIXED_LEN_2_CHANCES[trackLen])[0]
        else:
            newSuit.flyInSuit = 1
            newSuit.attemptingTakeover = self.newSuitShouldAttemptTakeover()
        if newSuit.attemptingTakeover == 2:
            cogdoTakeover = True
        if suitName == None:
            if not cogdoTakeover and not ZoneUtil.isWelcomeValley(self.zoneId):
                suitName, skelecog = self.air.suitInvasionManager.getInvadingCog()
            if suitName == None:
                suitName = self.defaultSuitName
        if suitType == None and suitName != None:
            suitType = SuitDNA.getSuitType(suitName)
            suitTrack = SuitDNA.getSuitDept(suitName)
        suitLevel, suitType, suitTrack = self.pickLevelTypeAndTrack(suitLevel, suitType, suitTrack)
        if summon:
            allowBuildingCogs = False
        else:
            allowBuildingCogs = not self.air.suitInvasionManager.getInvading()
        newSuit.setupSuitDNA(suitLevel, suitType, suitTrack, allowBuildingCogs=allowBuildingCogs)
        gotDestination = self.chooseDestination(newSuit, startTime, toonBlockTakeover=toonBlockTakeover, cogdoTakeover=cogdoTakeover, minPathLen=minPathLen, maxPathLen=maxPathLen)
        if not gotDestination:
            self.notify.debug("Couldn't get a destination in %d!" % self.zoneId)
            newSuit.doNotDeallocateChannel = None
            newSuit.delete()
            return
        newSuit.initializePath()
        self.zoneChange(newSuit, None, newSuit.zoneId)
        if skelecog:
            newSuit.setSkelecog(skelecog)
        if revives:
            newSuit.setSkeleRevives(revives)
        newSuit.generateWithRequired(newSuit.zoneId)
        newSuit.d_setSPDoId(self.doId)
        newSuit.moveToNextLeg(None)
        self.suitList.append(newSuit)
        if newSuit.flyInSuit:
            self.numFlyInSuits += 1
        if newSuit.buildingSuit:
            self.numBuildingSuits += 1
        if newSuit.attemptingTakeover:
            self.incrementTakeover()
            if newSuit.takeoverIsCogdo:
                self.numAttemptingCogdoTakeover += 1
        return newSuit
        
    def incrementTakeover(self):
        self.numAttemptingTakeover += 1
        
    def decrementTakeover(self):
        self.numAttemptingTakeover -= 1

    def newSuitShouldAttemptTakeover(self):
        if not self.wantBuildings:
            return 0
        return self.air.bldgMgr.attemptBuildingTakeover(self.zoneId)    

    def chooseDestination(self, suit, startTime, toonBlockTakeover=None, cogdoTakeover=None, minPathLen=None, maxPathLen=None):
        possibles = []
        backup = []
        if cogdoTakeover is None:
            cogdoTakeover = False
        if cogdoTakeover:
            suit.takeoverIsCogdo = True
        if toonBlockTakeover != None:
            suit.attemptingTakeover = 1
            blockNumber = toonBlockTakeover
            if blockNumber in self.buildingFrontDoors:
                possibles.append((blockNumber, self.buildingFrontDoors[blockNumber]))
        elif suit.attemptingTakeover:
            if self.air.bldgMgr.getStreetNumBuildings(self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_ZONE]) >= len(self.air.bldgMgr.getStreetBuildingWeight(self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_ZONE])):
                suit.attemptingTakeover -= 1
                self.decrementTakeover()
                if suit.takeoverIsCogdo:
                    suit.takeoverIsCogdo = 0
                    self.numAttemptingCogdoTakeover -= 1
            for blockNumber in self.buildingMgr.getToonBlocks():
                building = self.buildingMgr.getBuilding(blockNumber)
                extZoneId, intZoneId = building.getExteriorAndInteriorZoneId()
                if not NPCToons.isZoneProtected(intZoneId):
                    if blockNumber in self.buildingFrontDoors:
                        possibles.append((blockNumber, self.buildingFrontDoors[blockNumber]))

        else:
            if self.buildingMgr:
                for blockNumber in self.buildingMgr.getSuitBlocks():
                    tracks = self.buildingMgr.getBuildingTracks(blockNumber)
                    if suit.track in tracks and blockNumber in self.buildingSideDoors:
                        for doorPoint in self.buildingSideDoors[blockNumber]:
                            possibles.append((blockNumber, doorPoint))

            backup = []
            for p in self.streetPointList:
                backup.append((None, p))

        if self.notify.getDebug():
            self.notify.debug('Choosing destination point from %d+%d possibles.' % (len(possibles), len(backup)))
        if len(possibles) == 0:
            possibles = backup
            backup = []
        if minPathLen == None:
            if suit.attemptingTakeover:
                minPathLen = self.MIN_TAKEOVER_PATH_LEN
            else:
                minPathLen = self.MIN_PATH_LEN
        if maxPathLen == None:
            maxPathLen = self.MAX_PATH_LEN
        retryCount = 0
        while len(possibles) > 0 and retryCount < 50:
            p = random.choice(possibles)
            possibles.remove(p)
            if len(possibles) == 0:
                possibles = backup
                backup = []
            path = self.genPath(suit.startPoint, p[1], minPathLen, maxPathLen)
            if path and not self.pathCollision(path, startTime):
                suit.endPoint = p[1]
                suit.minPathLen = minPathLen
                suit.maxPathLen = maxPathLen
                suit.buildingDestination = p[0]
                suit.buildingDestinationIsCogdo = cogdoTakeover
                suit.setPath(path)
                return 1
            retryCount += 1

        return 0

    def pathCollision(self, path, elapsedTime):
        pathLength = path.getNumPoints()
        i = 0
        pi = path.getPointIndex(i)
        point = self.pointIndexes[pi]
        adjacentPoint = self.pointIndexes[path.getPointIndex(i + 1)]
        while point.getPointType() == DNASuitPoint.FRONTDOORPOINT or point.getPointType() == DNASuitPoint.SIDEDOORPOINT:
            i += 1
            lastPi = pi
            pi = path.getPointIndex(i)
            adjacentPoint = point
            point = self.pointIndexes[pi]
            elapsedTime += self.dnaStore.getSuitEdgeTravelTime(lastPi, pi, self.suitWalkSpeed)

        result = self.pointCollision(point, adjacentPoint, elapsedTime)
        return result

    def pointCollision(self, point, adjacentPoint, elapsedTime):
        for suit in self.suitList:
            if suit.pointInMyPath(point, elapsedTime):
                return 1

        if adjacentPoint != None:
            return self.battleCollision(point, adjacentPoint)
        else:
            points = self.dnaStore.getAdjacentPoints(point)
            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                p = self.pointIndexes[pi]
                i -= 1
                if self.battleCollision(point, p):
                    return 1

        return 0

    def battleCollision(self, point, adjacentPoint):
        zoneName = self.dnaStore.getSuitEdgeZone(point.getIndex(), adjacentPoint.getIndex())
        zoneId = int(self.extractGroupName(zoneName))
        return self.battleMgr.cellHasBattle(zoneId)

    def removeSuit(self, suit):
        self.zoneChange(suit, suit.zoneId)
        if self.suitList.count(suit) > 0:
            self.suitList.remove(suit)
            if suit.flyInSuit:
                self.numFlyInSuits -= 1
            if suit.buildingSuit:
                self.numBuildingSuits -= 1
            if suit.attemptingTakeover:
                self.decrementTakeover()
                if suit.takeoverIsCogdo:
                    self.numAttemptingCogdoTakeover -= 1
        suit.requestDelete()

    def countTakeovers(self):
        count = 0
        for suit in self.suitList:
            if suit.attemptingTakeover:
                count += 1

        return count

    def countCogdoTakeovers(self):
        count = 0
        for suit in self.suitList:
            if suit.attemptingTakeover and suit.takeoverIsCogdo:
                count += 1

        return count

    def __waitForNextUpkeep(self):
        t = random.random() * 2.0 + self.POP_UPKEEP_DELAY
        taskMgr.doMethodLater(t, self.upkeepSuitPopulation, self.taskName('sptUpkeepPopulation'))

    def __waitForNextAdjust(self):
        t = random.random() * 10.0 + self.POP_ADJUST_DELAY
        taskMgr.doMethodLater(t, self.adjustSuitPopulation, self.taskName('sptAdjustPopulation'))

    def upkeepSuitPopulation(self, task):
        targetFlyInNum = self.calcDesiredNumFlyInSuits()
        targetFlyInNum = min(targetFlyInNum, self.TOTAL_MAX_SUITS - self.numBuildingSuits)
        streetPoints = self.streetPointList[:]
        flyInDeficit = (targetFlyInNum - self.numFlyInSuits + 3) // 4
        while flyInDeficit > 0:
            if not self.createNewSuit([], streetPoints):
                break
            flyInDeficit -= 1

        if self.buildingMgr:
            suitBuildings = self.buildingMgr.getEstablishedSuitBlocks()
        else:
            suitBuildings = []
        if self.currDesired != None:
            targetBuildingNum = max(0, self.currDesired - self.numFlyInSuits)
        else:
            targetBuildingNum = int(len(suitBuildings) * self.SUIT_BUILDING_NUM_SUITS)
        targetBuildingNum += flyInDeficit
        targetBuildingNum = min(targetBuildingNum, self.TOTAL_MAX_SUITS - self.numFlyInSuits)
        buildingDeficit = (targetBuildingNum - self.numBuildingSuits + 3) // 4
        while buildingDeficit > 0:
            if not self.createNewSuit(suitBuildings, streetPoints):
                break
            buildingDeficit -= 1

        if self.notify.getDebug() and self.currDesired == None:
            self.notify.debug('zone %d has %d of %d fly-in and %d of %d building suits.' % (self.zoneId, self.numFlyInSuits, targetFlyInNum, self.numBuildingSuits, targetBuildingNum))
            if buildingDeficit != 0:
                self.notify.debug('remaining deficit is %d.' % buildingDeficit)
        if self.buildingMgr:
            suitBuildings = self.buildingMgr.getEstablishedSuitBlocks()
            self.SUIT_BUILDING_TIMEOUT_TIMER -= 1
            if self.SUIT_BUILDING_TIMEOUT_TIMER == 0:
                self.SUIT_BUILDING_TIMEOUT_TIMER = random.randint(CogBuildingGlobalsAI.COG_BUILDING_TIMER[0], CogBuildingGlobalsAI.COG_BUILDING_TIMER[1])
                if len(suitBuildings) > 1:
                    oldest = None
                    oldestAge = 0
                    now = time.time()
                    for b in suitBuildings:
                        building = self.buildingMgr.getBuilding(b)
                        if hasattr(building, 'elevator'):
                            if building.elevator.fsm.getCurrentState().getName() == 'waitEmpty':
                                age = now - building.becameSuitTime
                                if age > oldestAge:
                                    oldest = building
                                    oldestAge = age

                    if oldestAge >= 3600:
                        self.notify.info('Street %d has %d buildings; reclaiming an hour old cog building.' % (self.zoneId, len(suitBuildings)))
                        oldest.b_setVictorList([0, 0, 0, 0])
                        oldest.updateSavedBy(None)
                        oldest.toonTakeOver()
        self.__waitForNextUpkeep()
        return Task.done

    def adjustSuitPopulation(self, task):
        hoodInfo = self.SuitHoodInfo[self.hoodInfoIdx]
        if hoodInfo[self.SUIT_HOOD_INFO_MAX] == 0:
            self.__waitForNextAdjust()
            return Task.done
        min = hoodInfo[self.SUIT_HOOD_INFO_MIN]
        max = hoodInfo[self.SUIT_HOOD_INFO_MAX]
        adjustment = random.choice((-2, -1, -1, 0, 0, 0, 1, 1, 2))
        self.suitCountAdjust += adjustment
        desiredNum = self.calcDesiredNumFlyInSuits()
        if desiredNum < min:
            self.suitCountAdjust = min - self.baseNumSuits
        else:
            if desiredNum > max:
                self.suitCountAdjust = max - self.baseNumSuits
        self.__waitForNextAdjust()
        return Task.done

    def chooseStreetNoPreference(self, hoodInfo, totalWeight):
        c = random.random() * totalWeight
        t = 0
        for currHoodInfo in hoodInfo:
            weight = currHoodInfo[self.SUIT_HOOD_INFO_BWEIGHT]
            t += weight
            if c < t:
                return currHoodInfo

        self.notify.warning('Weighted random choice failed!  Total is %s, chose %s' % (t, c))
        return random.choice(hoodInfo)

    def initTasks(self):
        self.__waitForNextUpkeep()
        self.__waitForNextAdjust()

    def resyncSuits(self):
        for suit in self.suitList:
            suit.resync()

    def flySuits(self):
        for suit in self.suitList:
            if suit.pathState == 1:
                suit.flyAwayNow()

    def requestBattle(self, zoneId, suit, toonId):
        self.notify.debug('requestBattle() - zone: %d suit: %d toon: %d' % (zoneId, suit.doId, toonId))
        canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        if canonicalZoneId not in self.battlePosDict:
            return 0
        toon = self.air.doId2do.get(toonId)
        if toon.getBattleId() > 0:
            self.notify.warning('We tried to request a battle when the toon was already in battle')
            return 0
        if toon:
            if hasattr(toon, 'doId'):
                toon.b_setBattleId(toonId)
        pos = self.battlePosDict[canonicalZoneId]
        interactivePropTrackBonus = -1
        if simbase.config.GetBool('props-buff-battles', True) and canonicalZoneId in self.cellToGagBonusDict:
            tentativeBonusTrack = self.cellToGagBonusDict[canonicalZoneId]
            trackToHolidayDict = {ToontownBattleGlobals.SQUIRT_TRACK: ToontownGlobals.HYDRANTS_BUFF_BATTLES, ToontownBattleGlobals.THROW_TRACK: ToontownGlobals.MAILBOXES_BUFF_BATTLES, ToontownBattleGlobals.HEAL_TRACK: ToontownGlobals.TRASHCANS_BUFF_BATTLES}
            if tentativeBonusTrack in trackToHolidayDict:
                holidayId = trackToHolidayDict[tentativeBonusTrack]
                if simbase.air.holidayManager.isHolidayRunning(holidayId) and simbase.air.holidayManager.getCurPhase(holidayId) >= 1:
                    interactivePropTrackBonus = tentativeBonusTrack
        self.battleMgr.newBattle(zoneId, zoneId, pos, suit, toonId, self.__battleFinished, self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_SMAX], interactivePropTrackBonus)
        for currOther in self.zoneInfo[zoneId]:
            self.notify.debug('Found suit %d in this new battle zone %d' % (currOther.getDoId(), zoneId))
            if currOther != suit:
                if currOther.pathState == 1 and currOther.legType == SuitLeg.TWalk:
                    self.checkForBattle(zoneId, currOther)

        return 1

    def __battleFinished(self, zoneId):
        self.notify.debug('DistSuitPlannerAI:  battle in zone ' + str(zoneId) + ' finished')
        currBattleIdx = 0
        while currBattleIdx < len(self.battleList):
            currBattle = self.battleList[currBattleIdx]
            if currBattle[0] == zoneId:
                self.notify.debug('DistSuitPlannerAI: battle removed')
                self.battleList.remove(currBattle)
            else:
                currBattleIdx = currBattleIdx + 1

        return None

    def __suitCanJoinBattle(self, zoneId):
        battle = self.battleMgr.getBattle(zoneId)
        if len(battle.suits) >= battle.maxSuits:
            return 0
        if battle:
            if simbase.config.GetBool('suits-always-join', 0):
                return 1
            jChanceList = self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_JCHANCE]
            ratioIdx = len(battle.toons) - battle.numSuitsEver + 2
            if ratioIdx >= 0:
                if ratioIdx < len(jChanceList):
                    if random.randint(0, 99) < jChanceList[ratioIdx]:
                        return 1
                else:
                    self.notify.warning('__suitCanJoinBattle idx out of range!')
                    return 1
        return 0

    def checkForBattle(self, zoneId, suit):
        if self.battleMgr.cellHasBattle(zoneId):
            if self.__suitCanJoinBattle(zoneId) and self.battleMgr.requestBattleAddSuit(zoneId, suit):
                pass
            else:
                suit.flyAwayNow()
            return 1
        else:
            return 0

    def postBattleResumeCheck(self, suit):
        self.notify.debug('DistSuitPlannerAI:postBattleResumeCheck:  suit ' + str(suit.getDoId()) + ' is leaving battle')
        battleIndex = 0
        for currBattle in self.battleList:
            if suit.zoneId == currBattle[0]:
                self.notify.debug('    battle found' + str(suit.zoneId))
                for currPath in currBattle[1]:
                    for currPathPtSuit in range(suit.currWpt, suit.myPath.getNumPoints()):
                        ptIdx = suit.myPath.getPointIndex(currPathPtSuit)
                        if self.notify.getDebug():
                            self.notify.debug('    comparing' + str(ptIdx) + 'with' + str(currPath))
                        if currPath == ptIdx:
                            if self.notify.getDebug():
                                self.notify.debug('    match found, telling' + 'suit to fly')
                            return 0

            else:
                battleIndex = battleIndex + 1

        pointList = []
        for currPathPtSuit in range(suit.currWpt, suit.myPath.getNumPoints()):
            ptIdx = suit.myPath.getPointIndex(currPathPtSuit)
            if self.notify.getDebug():
                self.notify.debug('    appending point with index of' + str(ptIdx))
            pointList.append(ptIdx)

        self.battleList.append([suit.zoneId, pointList])
        return 1

    def zoneChange(self, suit, oldZone, newZone=None):
        if oldZone in self.zoneInfo and suit in self.zoneInfo[oldZone]:
            self.zoneInfo[oldZone].remove(suit)
        if newZone != None:
            if newZone not in self.zoneInfo:
                self.zoneInfo[newZone] = []
            self.zoneInfo[newZone].append(suit)
        return

    def d_setZoneId(self, zoneId):
        self.sendUpdate('setZoneId', [self.getZoneId()])

    def getZoneId(self):
        return self.zoneId

    def suitListQuery(self):
        suitIndexList = []
        for suit in self.suitList:
            suitIndexList.append(SuitDNA.suitHeadTypes.index(suit.dna.name))

        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'suitListResponse', [suitIndexList])

    def buildingListQuery(self):
        # huh, do we even need this
        buildingList = [0, 0, 0, 0]
        for dept in SuitDNA.suitDepts:
            if dept in buildingDict:
                buildingList[SuitDNA.suitDepts.index(dept)] = buildingDict[dept]

        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'buildingListResponse', [buildingList])

    def pickLevelTypeAndTrack(self, level=None, type=None, track=None):
        if level == None:
            level = random.choice(self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_LVL])
        if type == None:
            typeChoices = list(range(max(level - 4, 1), min(level, self.MAX_SUIT_TYPES) + 1))
            type = random.choice(typeChoices)
        else:
            level = min(max(level, type), type + 4)
        if track == None:
            track = self.pickTrack()
        self.notify.debug('pickLevelTypeAndTrack: %d %d %s' % (level, type, track))
        return (level, type, track)
        
    def pickTrack(self):
        tracks = CogPlannerPercentages.CogHoodPercentageInfo.get(self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_ZONE])
        track = SuitDNA.suitDepts[SuitBattleGlobals.pickFromFreqList(tracks)]
        return track        