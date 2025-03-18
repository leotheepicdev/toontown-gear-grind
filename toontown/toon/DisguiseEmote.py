from . import Toon, ToonDNA
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.showbase import PythonUtil
from panda3d.core import *
from otp.avatar import Emote
from direct.directnotify import DirectNotifyGlobal
from lib.libotp._constants import CFSpeech, CFTimeout, CFThought
EmoteSleepIndex = 4
EmoteClear = -1

def returnToLastAnim(toon):
    try:
        suit = toon.suit
    except:
        return

    if hasattr(toon, 'playingAnim') and toon.playingAnim:
        if toon.playingAnim == 'neutral':
            suit.loop('neutral')
        else:
            rightHand = suit.rightHand
            numChildren = rightHand.getNumChildren()
            if numChildren > 0:
                anim = 'tray-' + anim
                if anim == 'tray-run':
                    anim = 'tray-walk'
                self.suit.stop()
                self.suit.loop(anim)
    else:
        suit.loop('neutral')

def doVictory(suit, volume = 1):
    duration = suit.getDuration('victory')
    track = Sequence(Func(suit.play, 'victory'))
    return (track, duration, None)
    
def doSidestepLeft(suit, volume = 1):
    duration = suit.getDuration('sidestep-left')
    track = Sequence(Func(suit.play, 'sidestep-left'))
    return (track, duration, None)
    
def doSidestepRight(suit, volume = 1):
    duration = suit.getDuration('sidestep-right')
    track = Sequence(Func(suit.play, 'sidestep-right'))
    return (track, duration, None)
    
def doFlail(suit, volume = 1):
    duration = suit.getDuration('flail')
    track = Sequence(Func(suit.play, 'flail'))
    return (track, duration, None)

def doSlipBackward(suit, volume = 1):
    duration = suit.getDuration('slip-backward')
    track = Sequence(Func(suit.play, 'slip-backward'))
    return (track, duration, None)
    
def doSlipForward(suit, volume = 1):
    duration = suit.getDuration('slip-forward')
    track = Sequence(Func(suit.play, 'slip-forward'))
    return (track, duration, None)
    
def doHypnotized(suit, volume = 1):
    duration = suit.getDuration('hypnotized')
    track = Sequence(Func(suit.play, 'hypnotized'))
    return (track, duration, None)

EmoteFunc = [[doVictory, 0],
 [doSidestepLeft, 0],
 [doSidestepRight, 0],
 [doFlail, 0],
 [doSlipBackward, 0],
 [doSlipForward, 0],
 [doHypnotized, 0],
]

class DisguiseEmote(Emote.Emote):
    notify = DirectNotifyGlobal.directNotify.newCategory('DisguiseEmote')
    EmoteEnableStateChanged = 'DisguiseEmoteEnableStateChanged'
    SLEEP_INDEX = 4

    def __init__(self):
        self.emoteFunc = EmoteFunc
        self.bodyEmotes = [0,
        1,
        2,
        3,
        4,
        5,
        6]
        if len(self.emoteFunc) != len(OTPLocalizer.DisguiseEmoteList):
            self.notify.error('Emote.EmoteFunc and OTPLocalizer.DisguiseEmoteList are different lengths.')
        self.track = None
        self.stateChangeMsgLocks = 0
        self.stateHasChanged = 0

    def lockStateChangeMsg(self):
        self.stateChangeMsgLocks += 1

    def unlockStateChangeMsg(self):
        if self.stateChangeMsgLocks <= 0:
            print(PythonUtil.lineTag() + ': someone unlocked too many times')
            return
        self.stateChangeMsgLocks -= 1
        if self.stateChangeMsgLocks == 0 and self.stateHasChanged:
            messenger.send(self.EmoteEnableStateChanged)
            self.stateHasChanged = 0

    def emoteEnableStateChanged(self):
        if self.stateChangeMsgLocks > 0:
            self.stateHasChanged = 1
        else:
            messenger.send(self.EmoteEnableStateChanged)

    def disableAll(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        if not toon.isDisguised:
            return
        self.disableGroup(list(range(len(self.emoteFunc))), toon)

    def releaseAll(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        self.enableGroup(list(range(len(self.emoteFunc))), toon)

    def disableBody(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        if not toon.isDisguised:
            return
        self.disableGroup(self.bodyEmotes, toon)

    def releaseBody(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        if not toon.isDisguised:
            return
        self.enableGroup(self.bodyEmotes, toon)

    def disableGroup(self, indices, toon):
        if not toon.isDisguised:
            return
        self.lockStateChangeMsg()
        for i in indices:
            self.disable(i, toon)

        self.unlockStateChangeMsg()

    def enableGroup(self, indices, toon):
        self.lockStateChangeMsg()
        for i in indices:
            self.enable(i, toon)

        self.unlockStateChangeMsg()

    def disable(self, index, toon):
        if isinstance(index, str):
            index = OTPLocalizer.EmoteFuncDict[index]
        self.emoteFunc[index][1] = self.emoteFunc[index][1] + 1
        if toon is base.localAvatar:
            if self.emoteFunc[index][1] == 1:
                self.emoteEnableStateChanged()

    def enable(self, index, toon):
        if isinstance(index, str):
            index = OTPLocalizer.EmoteFuncDict[index]
        self.emoteFunc[index][1] = self.emoteFunc[index][1] - 1
        if toon is base.localAvatar:
            if self.emoteFunc[index][1] == 0:
                self.emoteEnableStateChanged()

    def doEmote(self, toon, emoteIndex, ts = 0, volume = 1):
        if not toon.isDisguised:
            return
            
        suit = toon.suit
    
        try:
            func = self.emoteFunc[emoteIndex][0]
        except:
            print('Error in finding emote func %s' % emoteIndex)
            return (None, None)

        def clearEmoteTrack():
            base.localAvatar.emoteTrack = None
            base.localAvatar.d_setDisguiseEmoteState(self.EmoteClear, 1.0)
            return

        if volume == 1:
            track, duration, exitTrack = func(suit)
        else:
            track, duration, exitTrack = func(suit, volume)
        if track != None:
            track = Sequence(Func(self.disableAll, toon, 'doEmote'), track)
            if duration > 0:
                track = Sequence(track, Wait(duration))
            if exitTrack != None:
                track = Sequence(track, exitTrack)
            if duration > 0:
                track = Sequence(track, Func(returnToLastAnim, toon))
            track = Sequence(track, Func(self.releaseAll, toon, 'doEmote'), autoFinish=1)
            if toon.isLocal():
                track = Sequence(track, Func(clearEmoteTrack))
        if track != None:
            if toon.disguiseEmote != None:
                toon.disguiseEmote.finish()
                toon.disguiseEmote = None
            toon.disguiseEmote = track
            track.start(ts)
        del clearEmoteTrack
        return (track, duration)

    def printEmoteState(self, action, msg):
        pass


Emote.globalDisguiseEmote = DisguiseEmote()
