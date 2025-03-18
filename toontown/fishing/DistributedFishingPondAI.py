from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.fishing import FishingTargetGlobals
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI

class DistributedFishingPondAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedFishingPondAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        # Defines:
        self.area = None
        self.bingoMgr = None

        # Dictonaries:
        self.targets = {}
        self.spots = {}

    def setArea(self, area):
        self.area = area

    def d_setArea(self, area):
        self.sendUpdate('setArea', [area])

    def b_setArea(self, area):
        self.setArea(area)
        self.d_setArea(area)

    def getArea(self):
        return self.area

    def start(self):
        for _ in range(FishingTargetGlobals.getNumTargets(self.area)):
            fishingTarget = DistributedFishingTargetAI(simbase.air)
            fishingTarget.setPondDoId(self.getDoId())
            fishingTarget.generateWithRequired(self.zoneId)

    def addTarget(self, target):
        self.targets[target.doId] = target

    def addSpot(self, spot):
        self.spots[spot.doId] = spot

    def hitTarget(self, target):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return
        if self.targets.get(target) is None:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to hit nonexistent fishing target!')
            return
        spot = self.hasToon(avId)
        if spot:
            spot.considerReward(target)
            return
        self.air.writeServerEvent('suspicious', avId, 'Toon tried to catch fish while not fishing!')
        return

    def hasToon(self, avId):
        for spot in self.spots:
            if self.spots[spot].avId == avId:
                return self.spots[spot]