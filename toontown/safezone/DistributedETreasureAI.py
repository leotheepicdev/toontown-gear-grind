from . import DistributedSZTreasureAI

class DistributedETreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        self.variations = [0, 1, 2, 3, 4, 5, 6]
