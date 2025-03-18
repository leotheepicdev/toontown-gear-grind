from .DistributedToonInteriorAI import *
from toontown.toonbase import ToontownGlobals

class DistributedToonHallInteriorAI(DistributedToonInteriorAI):

    def __init__(self, block, air, zoneId, building):
        DistributedToonInteriorAI.__init__(self, block, air, zoneId, building)

    def getCurPhase(self):
        result = -1
        enoughInfoToRun = False
        if ToontownGlobals.SILLYMETER_HOLIDAY in simbase.air.holidayManager.currentHolidays and simbase.air.holidayManager.currentHolidays[ToontownGlobals.SILLYMETER_HOLIDAY] != None and simbase.air.holidayManager.currentHolidays[ToontownGlobals.SILLYMETER_HOLIDAY].getRunningState():
            if hasattr(simbase.air, 'SillyMeterMgr'):
                enoughInfoToRun = True
            else:
                self.notify.debug('simbase.air does not have SillyMeterMgr')
        else:
            self.notify.debug('holiday is not running')
        self.notify.debug('enoughInfoToRun = %s' % enoughInfoToRun)
        if enoughInfoToRun and simbase.air.SillyMeterMgr.getIsRunning():
            result = simbase.air.SillyMeterMgr.getCurPhase()
        return result

    def delete(self):
        self.ignoreAll()
        DistributedToonInteriorAI.delete(self)
