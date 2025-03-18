from panda3d.core import *
from . import DaylightHood
from toontown.safezone import OZSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from toontown.racing import DistributedVehicle
from . import SkyUtil

class OZHood(DaylightHood.DaylightHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        DaylightHood.DaylightHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = OutdoorZone
        self.safeZoneLoaderClass = OZSafeZoneLoader.OZSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_OZ.dna'
        self.holidayStorageDNADict = {HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_OZ.dna'],
         SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_OZ.dna']}
        self.titleColor = (1.0, 0.5, 0.4, 1.0)
        self.whiteFogColor = Vec4(0.95, 0.95, 0.95, 1)
        self.underwaterFogColor = Vec4(0.0, 0.0, 0.6, 1.0)

    def load(self):
        DaylightHood.DaylightHood.load(self)
        self.parentFSM.getStateNamed('OZHood').addChild(self.fsm)
        self.fog = Fog('OZFog')

    def unload(self):
        self.parentFSM.getStateNamed('OZHood').removeChild(self.fsm)
        DaylightHood.DaylightHood.unload(self)

    def enter(self, *args):
        DaylightHood.DaylightHood.enter(self, *args)
        base.camLens.setNearFar(SpeedwayCameraNear, SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(DefaultCameraNear, DefaultCameraFar)
        DaylightHood.DaylightHood.exit(self)

    def setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(self.underwaterFogColor)
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            self.daySky.setFog(self.fog)
            self.dawnSky.setFog(self.fog)
            self.nightSky.setFog(self.fog)

    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(0.0, 400.0)
            render.clearFog()
            render.setFog(self.fog)
            for sky in (self.daySky, self.dawnSky, self.nightSky):
                sky.clearFog()
                sky.setFog(self.fog)

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            for sky in (self.daySky, self.dawnSky, self.nightSky):
                sky.clearFog()
