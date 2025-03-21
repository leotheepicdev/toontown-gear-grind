from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from .RewardPanel import *
from .BattleSounds import *
from . import MovieCamera
from direct.directnotify import DirectNotifyGlobal
from lib.libotp import NametagGlobals
import types
notify = DirectNotifyGlobal.directNotify.newCategory('MovieToonVictory')

def __findToonReward(rewards, toon):
    for r in rewards:
        if r['toon'] == toon:
            return r

    return None


class ToonVictorySkipper(DirectObject):

    def __init__(self, numToons, noSkip):
        self._numToons = numToons
        self._noSkip = noSkip
        self._startTimes = {}
        self._ivals = []
        self._battle = None

    def destroy(self):
        self._ivals = None

    def getSetupFunc(self, index):
        return Func(self._setupSkipListen, index)

    def getTeardownFunc(self, index):
        return Func(self._teardownSkipListen, index)

    def setBattle(self, battle):
        self._battle = battle

    def setStartTime(self, index, startT):
        self._startTimes[index] = startT

    def setIvals(self, ivals, timeOffset = 0.0):
        for index in self._startTimes:
            self._startTimes[index] += timeOffset

        self._ivals = ivals

    def _setupSkipListen(self, index):
        if not self._noSkip:
            func = Functor(self._skipToon, index)
            self.accept('escape', func)
            self.accept(RewardPanel.SkipBattleMovieEvent, func)

    def _teardownSkipListen(self, index):
        if not self._noSkip:
            self.ignore('escape')
            self.ignore(RewardPanel.SkipBattleMovieEvent)

    def _skipToon(self, index):
        nextIndex = index + 1
        if nextIndex >= self._numToons:
            for ival in self._ivals:
                ival.finish()

            if self._battle:
                self._battle.setSkippingRewardMovie()
        elif nextIndex in self._startTimes:
            for ival in self._ivals:
                ival.setT(self._startTimes[nextIndex])


def doToonVictory(localToonActive, toons, rewardToonIds, rewardDicts, deathList, rpanel, allowGroupShot = 1, helpfulToonsList = [], noSkip = False, mvp=0):
    track = Sequence()
    if localToonActive == 1:
        track.append(Func(rpanel.show))
        track.append(Func(NametagGlobals.setOnscreenChatForced, 1))
    camTrack = Sequence()
    endTrack = Sequence()
    danceSound = globalBattleSoundCache.getSound('ENC_Win.ogg')
    toonList = []
    toonId2toon = {}
    for t in toons:
        if isinstance(t, int):
            t = base.cr.doId2do.get(t)
        if t:
            toonList.append(t)
            toonId2toon[t.doId] = t

    rewardToonList = []
    for i in range(len(rewardToonIds)):
        tup = rewardToonIds[i]
        if type(tup) == int:
            tid = tup
        else:
            tid = tup[0]
        rewardToonList.append(toonId2toon.get(tid))

    skipper = ToonVictorySkipper(len(toonList), noSkip)
    lastListenIndex = 0
    track.append(skipper.getSetupFunc(lastListenIndex))
    for tIndex in range(len(toonList)):
        t = toonList[tIndex]
        rdict = __findToonReward(rewardDicts, t)
        if rdict != None:
            expTrack = rpanel.getExpTrack(t, rdict['origExp'], rdict['earnedExp'], deathList, rdict['origQuests'], rdict['items'], rdict['missedItems'], rdict['origMerits'], rdict['merits'], rdict['parts'], rdict['piggyAmount'], rdict['piggyMax'], rewardToonList, helpfulToonsList, noSkip=noSkip, mvp=mvp)
            if expTrack:
                skipper.setStartTime(tIndex, track.getDuration())
                track.append(skipper.getTeardownFunc(lastListenIndex))
                lastListenIndex = tIndex
                track.append(skipper.getSetupFunc(lastListenIndex))
                track.append(expTrack)
                camDuration = expTrack.getDuration()
                camExpTrack = MovieCamera.chooseRewardShot(t, camDuration)
                camTrack.append(MovieCamera.chooseRewardShot(t, camDuration, allowGroupShot=allowGroupShot))

    track.append(skipper.getTeardownFunc(lastListenIndex))
    track.append(Func(skipper.destroy))
    if localToonActive == 1:
        track.append(Func(rpanel.hide))
        track.append(Func(NametagGlobals.setOnscreenChatForced, 0))
    track.append(endTrack)
    trackdur = track.getDuration()
    soundTrack = SoundInterval(danceSound, duration=trackdur, loop=1)
    mtrack = Parallel(track, soundTrack)
    skipper.setIvals((mtrack, camTrack))
    return (mtrack, camTrack, skipper)
