import random
from panda3d.core import VBase3, Point3, Vec4
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, Track, SoundInterval, LerpColorScaleInterval
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import DistributedBattleFinal, DistributedBattleWaiters, SuitBattleGlobals
from lib.libotp._constants import CFSpeech, CFTimeout
from toontown.suit import SuitTimings
from toontown.toonbase import ToontownGlobals

class DistributedBattleVirtuals(DistributedBattleWaiters.DistributedBattleWaiters):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleVirtuals')

    def announceGenerate(self):
        DistributedBattleFinal.DistributedBattleFinal.announceGenerate(self)

    def doInitialFlyDown(self):
        self.showSuitsFalling(self.suits, 0, self.uniqueName('initial-FlyDown'), self.flyDownDone)
        
    def flyDownDone(self):
        self.notify.info('flyDownDone')

    def showSuitsFalling(self, suits, ts, name, callback):
        if self.bossCog == None:
            return
        suitTrack = Parallel()
        delay = 0
        failSound = loader.loadSfx('phase_11/audio/sfx/LB_laser_beam_on_2.ogg')
        soundTrack = SoundInterval(failSound, volume=0.8)
        suitTrack.append(soundTrack)
        for suit in suits:
            suit.setState('Battle')
            if suit.dna.dept == 'l':
                suit.reparentTo(self.bossCog)
                suit.setPos(0, 0, 0)
            if suit in self.joiningSuits:
                i = len(self.pendingSuits) + self.joiningSuits.index(suit)
                destPos, h = self.suitPendingPoints[i]
                destHpr = VBase3(h, 0, 0)
            else:
                destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            suit.reparentTo(hidden)
            suit.setPos(destPos)
            suit.headsUp(self)
            
            suitTrack.append(Sequence(Parallel(Sequence(Func(suit.reparentTo, self), Parallel(soundTrack, suit.scaleInterval(0.6, (1, 1, 1), startScale=(0.01, 0.01, 0.01), blendType='easeIn')))), Func(suit.loop, 'neutral')))

        if self.hasLocalToon():
            base.camera.reparentTo(self)
            if random.choice([0, 1]):
                base.camera.setPosHpr(20, -4, 7, 60, 0, 0)
            else:
                base.camera.setPosHpr(-20, -4, 7, -60, 0, 0)
        done = Func(callback)
        track = Sequence(suitTrack, done, name=name)
        track.start(ts)
        self.storeInterval(track, name)