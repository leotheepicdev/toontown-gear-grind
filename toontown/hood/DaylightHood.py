from panda3d.core import *
from direct.interval.IntervalGlobal import *
from . import ToonHood
from .DaylightGlobals import *
from toontown.toonbase.ToontownGlobals import *
from . import SkyUtil
from direct.directnotify import DirectNotifyGlobal
import time

class DaylightHood(ToonHood.ToonHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('DaylightHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.nightSkyFile = 'phase_8/models/props/DL_sky'
        self.dawnSkyFile = 'phase_6/models/props/MM_sky'
        self.daySkyFile = 'phase_3.5/models/props/TT_sky'
        self.nightSky = None
        self.dawnSky = None
        self.daySky = None
        self.nightColor = Vec4(0.3, 0.3, 0.5, 1)
        self.duskColor = Vec4(0.8, 0.4, 0.7, 1)
        self.dawnColor = Vec4(1, 0.8, 0.4, 1)
        self.dayColor = Vec4(1, 1, 1, 1)
        self.seq = None

    def load(self):
        if self.storageDNAFile:
            loader.loadDNAFile(self.dnaStore, self.storageDNAFile)
        self.nightSky = loader.loadModel(self.nightSkyFile)
        self.nightSky.setScale(0.8)
        self.nightSky.setTransparency(1)
        self.nightSky.setBin('background', 102)
        self.dawnSky = loader.loadModel(self.dawnSkyFile)
        self.dawnSky.setScale(0.8)
        self.dawnSky.setTransparency(1)
        self.dawnSky.setBin('background', 102)
        self.daySky = loader.loadModel(self.daySkyFile)
        self.daySky.setTransparency(1)
        self.daySky.setBin('background', 100)
        self.accept('daylightSettingsChange', self.adjustSky)
            
    def unload(self):
        if hasattr(self, 'loader'):
            self.notify.info('Aggressively cleaning up loader: %s' % self.loader)
            self.loader.exit()
            self.loader.unload()
            del self.loader
        del self.fsm
        del self.parentFSM
        self.dnaStore.resetHood()
        del self.dnaStore
        for sky in (self.nightSky, self.dawnSky, self.daySky):
            sky.removeNode()
            del sky
        if self.seq:
            self.seq.pause()
            del self.seq
            self.seq = None
            render.setColorScale(1, 1, 1, 1)
        self.ignoreAll()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def skyTrack(self, task):
        return None
        
    def startDefaultSky(self):
        self.daySky.setColorScale(1, 1, 1, 1)
        self.dawnSky.setColorScale(1, 1, 1, 0)
        self.nightSky.setColorScale(1, 1, 1, 0)

    def startSky(self):
        for sky in (self.nightSky, self.dawnSky, self.daySky):
            sky.reparentTo(camera)
            sky.setZ(0)
            sky.setHpr(0, 0, 0)
            ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
            sky.node().setEffect(ce)
            sky.setDepthTest(0)
            sky.setDepthWrite(0)
            
        self.startDefaultSky()
        render.setColorScale(1, 1, 1, 1)

        if Settings['wantDaylight']:
            if base.cr.daylightManager:
                base.cr.daylightManager.d_requestTime()
            
    def adjustSky(self):
        if Settings['wantDaylight']:
            if base.cr.daylightManager:
                base.cr.daylightManager.d_requestTime()
        else:
            if self.seq:
                self.seq.pause()
                del self.seq
                self.seq = None
                self.transitionToMorning()
            self.startDefaultSky()
            render.setColorScale(1, 1, 1, 1)
    
    def stopSky(self):
        for sky in (self.nightSky, self.dawnSky, self.daySky):
            sky.reparentTo(hidden)
        if self.seq:
            self.seq.pause()
            del self.seq
            self.seq = None
        render.setColorScale(1, 1, 1, 1)

    def startSpookySky(self):
        return
        if hasattr(self, 'sky') and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag('sky', 'Halloween')
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5, 0.5, 0.5, 1)
        self.sky.setBin('background', 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval(1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0.25), blendType='easeInOut')
        fadeIn.start()
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        
    def transitionToMorning(self):
        try:
            geom = base.cr.playGame.getPlace().loader.geom
            lights = geom.findAllMatches('**/*light*')
            lights += geom.findAllMatches('**/*lamp*')
            for light in lights:
                light.setColorScaleOff(0)
        except:
            pass
       
    def transitionToDarkness(self):
        try:
            geom = base.cr.playGame.getPlace().loader.geom
            lights = geom.findAllMatches('**/*light*')
            lights += geom.findAllMatches('**/*lamp*')
            for light in lights:
                light.setColorScaleOff(1)
        except:
            pass
            
    def restartSequence(self):
        try:
            self.seq.finish()
            self.seq.start()
        except:
            self.seq = None
        
    def adjustDaylight(self, elaspedTime, serverTime):
        clientTime = time.time()
        timeAdjust = clientTime - serverTime
        elaspedTime += timeAdjust
        self.seq = Sequence(
                       Parallel(
                         LerpColorScaleInterval(self.daySky, DAY_TIME, Vec4(0, 0, 0, 0)),
                         LerpColorScaleInterval(self.dawnSky, DAY_TIME, Vec4(1, 1, 1, 1)),
                         LerpColorScaleInterval(render, DAY_TIME, self.duskColor),
                         Wait(DAY_TIME),
                       ),
                       Parallel(
                         LerpColorScaleInterval(self.dawnSky, DUSK_TIME, Vec4(0, 0, 0, 0)),
                         LerpColorScaleInterval(self.nightSky, DUSK_TIME, Vec4(1, 1, 1, 1)),
                         LerpColorScaleInterval(render, DUSK_TIME, self.nightColor),
                         Wait(DUSK_TIME),
                         Sequence(Wait(NIGHT_TIME_TRANSITION_WAIT), Func(self.transitionToDarkness))
                       ),
                       Parallel(
                         LerpColorScaleInterval(self.nightSky, NIGHT_TIME, Vec4(0, 0, 0, 0)),
                         LerpColorScaleInterval(self.dawnSky, NIGHT_TIME, Vec4(1, 1, 1, 1)),
                         LerpColorScaleInterval(render, NIGHT_TIME, self.dawnColor),
                         Wait(NIGHT_TIME),
                       ),
                       Parallel(
                         LerpColorScaleInterval(self.dawnSky, DAWN_TIME, Vec4(0, 0, 0, 0)),
                         LerpColorScaleInterval(self.daySky, DAWN_TIME, Vec4(1, 1, 1, 1)),
                         LerpColorScaleInterval(render, DAWN_TIME, self.dayColor),
                         Wait(DAWN_TIME),
                         Sequence(Wait(MORNING_TIME_TRANSITION_WAIT), Func(self.transitionToMorning))
                       ),
                       Func(self.restartSequence)
                   )
        try:
            self.seq.start(elaspedTime)
        except:
            self.notify.warning('Woah! The daylight sequence failed! Defaulting to server sequence time...')
            self.seq.start(elaspedTime - timeAdjust)
                       

