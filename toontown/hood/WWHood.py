from panda3d.core import *
from direct.interval.IntervalGlobal import *
from . import ToonHood
from toontown.safezone import WWSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from toontown.town import WWTownLoader
from direct.directnotify import DirectNotifyGlobal

class WWHood(ToonHood.ToonHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('WWHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = WackyWest
        self.townLoaderClass = WWTownLoader.WWTownLoader
        self.safeZoneLoaderClass = WWSafeZoneLoader.WWSafeZoneLoader
        self.storageDNAFile = 'phase_14/dna/storage_WW.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: [],
         WACKY_WINTER_DECORATIONS: [],
         HALLOWEEN_PROPS: [],
         SPOOKY_PROPS: []}
        self.skyFile = 'phase_14/models/props/WackyWestSky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.47, 0.36, 0.33, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('WWHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('WWHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        
    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)
        base.camLens.setNearFar(WackyWestCameraNear, WackyWestCameraFar)

    def exit(self):
        base.camLens.setNearFar(DefaultCameraNear, DefaultCameraFar)
        ToonHood.ToonHood.exit(self)
 
    def startSky(self):
        self.sky.reparentTo(camera)
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setBin('background', 100)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)