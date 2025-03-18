from direct.interval.IntervalGlobal import *
from .BattleBase import *
from .BattleSounds import *
from . import MovieCamera
from direct.directnotify import DirectNotifyGlobal
from . import MovieUtil
from . import MovieNPCSOS
notify = DirectNotifyGlobal.directNotify.newCategory('MovieTaunt')

def doTaunts(taunts):
    if len(taunts) == 0:
        return (None, None)
    npcArrivals, npcDepartures, npcs = MovieNPCSOS.doNPCTeleports(taunts)
    mtrack = Parallel()
    suitTrack = Parallel()
    for t in taunts:
        ival = doTauntMovie(t, npcs)
        if ival:
            mtrack.append(ival)
    targets = taunts[0]['target']
    for target in targets:
        suit = target['suit']
        suitTrack.append(MovieUtil.createSuitTauntMultiTrack(suit, 1))
    mtrack.append(suitTrack)

    lureTrack = Sequence(npcArrivals, mtrack, npcDepartures)
    camDuration = mtrack.getDuration()
    enterDuration = npcArrivals.getDuration()
    exitDuration = npcDepartures.getDuration()
    camTrack = MovieCamera.chooseLureShot(taunts, camDuration, enterDuration, exitDuration)
    return (lureTrack, camTrack)

def doTauntMovie(taunt, npcs):
    toon = taunt['toon']
    target = taunt['target']
    toonTrack = Sequence(Func(toon.angryEyes), Func(toon.blinkEyes), ActorInterval(toon, 'taunt'), Func(toon.normalEyes), Func(toon.blinkEyes), Func(toon.loop, 'neutral'))
    taunt = loader.loadSfx('phase_4/audio/sfx/avatar_battle_taunt.ogg')
    soundTrack = Sequence(Wait(0.01), SoundInterval(taunt, node=toon))
    return Parallel(toonTrack, soundTrack)