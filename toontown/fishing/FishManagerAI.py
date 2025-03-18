from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.fishing import FishGlobals
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.FishBase import FishBase
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI

import random
import json, os
from datetime import datetime, timedelta

class FishManagerAI:
    notify = directNotify.newCategory('FishManagerAI')
    serverDataFolder = simbase.config.GetString('dailycatch-data-backup-folder', '')

    def __init__(self, air):
        self.air = air

        # Dictonaries:
        self.requestedFish = {}
        
    def getFileName(self):
        if not os.path.exists(self.serverDataFolder):
            os.makedirs(self.serverDataFolder)
        f = '%s/%s_dailycatch.json' % (self.serverDataFolder, str(self.air.districtId))
        return f
        
    def generateNextDailyCatch(self, task):
        taskMgr.remove('generateNextDailyCatch')
        self.generateDailyCatch()
        
    def generateDailyCatch(self):
    
        now = self.air.toontownTimeManager.getCurServerDateTime().now(tz=self.air.toontownTimeManager.serverTimeZone)
        future = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
        
        filename = self.getFileName()
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                genus, species = FishGlobals.getRandomFish()
                info = {'genus': genus,
                        'species': species,
                        'now': str(now)}
                json.dump(info, file, sort_keys=1, indent=4, separators=[',', ': '])
        else:
            info = json.load(open(filename, 'r'))
            oldNow = info['now']
            old_datetime_obj = datetime.strptime(oldNow, "%Y-%m-%d %H:%M:%S.%f%z")
            genus = info['genus']
            species = info['species']
            if datetime(old_datetime_obj.year, old_datetime_obj.month, old_datetime_obj.day) < datetime(now.year, now.month, now.day):
                genus, species = FishGlobals.getRandomFish()
                with open(filename, 'w') as file:
                    genus, species = FishGlobals.getRandomFish()
                    info = {'genus': genus,
                            'species': species,
                            'now': str(now)}
                    json.dump(info, file, sort_keys=1, indent=4, separators=[',', ': '])
                    
        self.air.newsManager.b_setDailyCatch(genus, species)
        
        seconds = (future - now).total_seconds()
        taskMgr.doMethodLater(seconds, self.generateNextDailyCatch, 'generateNextDailyCatch')

    def generatePond(self, area, zoneId):
        fishingPond = DistributedFishingPondAI(self.air)
        fishingPond.setArea(area)
        fishingPond.generateWithRequired(zoneId)
        fishingPond.start()
        return fishingPond

    def generateSpots(self, dnaData, fishingPond):
        zoneId = fishingPond.zoneId
        doId = fishingPond.getDoId()
        fishingSpot = DistributedFishingSpotAI(self.air)
        fishingSpot.setPondDoId(doId)
        x, y, z = dnaData.getPos()
        h, p, r = dnaData.getHpr()
        fishingSpot.setPosHpr(x, y, z, h, p, r)
        fishingSpot.generateWithRequired(zoneId)
        return fishingSpot

    def generateCatch(self, av, zoneId):
        if len(av.fishTank) >= av.getMaxFishTank():
            return [FishGlobals.OverTankLimit, 0, 0, 0]
        caughtItem = self.air.questManager.toonFished(av, zoneId)
        if caughtItem:
            return [FishGlobals.QuestItem, caughtItem, 0, 0]
        rand = random.random() * 100.0
        for cutoff in FishGlobals.SortedProbabilityCutoffs:
            if rand <= cutoff:
                itemType = FishGlobals.ProbabilityDict[cutoff]
                break

        if av.doId in self.requestedFish:
            genus, species = self.requestedFish[av.doId]
            weight = FishGlobals.getRandomWeight(genus, species)
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            else:
                if fishType == FishGlobals.COLLECT_NEW_RECORD:
                    itemType = FishGlobals.FishItemNewRecord
                else:
                    itemType = FishGlobals.FishItem
            collectionNetList = av.fishCollection.getNetLists()
            av.d_setFishCollection(collectionNetList[0], collectionNetList[1], collectionNetList[2])
            av.fishTank.addFish(fish)
            tankNetList = av.fishTank.getNetLists()
            av.d_setFishTank(tankNetList[0], tankNetList[1], tankNetList[2])
            del self.requestedFish[av.doId]
            return [
             itemType, genus, species, weight]
        if itemType == FishGlobals.FishItem:
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            else:
                if fishType == FishGlobals.COLLECT_NEW_RECORD:
                    itemType = FishGlobals.FishItemNewRecord
                else:
                    itemType = FishGlobals.FishItem
            collectionNetList = av.fishCollection.getNetLists()
            av.d_setFishCollection(collectionNetList[0], collectionNetList[1], collectionNetList[2])
            av.fishTank.addFish(fish)
            tankNetList = av.fishTank.getNetLists()
            av.d_setFishTank(tankNetList[0], tankNetList[1], tankNetList[2])
            return [
             itemType, genus, species, weight]
        money = random.choice(FishGlobals.Rod2JellybeanDict[av.getFishingRod()])
        av.addMoney(money)
        return [
         itemType, money, 0, 0]

    def creditFishTank(self, av):
        totalFish = len(av.fishCollection)
        trophies = int(totalFish / 10)
        curTrophies = len(av.fishingTrophies)
        av.addMoney(av.fishTank.getTotalValue()[0])
        av.b_setFishTank([], [], [])
        if trophies > curTrophies:
            av.b_setMaxHp(av.getMaxHp() + trophies - curTrophies)
            av.toonUp(av.getMaxHp())
            av.b_setFishingTrophies(list(range(trophies)))
            if trophies in FishGlobals.Trophies2BucketUpgrade:
                av.b_setMaxFishTank(FishGlobals.Trophies2BucketUpgrade[trophies])
                return 2
            return 1
        return 0