from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from . import DaylightHood
from toontown.town import TTTownLoader
from toontown.safezone import TTSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from . import SkyUtil
from direct.directnotify import DirectNotifyGlobal

class TTHood(DaylightHood.DaylightHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        DaylightHood.DaylightHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownCentral
        self.townLoaderClass = TTTownLoader.TTTownLoader
        self.safeZoneLoaderClass = TTSafeZoneLoader.TTSafeZoneLoader
        self.storageDNAFile = 'phase_4/dna/storage_TT.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.dna', 'phase_4/dna/winter_storage_TT_sz.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.dna', 'phase_4/dna/winter_storage_TT_sz.dna'],
         HALLOWEEN_PROPS: ['phase_4/dna/halloween_props_storage_TT.dna', 'phase_4/dna/halloween_props_storage_TT_sz.dna'],
         SPOOKY_PROPS: ['phase_4/dna/halloween_props_storage_TT.dna', 'phase_4/dna/halloween_props_storage_TT_sz.dna']}
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        DaylightHood.DaylightHood.load(self)
        self.parentFSM.getStateNamed('TTHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('TTHood').removeChild(self.fsm)
        DaylightHood.DaylightHood.unload(self)

    def enter(self, *args):
        DaylightHood.DaylightHood.enter(self, *args)

    def exit(self):
        DaylightHood.DaylightHood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)
