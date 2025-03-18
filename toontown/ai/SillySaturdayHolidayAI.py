from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
from datetime import timedelta

from toontown.ai.HolidayBaseAI import HolidayBaseAI
from toontown.fishing.FishBingoManagerAI import FishBingoHolidayMgr
from toontown.racing.RaceManagerAI import CircuitRaceHolidayMgr
from toontown.minigame.TrolleyHolidayMgrAI import TrolleyHolidayMgrAI

forceSillyHoliday = None

class SillySaturdayHolidayMgrAI(HolidayBaseAI):
    """The master class for all the silly saturday events"""
    # bingo -> grand prix -> trolley tracks
    # 2 hours each
    holiday2class = {ToontownGlobals.SILLY_SATURDAY_BINGO: FishBingoHolidayMgr,
                     ToontownGlobals.SILLY_SATURDAY_CIRCUIT: CircuitRaceHolidayMgr,
                     ToontownGlobals.SILLY_SATURDAY_TROLLEY: TrolleyHolidayMgrAI}
    runningHoliday = None
    notify = directNotify.newCategory('SillySaturdayHolidayMgrAI')
    racingHolidays = (ToontownGlobals.CIRCUIT_RACING, ToontownGlobals.CIRCUIT_RACING_EVENT,
                      ToontownGlobals.SILLY_SATURDAY_CIRCUIT)

    def start(self):
        global forceSillyHoliday
        if forceSillyHoliday:
            self.doHoliday(forceSillyHoliday)
            forceSillyHoliday = None
        else:
            # calculate and start the correct holiday for the hour
            currentHour = self.air.toontownTimeManager.getCurServerDateTime().now(
                tz=self.air.toontownTimeManager.serverTimeZone).hour
            self.doHoliday(ToontownGlobals.SILLY_SATURDAY_BINGO + ((currentHour // 2) % 12) % 3)

    def stop(self):
        self.__stopHoliday()
        self.runningHoliday = None

    def doHoliday(self, holidayId):
        self.__startHoliday(doHolidayId=holidayId)

    def doNextHoliday(self, task=None):
        self.__startHoliday()

    def __getNextHoliday(self, holidayId=None):
        if holidayId and holidayId in self.holiday2class.keys():
            return holidayId, self.holiday2class[holidayId]
        if self.runningHoliday is None or self.runningHoliday.holidayId == ToontownGlobals.SILLY_SATURDAY_TROLLEY:
            return ToontownGlobals.SILLY_SATURDAY_BINGO, self.holiday2class[ToontownGlobals.SILLY_SATURDAY_BINGO]
        else:
            return self.runningHoliday.holidayId + 1, self.holiday2class[self.runningHoliday.holidayId + 1]

    def __stopHoliday(self):
        if self.runningHoliday is None:
            return
        taskMgr.remove('doNextSillySaturdayHoliday')
        self.runningHoliday.stop()
        if hasattr(self.air, 'newsManager') and hasattr(self.air, 'holidayManager'):
            if self.runningHoliday.holidayId in self.air.holidayManager.currentHolidays.keys():
                del self.air.holidayManager.currentHolidays[self.runningHoliday.holidayId]
            self.air.newsManager.d_setHolidayIdList(self.air.holidayManager.currentHolidays.keys())

    def __startHoliday(self, task=None, doHolidayId=None):
        if self.runningHoliday is not None:
            self.__stopHoliday()
        nextHoliday = self.__getNextHoliday(doHolidayId)
        self.runningHoliday = nextHoliday[1](self.air, nextHoliday[0])
        taskMgr.doMethodLater(1, self.__announceHoliday, 'announceNextSillyHoliday')

    def __announceHoliday(self, task):
        if self.runningHoliday is None:
            return
        self.runningHoliday.start()
        if hasattr(self.air, 'newsManager') and hasattr(self.air, 'holidayManager'):
            self.air.holidayManager.currentHolidays[self.runningHoliday.holidayId] = self.runningHoliday
            self.air.newsManager.d_setHolidayIdList(self.air.holidayManager.currentHolidays.keys())
        self.notify.debug('Current running holiday class: {}'.format(self.runningHoliday.__class__.__name__))

        # calculate next run in seconds
        now = self.air.toontownTimeManager.getCurServerDateTime().now(tz=self.air.toontownTimeManager.serverTimeZone)
        # oops, forgot to account for odd hours
        future = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=((now.hour // 2) % 2) + 1))

        next = (future - now).total_seconds()

        self.notify.debug('Next holiday run in {} seconds'.format(next))
        taskMgr.doMethodLater(next, self.doNextHoliday, 'doNextSillySaturdayHoliday')
