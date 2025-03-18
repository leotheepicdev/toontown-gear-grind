from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.safezone.DistributedSZTreasureAI import DistributedSZTreasureAI

class DistributedEFlyingTreasureAI(DistributedSZTreasureAI):
    notify = directNotify.newCategory('DistributedEFlyingTreasureAI')
    
    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        self.variations = [0, 1, 2, 3, 4, 5, 6]
