from . import DistributedSZTreasure

class DistributedDLTreasure(DistributedSZTreasure.DistributedSZTreasure):
    SillySurgeHpHeight = 2.5

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'phase_4/models/props/ddlTreasure'
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'