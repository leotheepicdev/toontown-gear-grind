from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedHotTubAI(DistributedObjectAI):
    TOON_UP_FREQ = 30

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [None, None, None, None]
        self.pos = (0, 0, 0)
        
    def delete(self):
        for toonId in self.toons:
            if toonId != None:
                toon = self.air.doId2do.get(toonId)
                toon.stopToonUp()
        DistributedObjectAI.delete(self)
        
    def requestBoard(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        # logic check for max toons goes here
        
        # add toon here
        self.startToonUpTask(av)
            
    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        self.stopToonUpTask(av)
        
        # remove toon

    def sendBoardResponse(self):
        pass
        
    def sendExitResponse(self):
        pass

    def setPos(self, x, y, z):
        self.pos = (x, y, z)
        
    def getPos(self):
        return self.pos
            
    def startToonUpTask(self, av):
        if not av.isToonedUp():
            av.startToonUp(self.TOON_UP_FREQ)
        
    def stopToonUpTask(self, av):
        av.stopToonUp()