from .DistributedFlunkyBuildingInteriorAI import DistributedFlunkyBuildingInteriorAI

class FlunkyBuildingMgrAI:

    def __init__(self, air):
        self.air = air
        self.activeInteriors = {}
        
    def getDoId(self):
        return 0
        
    def createFlunkyBuildingInterior(self, players):
        zoneId = self.air.allocateZone()
        interior = DistributedFlunkyBuildingInteriorAI(self.air, zoneId, self, players)
        interior.generateWithRequired(zoneId)
        interior.b_setState('WaitForAllToonsInside')
        self.activeInteriors[zoneId] = interior
        return zoneId
		
    def destroyFlunkyBuildingInterior(self, zoneId):
        if zoneId in self.activeInteriors:
            self.activeInteriors[zoneId].requestDelete()
            del self.activeInteriors[zoneId]
            self.air.deallocateZone(zoneId)
