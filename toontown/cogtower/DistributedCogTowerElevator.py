from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevator
from toontown.building import DistributedElevatorExt
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedCogTowerElevator(DistributedElevatorExt.DistributedElevatorExt):

    def __init__(self, cr):
        DistributedElevatorExt.DistributedElevatorExt.__init__(self, cr)
        self.openSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.ogg')
        self.finalOpenSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.ogg')
        self.closeSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.ogg')
        self.finalCloseSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.ogg')
        self.type = ELEVATOR_COG_TOWER
        self.countdownTime = ElevatorData[self.type]['countdown']

    def disable(self):
        DistributedElevator.DistributedElevator.disable(self)

    def generate(self):
        DistributedElevatorExt.DistributedElevatorExt.generate(self)

    def delete(self):
        self.elevatorModel.removeNode()
        del self.elevatorModel
        DistributedElevatorExt.DistributedElevatorExt.delete(self)

    def setupElevator(self):
        self.elevatorModel = loader.loadModel('phase_4/models/modules/elevator')
        self.elevatorModel.reparentTo(render)
        self.elevatorModel.setScale(1.05)
        self.elevatorModel.setPosHpr(64.793, -2.34, 0.0, -900.0, 0.0, 0.0)
        self.leftDoor = self.elevatorModel.find('**/left-door')
        self.rightDoor = self.elevatorModel.find('**/right-door')
        self.elevatorModel.find('**/light_panel').removeNode()
        self.elevatorModel.find('**/light_panel_frame').removeNode()
        DistributedElevator.DistributedElevator.setupElevator(self)

    def getElevatorModel(self):
        return self.elevatorModel
		
    def setBldgDoId(self, bldgDoId):
        self.bldg = None
        self.setupElevator()

    def getZoneId(self):
        return 0

    def __doorsClosed(self, zoneId):
        pass

    def setCogTowerZone(self, zoneId):
        if self.localToonOnBoard:
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {'loader': 'safeZoneLoader',
             'where': 'cogTowerInterior',
             'zoneId': zoneId,
             'hoodId': hoodId}
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)

    def getDestName(self):
        return TTLocalizer.ElevatorCogTower
