from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import TTTreasurePlannerAI
from toontown.classicchars import DistributedMickeyAI
from toontown.safezone import ButterflyGlobals
from toontown.building import FlunkyBuildingMgrAI, DistributedFlunkyBuildingElevatorAI, DistributedFlunkyBuildingAI
from direct.task import Task

class TTHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.ToontownCentral
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)
        return

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.addDistObj(trolley)
        self.trolley = trolley
        self.treasurePlanner = TTTreasurePlannerAI.TTTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
        self.addDistObj(self.classicChar)
        if self.zoneId == ToontownGlobals.ToontownCentral:
            terrace = 2400
        else:
            terrace = 22400
        self.flunkyBldgElevator = DistributedFlunkyBuildingElevatorAI.DistributedFlunkyBuildingElevatorAI(self.air, FlunkyBuildingMgrAI.FlunkyBuildingMgrAI(self.air))
        self.flunkyBldgElevator.generateWithRequired(terrace)
        self.addDistObj(self.flunkyBldgElevator)
        self.flunkyBldg = DistributedFlunkyBuildingAI.DistributedFlunkyBuildingAI(self.air)
        self.flunkyBldg.setPosHpr(0, 5, 0, 90, 0, 0)
        self.flunkyBldg.setElevatorDoId(self.flunkyBldgElevator.doId)
        self.flunkyBldg.generateWithRequired(terrace)
        self.addDistObj(self.flunkyBldg)
        self.createButterflies(ButterflyGlobals.TTC)
        if simbase.blinkTrolley:
            taskMgr.doMethodLater(0.5, self._deleteTrolley, 'deleteTrolley')
        messenger.send('TTHoodSpawned', [self])

    def shutdown(self):
        HoodDataAI.HoodDataAI.shutdown(self)
        messenger.send('TTHoodDestroyed', [self])

    def _deleteTrolley(self, task):
        self.trolley.requestDelete()
        taskMgr.doMethodLater(0.5, self._createTrolley, 'createTrolley')
        return Task.done

    def _createTrolley(self, task):
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.trolley = trolley
        taskMgr.doMethodLater(0.5, self._deleteTrolley, 'deleteTrolley')
        return Task.done
