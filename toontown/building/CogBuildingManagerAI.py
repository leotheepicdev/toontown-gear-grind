from toontown.toonbase import ToontownGlobals
from toontown.toon import NPCToons
from toontown.suit import SuitDNA
import random

class BuildingStreet:

    def __init__(self):
        self.numBuildings = 0 # How much buildings do we have in total?
        self.minBuildings = 0 # How many do we assign at initial AI creation?
        self.difficulties = (0) # How difficult are our buildings?
        self.buildingWeight = [0] # Determine if we want to spawn a building based on our number of allowed buildings.
        self.buildingChance = 0 # Ok, we have the potential to spawn a building. What are the odds that our lazy cog wants to actually work?
        self.foChance = 0 # What are the odds that this building is instead a field office?
        
    def getNumBuildings(self):
        return self.numBuildings
        
    def getMinBuildings(self):
        return self.minBuildings
        
    def getMaxBuildingsAllowed(self):
        return len(self.buildingWeight)

    def getBuildingDifficulties(self):
        return self.difficulties

    def getBuildingWeight(self):
        return self.buildingWeight
        
    def getBuildingChance(self):
        return self.buildingChance
        
    def getFieldOfficeChance(self):
        return self.foChance

class TTC2100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.buildingWeight = [80, 60, 40, 0, 0, 0, 0, 0, 0]
        self.difficulties = (0, 1, 2)
        self.buildingChance = 10
        self.foChance = 10
        
class TTC2200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.buildingWeight = [80, 60, 40, 0, 0, 0, 0, 0, 0]
        self.difficulties = (0, 1, 2)
        self.buildingChance = 10
        self.foChance = 10
        
class TTC2300(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.buildingWeight = [80, 60, 40, 0, 0, 0, 0, 0, 0]
        self.difficulties = (0, 1, 2)
        self.buildingChance = 10
        self.foChance = 10
        
class DD1100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 1
        self.difficulties = (1, 2, 3)
        self.buildingWeight = [80, 60, 40, 20, 10, 0, 0, 0, 0, 0]
        self.buildingChance = 75
        self.foChance = 10
        
class DD1200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 1
        self.difficulties = (1, 2, 3)
        self.buildingWeight = [80, 60, 40, 20, 10, 0, 0, 0, 0, 0]
        self.buildingChance = 75
        self.foChance = 10
        
class DD1300(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 1
        self.difficulties = (2, 3, 4, 5)
        self.buildingWeight = [80, 60, 40, 20, 10, 0, 0, 0, 0, 0]
        self.buildingChance = 75
        self.foChance = 10
        
class DG5100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 2
        self.difficulties = (1, 2, 3)
        self.buildingWeight = [80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 90
        self.foChance = 10
        
class DG5200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 2
        self.difficulties = (2, 3, 4, 5)
        self.buildingWeight = [80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 90
        self.foChance = 10
        
class DG5300(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 2
        self.difficulties = (2, 3, 4, 5)
        self.buildingWeight = [80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 90
        self.foChance = 10

class MM4100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 3
        self.difficulties = (1, 2, 3)
        self.buildingWeight = [80, 80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 95
        self.foChance = 10
        
class MM4200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 3
        self.difficulties = (2, 3, 4, 5)
        self.buildingWeight = [80, 80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 95
        self.foChance = 10
        
class MM4300(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 3
        self.difficulties = (3, 4, 5, 6)
        self.buildingWeight = [80, 80, 80, 60, 40, 20, 10, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 95
        self.foChance = 10
        
class BR3100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 5
        self.difficulties = (4, 5, 6)
        self.buildingWeight = [80, 80, 80, 80, 80, 60, 40, 20, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 100
        self.foChance = 10
        
class BR3200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 5
        self.difficulties = (4, 5, 6)
        self.buildingWeight = [80, 80, 80, 80, 80, 60, 40, 20, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 100
        self.foChance = 10

class BR3300(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 5
        self.difficulties = (6, 7, 8)
        self.buildingWeight = [80, 80, 80, 80, 80, 60, 40, 20, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 100
        self.foChance = 10
        
class DL9100(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 6
        self.difficulties = (5, 6, 7, 8, 9, 10)
        self.buildingWeight = [100, 80, 80, 80, 80, 80, 60, 40, 20, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 100
        self.foChance = 10
        
class DL9200(BuildingStreet):
    
    def __init__(self):
        BuildingStreet.__init__(self)
        self.minBuildings = 6
        self.difficulties = (5, 6, 7, 8, 9, 10)
        self.buildingWeight = [100, 80, 80, 80, 80, 80, 60, 40, 20, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buildingChance = 100
        self.foChance = 10

class CogBuildingManagerAI:

    def __init__(self, air):
        self.air = air
        self.streetBuildingClasses = {ToontownGlobals.SillyStreet: TTC2100(),
          ToontownGlobals.LoopyLane: TTC2200(),
          ToontownGlobals.PunchlinePlace: TTC2300(),
          ToontownGlobals.BarnacleBoulevard: DD1100(),
          ToontownGlobals.SeaweedStreet: DD1200(),
          ToontownGlobals.LighthouseLane: DD1300(),
          ToontownGlobals.ElmStreet: DG5100(),
          ToontownGlobals.MapleStreet: DG5200(),
          ToontownGlobals.OakStreet: DG5300(),
          ToontownGlobals.AltoAvenue: MM4100(),
          ToontownGlobals.BaritoneBoulevard: MM4200(),
          ToontownGlobals.TenorTerrace: MM4300(),
          ToontownGlobals.WalrusWay: BR3100(),
          ToontownGlobals.SleetStreet: BR3200(),
          ToontownGlobals.PolarPlace: BR3300(),
          ToontownGlobals.LullabyLane: DL9100(),
          ToontownGlobals.PajamaPlace: DL9200()}
          
    def addBuilding(self, zoneId):
        self.streetBuildingClasses[zoneId].numBuildings += 1
        
    def removeBuilding(self, zoneId):
        self.streetBuildingClasses[zoneId].numBuildings -= 1
        
    def getStreetNumBuildings(self, zoneId):
        return self.streetBuildingClasses[zoneId].numBuildings
          
    def getStreetBuildingWeight(self, zoneId):
        return self.streetBuildingClasses[zoneId].getBuildingWeight()
          
    def attemptBuildingTakeover(self, zoneId):
        street = self.streetBuildingClasses[zoneId]
        bldgWeightList = street.getBuildingWeight()
        if street.getNumBuildings() >= len(bldgWeightList):
            bldgWeight = 0
        else:
            try:
                bldgWeight = street.getBuildingWeight()[street.getNumBuildings()]
            except:
                bldgWeight = 0
        if bldgWeight == 0:
            return 0 
        if bldgWeight >= random.randint(0, 100):
            if street.getBuildingChance() >= random.randint(0, 100):
                if street.getFieldOfficeChance() >= random.randint(0, 100):
                    return 2
                return 1
            else:
                return 0
        return 0
        
    def pickBuildingDifficulty(self, zoneId):
        street = self.streetBuildingClasses[zoneId]
        return random.choice(street.getBuildingDifficulties())
        
    def assignInitialCogBuildings(self):
        for zoneId in self.streetBuildingClasses:
            street = self.streetBuildingClasses[zoneId]
            numBuildings = street.numBuildings
            if numBuildings < street.minBuildings:
                bldgMgr = self.air.buildingManagers[zoneId]
                for i in range(street.minBuildings - numBuildings):
                    blockNumber = random.choice(bldgMgr.getToonBlocks())
                    building = bldgMgr.getBuilding(blockNumber)
                    if building == None:
                        continue
                    if NPCToons.isZoneProtected(building.getExteriorAndInteriorZoneId()[1]):
                        continue
                    invadingCog, specialCog = self.air.suitInvasionManager.getInvadingCog()
                    if invadingCog:
                        dept = SuitDNA.getSuitDept(invadingCog)
                    else:
                        dept = self.air.suitPlanners[zoneId].pickTrack()
                    building.suitTakeOver(dept)        

                bldgMgr.save()                    