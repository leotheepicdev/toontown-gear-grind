from . import TownLoader
from . import WWStreet
from toontown.suit import Suit

class WWTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = WWStreet.WWStreet
        self.musicFile = 'phase_14/audio/bgm/WW_SZ.ogg'
        self.activityMusicFile = 'phase_14/audio/bgm/WW_SZ_activity.ogg'
        self.townStorageDNAFile = 'phase_14/dna/storage_WW_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        dnaFile = 'phase_14/dna/wacky_west_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)
