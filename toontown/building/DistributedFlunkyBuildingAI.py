from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedFlunkyBuildingAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.elevatorDoId = 0
        self.posHpr = (0, 0, 0, 0, 0, 0)
        
    def setElevatorDoId(self, elevatorDoId):
        self.elevatorDoId = elevatorDoId
        
    def getElevatorDoId(self):
        return self.elevatorDoId
        
    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)
        
    def getPosHpr(self):
        return self.posHpr