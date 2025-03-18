from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.toonbase import ToontownGlobals

from toontown.ai.HolidayBaseAI import HolidayBaseAI
from toontown.effects.FireworkHolidayAI import FireworkHolidayAI
from toontown.fishing.FishBingoManagerAI import FishBingoHolidayMgr
from toontown.ai.DistributedBlackCatMgrAI import BlackCatDayHolidayAI
from toontown.racing.RaceManagerAI import KartRecordDailyResetter, KartRecordWeeklyResetter, CircuitRaceHolidayMgr
from toontown.ai.ScavengerHuntHolidayAI import ScavengerHuntHolidayAI
from toontown.minigame.TrolleyHolidayMgrAI import TrolleyHolidayMgrAI
from toontown.minigame.TrolleyWeekendMgrAI import TrolleyWeekendMgrAI
from toontown.ai.CharacterSwitchHolidayAI import CharacterSwitchHolidayAI
from toontown.ai.DistributedGreenToonEffectMgrAI import GreenToonHolidayAI
from toontown.ai.SillyMeterHolidayAI import SillyMeterHolidayAI

holidayToMgr = {
    ToontownGlobals.JULY4_FIREWORKS: FireworkHolidayAI, # 1
    ToontownGlobals.NEWYEARS_FIREWORKS: FireworkHolidayAI, # 2
    ToontownGlobals.FISH_BINGO_NIGHT: FishBingoHolidayMgr, # 7
    ToontownGlobals.BLACK_CAT_DAY: BlackCatDayHolidayAI, # 9
    ToontownGlobals.KART_RECORD_DAILY_RESET: KartRecordDailyResetter, # 11
    ToontownGlobals.KART_RECORD_WEEKLY_RESET: KartRecordWeeklyResetter, # 12
    ToontownGlobals.TRICK_OR_TREAT: ScavengerHuntHolidayAI, # 13
    ToontownGlobals.CIRCUIT_RACING: CircuitRaceHolidayMgr, # 14
    ToontownGlobals.CIRCUIT_RACING_EVENT: CircuitRaceHolidayMgr, # 16
    ToontownGlobals.TROLLEY_HOLIDAY: TrolleyHolidayMgrAI, # 17
    ToontownGlobals.TROLLEY_WEEKEND: TrolleyWeekendMgrAI, # 18
    #ToontownGlobals.SILLY_SATURDAY_BINGO: FishBingoHolidayMgr, # 19
    #ToontownGlobals.SILLY_SATURDAY_CIRCUIT: CircuitRaceHolidayMgr, # 20
    #ToontownGlobals.SILLY_SATURDAY_TROLLEY: TrolleyHolidayMgrAI, # 21
    ToontownGlobals.HALLOWEEN_COSTUMES: CharacterSwitchHolidayAI, # 27
    ToontownGlobals.APRIL_FOOLS_COSTUMES: CharacterSwitchHolidayAI, # 29
    ToontownGlobals.WINTER_CAROLING: ScavengerHuntHolidayAI, # 57
    ToontownGlobals.COMBO_FIREWORKS: FireworkHolidayAI, # 112
    ToontownGlobals.IDES_OF_MARCH: GreenToonHolidayAI, # 105
    ToontownGlobals.SPOOKY_BLACK_CAT: BlackCatDayHolidayAI, # 117
    ToontownGlobals.SPOOKY_TRICK_OR_TREAT: ScavengerHuntHolidayAI, # 118
    ToontownGlobals.SPOOKY_COSTUMES: CharacterSwitchHolidayAI, # 120
    ToontownGlobals.WACKY_WINTER_CAROLING: ScavengerHuntHolidayAI, # 122
    ToontownGlobals.SILLYMETER_HOLIDAY: SillyMeterHolidayAI
}

class HolidayManagerAI:
    notify = directNotify.newCategory('HolidayManagerAI')

    def __init__(self, air):
        self.air = air

        # Dictionaries:
        self.currentHolidays = {}

    def isHolidayRunning(self, holidayId):
        return holidayId in self.currentHolidays

    def isMoreXpHolidayRunning(self):
        if ToontownGlobals.MORE_XP_HOLIDAY in self.currentHolidays:
            return True

        return False

    def getCurPhase(self, holidayId):
        # TODO: Figure out how this works.
        return 1

    def startHoliday(self, holidayId, task = None):
        if holidayId not in self.currentHolidays:
            if holidayId in holidayToMgr:
                holidayMgr = holidayToMgr[holidayId]
                for holiday in self.currentHolidays.values():
                    if isinstance(holiday, holidayMgr):
                        self.notify.warning('Unable to start holiday {} because the same manager for {} is already running!'.format(holidayId, holiday.holidayId))
                        return
                holidayMgr = holidayMgr(self.air, holidayId)
            else:
                holidayMgr = HolidayBaseAI(self.air, holidayId)
            holidayMgr.start()
            self.currentHolidays[holidayId] = holidayMgr
            self.air.newsManager.d_setHolidayIdList(list(self.currentHolidays.keys()))

        if task:
            return task.done

    def endHoliday(self, holidayId):
        if holidayId in self.currentHolidays:
            self.currentHolidays[holidayId].stop()
            del self.currentHolidays[holidayId]
            self.air.newsManager.d_setHolidayIdList(list(self.currentHolidays.keys()))
