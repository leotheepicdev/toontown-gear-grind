from . import DistributedSZTreasure

class DistributedTTTreasure(DistributedSZTreasure.DistributedSZTreasure):
    VANILLA = 0
    CHOCOLATE = 1
    STRAWBERRY = 2
    MINT = 3

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/ttcTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        
    def loadModel(self, modelPath, modelFindString=None):
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)
        
        if self.getVariant() == self.CHOCOLATE:
            self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce1.png'), 1)
            self.treasure.find('**/cone').setTexture(loader.loadTexture('phase_4/maps/chocolate_cone.png'), 1)
        elif self.getVariant() == self.STRAWBERRY:
            self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce2.png'), 1)
        elif self.getVariant() == self.MINT:
            self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce3.png'), 1)