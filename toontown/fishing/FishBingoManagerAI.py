from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from direct.distributed import ClockDelta

from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from . DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from . import BingoGlobals
from toontown.ai.HolidayBaseAI import HolidayBaseAI

import random, time, datetime

class FishBingoManagerAI:
    notify = directNotify.newCategory("FishBingoManagerAI")

    def __init__(self, air):
        self.air = air

        # Defaults:
        self.running = False

        # Dictionaries:
        self.zoneToPondBingoMgrs = {}

        # Defaults:
        self.intermissionTask = None
        self.intermission = 0
        self.blockoutTask = None
        self.blockout = False
        self.blockoutJackpot = BingoGlobals.MIN_SUPER_JACKPOT
        self.blockoutWin = False
        self.blockoutTimeout = None

    def createBingoManagers(self):
        for do in list(self.air.doId2do.values()):
            if isinstance(do, DistributedFishingPondAI):
                self.newFishingPond(do)

    def newFishingPond(self, pond):
        if pond.zoneId not in self.zoneToPondBingoMgrs:
            bingoMgr = DistributedPondBingoManagerAI(self.air)
            bingoMgr.setPond(pond)
            bingoMgr.generateWithRequired(pond.zoneId)
            bingoMgr.start()
            self.zoneToPondBingoMgrs[pond.zoneId] = bingoMgr

    def start(self):
        self.running = True
        self.createBingoManagers()
        self.startIntermissionTask()
        self.air.newsManager.bingoStart()

    def stop(self):
        self.running = False
        if self.intermissionTask:
            taskMgr.remove(self.intermissionTask)
            self.intermissionTask = None
        if not self.blockout and not self.intermission:
            # If we're not doing a intermission/blockout bingo
            # (i.e. holiday ended early), send the end notification.
            self.air.newsManager.bingoEnd()

    def getSecondsTillIntermission(self):
        hourContext = -1
        secondsUntilIntermission = 0
        while not secondsUntilIntermission:
            hourContext += 1
            currentTime = self.air.toontownTimeManager.getCurServerDateTime().now(
                tz=self.air.toontownTimeManager.serverTimeZone)

            # There should be a better way of doing this... Sheesh...
            if currentTime.hour == 23 and currentTime.minute in range(BingoGlobals.HOUR_BREAK_MIN - 1, BingoGlobals.HOUR_BREAK_MIN + 2):
                # Set the current time to tomorrow.
                currentTime += datetime.timedelta(1)

            laterTime = datetime.datetime(year = currentTime.year, month = currentTime.month, day = currentTime.day, hour = (currentTime.hour + hourContext) % 24, minute = BingoGlobals.HOUR_BREAK_MIN, second = 0, tzinfo = self.air.toontownTimeManager.serverTimeZone)
            secondsUntilIntermission = (laterTime - self.air.toontownTimeManager.getCurServerDateTime().now(tz = self.air.toontownTimeManager.serverTimeZone)).seconds

        self.notify.debug('getSecondsTillIntermission: {}'.format(secondsUntilIntermission))
        return secondsUntilIntermission

    def startIntermissionTask(self):
        self.intermissionTask = taskMgr.doMethodLater(self.getSecondsTillIntermission(), self.doIntermission, 'intermission')

    def doIntermission(self, task):
        # It's intermission time, folks!  Rise and stretch time!
        self.notify.debug('Starting intermission')
        self.intermission = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.blockoutTask = taskMgr.doMethodLater(BingoGlobals.HOUR_BREAK_SESSION, self.doBlockout, 'blockout')

        # Start the task again.
        task.delayTime = self.getSecondsTillIntermission()
        return task.again

    def doBlockout(self, task):
        # It's time for Blockout Bingo!
        self.notify.debug('Starting blockout')
        self.intermission = 0

        # Tell all their pond managers to pick up the blockout card.
        for bingoMgr in self.zoneToPondBingoMgrs.values():
            bingoMgr.getNewBingoCard(blockout = True)
            bingoMgr.b_setJackpot(self.blockoutJackpot)

        self.blockout = True
        self.blockoutTask = None

        timeoutTime = BingoGlobals.TIMEOUT_SESSION + BingoGlobals.getGameTime(BingoGlobals.BLOCKOUT_CARD) + BingoGlobals.REWARD_TIMEOUT
        self.blockoutTimeout = taskMgr.doMethodLater(timeoutTime, self.finishBlockout, 'blockoutTimeout')

        return task.done

    def handleBlockoutWin(self, winningBingoMgr):
        if not self.blockout:
            self.notify.warning('handleBlockoutWin called without blockout bingo in progress!')
            return

        self.blockoutWin = True

        # Tell the other managers that the game is over.
        for bingoMgr in self.zoneToPondBingoMgrs.values():
            if bingoMgr == winningBingoMgr:
                continue
            bingoMgr.b_setState('GameOver')

        if self.blockoutTimeout:
            taskMgr.remove(self.blockoutTimeout)
            self.blockoutTimeout = None

        taskMgr.doMethodLater(BingoGlobals.REWARD_TIMEOUT, self.finishBlockout, 'blockoutWin')

    def finishBlockout(self, task):
        self.blockout = False

        if self.blockoutTimeout:
            self.blockoutTimeout = None

        if self.running:
            # We're still up and running.
            if not self.blockoutWin:
                # Rollover the jackpot amount.
                self.blockoutJackpot += BingoGlobals.ROLLOVER_AMOUNT
                # Ensure that it doesn't overflow.
                self.blockoutJackpot = min(self.blockoutJackpot, BingoGlobals.MAX_SUPER_JACKPOT)
            else:
                # Reset the jackpot back to the minimum value.
                self.blockoutJackpot = BingoGlobals.MIN_SUPER_JACKPOT
                self.blockoutWin = False
        else:
            # Time to close up shop.  Send the end notification.
            self.air.newsManager.bingoEnd()
            # And reset the jackpot back to the minimum value.
            self.blockoutJackpot = BingoGlobals.MIN_SUPER_JACKPOT

        return task.done

    def closeBingoMgr(self, bingoMgr):
        bingoMgr.pond.bingoMgr = None
        bingoMgr.requestDelete()
        if bingoMgr.zoneId in self.zoneToPondBingoMgrs:
            del self.zoneToPondBingoMgrs[bingoMgr.zoneId]

class FishBingoHolidayMgr(HolidayBaseAI):
    notify = directNotify.newCategory("FishBingoHolidayMgr")

    def __init__(self, air, holidayId):
        HolidayBaseAI.__init__(self, air, holidayId)

    def start(self):
        self.air.fishBingoManager.start()

    def stop(self):
        self.air.fishBingoManager.stop()
