from . import TownLoader
from . import DGStreet
from toontown.suit import Suit

class DGTownLoader(TownLoader.TownLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = DGStreet.DGStreet
        self.musicFile = 'phase_8/audio/bgm/DG_SZ.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/DG_SZ.ogg'
        self.townStorageDNAFile = 'phase_8/dna/storage_DG_town.dna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        self.bird1Sound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bird_01.ogg')
        self.bird2Sound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bird_02.ogg')
        self.bird3Sound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bird_03.ogg')
        self.bird4Sound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bird_04.ogg')
        self.bird5Sound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bird_05.ogg')
        self.beeSound = base.loader.loadSfx('phase_8/audio/sfx/SZ_DG_bee.ogg')
        Suit.loadSuits(3)
        dnaFile = 'phase_8/dna/daisys_garden_' + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)

    def unload(self):
        del self.bird1Sound
        del self.bird2Sound
        del self.bird3Sound
        del self.bird4Sound
        del self.bird5Sound
        del self.beeSound
        Suit.unloadSuits(3)
        TownLoader.TownLoader.unload(self)

    def enter(self, requestStatus):
        TownLoader.TownLoader.enter(self, requestStatus)

    def exit(self):
        TownLoader.TownLoader.exit(self)
