from . import DistributedSZTreasure

class DistributedOZTreasure(DistributedSZTreasure.DistributedSZTreasure):
    SillySurgeHpHeight = 3

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/ozTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
