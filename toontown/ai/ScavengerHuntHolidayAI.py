from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.toonbase import ToontownGlobals

from . HolidayBaseAI import HolidayBaseAI
from . DistributedTrickOrTreatTargetAI import DistributedTrickOrTreatTargetAI
from . DistributedWinterCarolingTargetAI import DistributedWinterCarolingTargetAI

import pickle, time

TrickOrTreatTargets = [
    2649, # All Fun And Games Shop (Silly Street)
    1834, # Rudderly Ridiculous! (Lighthouse Lane)
    5620, # Rake It Inn (Elm Street)
    4835, # Ursatz for Really Kool Katz! (Tenor Terrace)
    3707, # Snowplace Like Home (Sleet Street)
    9619, # Relax To The Max (Lullaby Lane)
]

CarolingTargets = [
    
]

GET_GOALS = 0
ADD_GOAL = 1

RewardMoney = ToontownGlobals.TOT_REWARD_JELLYBEAN_AMOUNT

EffectDuration = 10080 # One week

class ScavengerHuntHolidayAI(HolidayBaseAI):
    notify = directNotify.newCategory('ScavengerHuntHolidayAI')

    def __init__(self, air, holidayId):
        HolidayBaseAI.__init__(self, air,holidayId)
        self.targets = []
        self.targetZones = []

    def start(self):
        HolidayBaseAI.start(self)

        if self.holidayId in [ToontownGlobals.TRICK_OR_TREAT, ToontownGlobals.SPOOKY_TRICK_OR_TREAT]:
            self.targetZones = TrickOrTreatTargets
            targetCtl = DistributedTrickOrTreatTargetAI
            self.air.dataStoreManager.startStore(1)
        elif self.holidayId in [ToontownGlobals.WINTER_CAROLING, ToontownGlobals.WACKY_WINTER_CAROLING]:
            self.targetZones = CarolingTargets
            targetCtl = DistributedWinterCarolingTargetAI
            self.air.dataStoreManager.startStore(2)
        else:
            self.notify.warning('Dont know which Hunt target to use for holiday {}!'.format(self.holidayId))
            return

        for zoneId in self.targetZones:
            targetMgr = targetCtl(self.air, self)
            targetMgr.generateWithRequired(zoneId)
            self.targets.append(targetMgr)

    def attemptScavengerHunt(self, toon, zoneId):

        def __getGoalCallback(results):
            qAvId, qZoneId, qGoals = results[1]
            if zoneId not in qGoals:
                toon.addMoney(RewardMoney)
                if self.holidayId in [ToontownGlobals.TRICK_OR_TREAT, ToontownGlobals.SPOOKY_TRICK_OR_TREAT]: 
                    toon.sendUpdate('trickOrTreatTargetMet', [RewardMoney])
                elif self.holidayId in [ToontownGlobals.WINTER_CAROLING, ToontownGlobals.WACKY_WINTER_CAROLING]:
                    toon.sendUpdate('winterCarolingTargetMet', [RewardMoney])

                qGoals.append(zoneId)
                query = pickle.dumps((ADD_GOAL, (toon.doId, zoneId)))
                self.air.dataStoreManager.queryStore(query, __setGoalCallback)

            if set(self.targetZones) == set(qGoals):
                expireTime = int(time.time() / 60 + 0.5) + EffectDuration
                if self.holidayId in [ToontownGlobals.TRICK_OR_TREAT, ToontownGlobals.SPOOKY_TRICK_OR_TREAT]:
                    toon.b_setCheesyEffect(ToontownGlobals.CEPumpkin, 0, expireTime)
                elif self.holidayId in [ToontownGlobals.WINTER_CAROLING, ToontownGlobals.WACKY_WINTER_CAROLING]:
                    toon.b_setCheesyEffect(ToontownGlobals.CESnowMan, 0, expireTime)

        def __setGoalCallback(results):
            pass

        query = pickle.dumps((GET_GOALS, (toon.doId, zoneId)))
        self.air.dataStoreManager.queryStore(query, __getGoalCallback)

    def stop(self):
        HolidayBaseAI.stop(self)

        if self.holidayId in [ToontownGlobals.TRICK_OR_TREAT, ToontownGlobals.SPOOKY_TRICK_OR_TREAT]:
            self.air.dataStoreManager.stopStore(1)
        elif self.holidayId in [ToontownGlobals.WINTER_CAROLING, ToontownGlobals.WACKY_WINTER_CAROLING]:
            self.air.dataStoreManager.stopStore(2)

        for targetMgr in self.targets:
            targetMgr.requestDelete()

        self.targets = []
