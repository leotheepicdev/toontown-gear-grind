from . import SafeZoneLoader
from . import WWPlayground

class WWSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = WWPlayground.WWPlayground
        self.musicFile = 'phase_14/audio/bgm/WW_nbrhood.ogg'
        self.activityMusicFile = 'phase_14/audio/bgm/WW_SZ_activity.ogg'
        self.dnaFile = 'phase_14/dna/wacky_west_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_14/dna/storage_WW_sz.dna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)
