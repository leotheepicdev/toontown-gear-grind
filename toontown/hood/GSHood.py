from . import DaylightHood
from toontown.safezone import GSSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class GSHood(DaylightHood.DaylightHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        DaylightHood.DaylightHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = GoofySpeedway
        self.safeZoneLoaderClass = GSSafeZoneLoader.GSSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_GS.dna'
        self.holidayStorageDNADict = {HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_GS.dna'],
         SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_GS.dna'],
         CRASHED_LEADERBOARD: ['phase_6/dna/crashed_leaderboard_storage_GS.dna']}
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        DaylightHood.DaylightHood.load(self)
        self.parentFSM.getStateNamed('GSHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('GSHood').removeChild(self.fsm)
        DaylightHood.DaylightHood.unload(self)

    def enter(self, *args):
        DaylightHood.DaylightHood.enter(self, *args)
        base.localAvatar.chatMgr.chatInputSpeedChat.addKartRacingMenu()
        base.camLens.setNearFar(SpeedwayCameraNear, SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(DefaultCameraNear, DefaultCameraFar)
        base.localAvatar.chatMgr.chatInputSpeedChat.removeKartRacingMenu()
        DaylightHood.DaylightHood.exit(self)
