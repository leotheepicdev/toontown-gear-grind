from . import DistributedSZTreasure

class DistributedDGTreasure(DistributedSZTreasure.DistributedSZTreasure):
    WHITE = 0
    ORANGE = 1
    YELLOW = 2
    PINK = 3

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/dgTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        
    def loadModel(self, modelPath, modelFindString=None):
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)
        
        if self.getVariant() == self.ORANGE:
            self.treasure.find('**/pedals').setColorScale(0.975, 0.382, 0, 1)
        elif self.getVariant() == self.YELLOW:
            self.treasure.find('**/pedals').setColorScale(1, 1, 0, 1)
        elif self.getVariant() == self.PINK:
            self.treasure.find('**/pedals').setColorScale(0.85, 0.61, 0.75, 1)
