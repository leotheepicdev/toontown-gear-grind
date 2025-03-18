from direct.distributed.DistributedObjectAI import DistributedObjectAI
from .DistributedCogTowerInteriorAI import DistributedCogTowerInteriorAI

class DistributedCogTowerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.activeInteriors = {}
		
    def generate(self):
        DistributedObjectAI.generate(self)
		
    def getDoId(self):
        return 0
		
    def createCogTowerInterior(self, players):
        cogTowerZone = self.air.allocateZone()
        interior = DistributedCogTowerInteriorAI(self.air, cogTowerZone, self, players)
        interior.generateWithRequired(cogTowerZone)
        interior.b_setState('WaitForAllToonsInside')
        self.activeInteriors[cogTowerZone] = interior
        return cogTowerZone
		
    def destroyCogTowerInterior(self, cogTowerZone):
        if cogTowerZone in self.activeInteriors:
            self.activeInteriors[cogTowerZone].requestDelete()
            del self.activeInteriors[cogTowerZone]
            self.air.deallocateZone(cogTowerZone)
	