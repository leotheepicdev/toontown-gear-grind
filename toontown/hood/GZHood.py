from . import DaylightHood
from toontown.safezone import GZSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class GZHood(DaylightHood.DaylightHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        DaylightHood.DaylightHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = GolfZone
        self.safeZoneLoaderClass = GZSafeZoneLoader.GZSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_GZ.dna'
        self.holidayStorageDNADict = {HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_GZ.dna'],
         SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_GZ.dna']}
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        DaylightHood.DaylightHood.load(self)
        self.parentFSM.getStateNamed('GZHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('GZHood').removeChild(self.fsm)
        DaylightHood.DaylightHood.unload(self)

    def enter(self, *args):
        DaylightHood.DaylightHood.enter(self, *args)
        base.localAvatar.chatMgr.chatInputSpeedChat.addGolfMenu()
        base.camLens.setNearFar(SpeedwayCameraNear, SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(DefaultCameraNear, DefaultCameraFar)
        base.localAvatar.chatMgr.chatInputSpeedChat.removeGolfMenu()
        DaylightHood.DaylightHood.exit(self)
