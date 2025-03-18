from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from . import ToonHood
from toontown.safezone import RRHSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from . import SkyUtil
from direct.directnotify import DirectNotifyGlobal

class RRHHood(ToonHood.ToonHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('RRHHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ResistanceRangerHideout
        self.safeZoneLoaderClass = RRHSafeZoneLoader.RRHSafeZoneLoader
        self.storageDNAFile = 'phase_14/dna/storage_RRH.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: [],
         WACKY_WINTER_DECORATIONS: [],
         HALLOWEEN_PROPS: [],
         SPOOKY_PROPS: []}
        self.skyFile = 'phase_3.5/models/props/BR_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('RRHHood').addChild(self.fsm)
        self.fog = Fog('RRHHood')

    def unload(self):
        self.parentFSM.getStateNamed('RRHHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        self.fog = None

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)
        
    def setFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.4, 0.4, 0.4, 1))
            self.fog.setExpDensity(0.01)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()

    def startSky(self):
        self.sky.reparentTo(camera)
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)