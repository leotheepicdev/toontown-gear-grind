from . import DistributedSZTreasure

class DistributedETreasure(DistributedSZTreasure.DistributedSZTreasure):
    GREEN = 0
    PURPLE = 1
    RED = 2
    BLUE = 3
    YELLOW = 4
    ORANGE = 5
    PINK = 6

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/estateTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        
    def loadModel(self, modelPath, modelFindString=None):
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)
        
        if self.getVariant() == self.GREEN:
            self.treasure.find('**/popsicle').setColorScale(0.54901960784, 1, 0.61176470588, 1)
        elif self.getVariant() == self.PURPLE:
            self.treasure.find('**/popsicle').setColorScale(0.628, 0.095, 0.99, 1)
        elif self.getVariant() == self.RED:
            self.treasure.find('**/popsicle').setColorScale(0.97, 0.051, 0.101, 1)
        elif self.getVariant() == self.BLUE:
            self.treasure.find('**/popsicle').setColorScale(0.1725490196, 0.50980392156, 0.78823529411, 1)
        elif self.getVariant() == self.YELLOW:
            self.treasure.find('**/popsicle').setColorScale(0.97, 0.792, 0.094, 1)
        elif self.getVariant() == self.ORANGE:
            self.treasure.find('**/popsicle').setColorScale(0.97, 0.58, 0.0235, 1)
        elif self.getVariant() == self.PINK:
            self.treasure.find('**/popsicle').setColorScale(1, 0.41, 0.705, 1)
