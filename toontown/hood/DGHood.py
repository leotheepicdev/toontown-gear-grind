from . import DaylightHood
from toontown.town import DGTownLoader
from toontown.safezone import DGSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class DGHood(DaylightHood.DaylightHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        DaylightHood.DaylightHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DaisyGardens
        self.townLoaderClass = DGTownLoader.DGTownLoader
        self.safeZoneLoaderClass = DGSafeZoneLoader.DGSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_DG.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DG.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DG.dna'],
         HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_DG.dna'],
         SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_DG.dna']}
        self.titleColor = (0.8, 0.6, 1.0, 1.0)

    def load(self):
        DaylightHood.DaylightHood.load(self)
        self.parentFSM.getStateNamed('DGHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('DGHood').removeChild(self.fsm)
        DaylightHood.DaylightHood.unload(self)