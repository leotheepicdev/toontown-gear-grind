from . HolidayBaseAI import HolidayBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.ai import DistributedSillyMeterMgrAI
from toontown.toonbase import ToontownGlobals
from datetime import datetime, timedelta

class SillyMeterHolidayAI(HolidayBaseAI):
    notify = directNotify.newCategory('SillyMeterHolidayAI')

    def __init__(self, air, holidayId):
        HolidayBaseAI.__init__(self, air, holidayId)
        self.sillyMeterMgr = None
        return

    def start(self):
        HolidayBaseAI.start(self)
        self.sillyMeterMgr = DistributedSillyMeterMgrAI.DistributedSillyMeterMgrAI(self.air, True, 0, 0, [])
        self.sillyMeterMgr.generateWithRequired(ToontownGlobals.ToonHall)
        taskMgr.add(self.checkPhase, 'checkPhase')

    def checkPhase(self, task):
        currentTime = self.air.toontownTimeManager.getCurServerDateTime().now(tz=self.air.toontownTimeManager.serverTimeZone)
        year = datetime.now().year
        holidayDates = []
        month = 3
        day = 22
        for x in range(16):
            if x == 8:
                month = 4
                day = 0
            day += 1
            date = (year, month, day, 0, 0, 0)
            holidayDates.append(date)

        holidayDates.append((year, 4, 12))
        curPhase = 0
        for x in range(16):
            date = holidayDates[x]
            nextDate = holidayDates[(x + 1)]
            startDate = datetime(year=year, month=date[1], day=date[2], hour=0, minute=0, second=0, tzinfo=self.air.toontownTimeManager.serverTimeZone)
            endDate = datetime(year=year, month=nextDate[1], day=nextDate[2], hour=0, minute=0, second=0, tzinfo=self.air.toontownTimeManager.serverTimeZone)
            if currentTime > startDate:
                if currentTime > endDate:
                    continue
                else:
                    curPhase = x
                    break

        del holidayDates[-1]
        numPhases = len(holidayDates)
        self.sillyMeterMgr.b_setNumPhases(numPhases)
        self.sillyMeterMgr.b_setCurPhase(curPhase)
        self.sillyMeterMgr.b_setDates(holidayDates)
        tomorrow = self.air.toontownTimeManager.getCurServerDateTime().now(tz=self.air.toontownTimeManager.serverTimeZone) + timedelta(1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0, tzinfo=self.air.toontownTimeManager.serverTimeZone)
        secondsUntilMidnight = (midnight - self.air.toontownTimeManager.getCurServerDateTime().now(tz=self.air.toontownTimeManager.serverTimeZone)).seconds
        task.delayTime = secondsUntilMidnight
        return task.again

    def stop(self):
        HolidayBaseAI.stop(self)
        taskMgr.remove('checkPhase')
        self.sillyMeterMgr.requestDelete()
        self.sillyMeterMgr = None
        return