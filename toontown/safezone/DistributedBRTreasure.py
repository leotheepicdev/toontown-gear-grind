from . import DistributedSZTreasure

class DistributedBRTreasure(DistributedSZTreasure.DistributedSZTreasure):

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/tbTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'

    def loadModel(self, modelPath, modelFindString=None):
        print(self.getVariant())
        modelFindString = 'flake%s' % str(self.getVariant() + 1)
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)