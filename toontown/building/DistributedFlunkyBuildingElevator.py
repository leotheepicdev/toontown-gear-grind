from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevator
from toontown.building import DistributedElevatorExt
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedFlunkyBuildingElevator(DistributedElevatorExt.DistributedElevatorExt):

    def __init__(self, cr):
        DistributedElevatorExt.DistributedElevatorExt.__init__(self, cr)
        self.openSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.ogg')
        self.finalOpenSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.ogg')
        self.closeSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_sliding.ogg')
        self.finalCloseSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_open_final.ogg')
        self.type = ELEVATOR_NORMAL
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
        npc = self.elevatorModel.findAllMatches('**/floor_light_?;+s')
        for i in range(npc.getNumPaths()):
            np = npc.getPath(i)
            floor = int(np.getName()[-1:]) - 1
            if floor < 2:
                np.setColor(LIGHT_OFF_COLOR)
            else:
                np.hide()

        self.leftDoor = self.elevatorModel.find('**/left-door')
        self.rightDoor = self.elevatorModel.find('**/right-door')
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
        
    def _getDoorsClosedInfo(self):
        return ('', '')

    def setFlunkyBuildingZone(self, zoneId):
        if self.localToonOnBoard:
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {'loader': 'flunkyBuildingInterior',
             'where': 'flunkyBuildingInterior',
             'zoneId': zoneId,
             'hoodId': hoodId,
             'shardId': None}
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)

    def getDestName(self):
        return TTLocalizer.ElevatorCogTower
