from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedKartPadAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedKartPadAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        # Defaults:
        self.area = None
        self.index = -1
        self.startingBlocks = []

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area

    def addStartingBlock(self, startingBlock):
        self.startingBlocks.append(startingBlock)