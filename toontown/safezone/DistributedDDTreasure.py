from . import DistributedSZTreasure

class DistributedDDTreasure(DistributedSZTreasure.DistributedSZTreasure):
    ORANGE = 1
    PINK = 2

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/ddTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        
    def loadModel(self, modelPath, modelFindString=None):
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)
        
        if self.getVariant() == self.ORANGE:
            self.treasure.setTexture(loader.loadTexture('phase_4/maps/starfish_orange.png'), 1)
        elif self.getVariant() == self.PINK:
            self.treasure.setTexture(loader.loadTexture('phase_4/maps/starfish_pink.png'), 1)
