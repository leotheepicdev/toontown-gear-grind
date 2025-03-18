from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorExtAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal

class DistributedFlunkyBuildingElevatorAI(DistributedElevatorExtAI.DistributedElevatorExtAI):

    def __init__(self, air, bldg):
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg)
        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.activeFlunkyBuildingZone = None
        self.players = []

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()
        if numPlayers > 0:
            self.players = []
            for i in self.seats:
                if i not in [None, 0]:
                    self.players.append(i)
            self.activeFlunkyBuildingZone = self.bldg.createFlunkyBuildingInterior(self.players)
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setFlunkyBuildingZone', [self.activeFlunkyBuildingZone])
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning('The elevator left, but was empty.')
        self.fsm.request('closed')
		
    def enterClosed(self):
        DistributedElevatorExtAI.DistributedElevatorExtAI.enterClosed(self)
        self.__doorsClosed()
		
    def __doorsClosed(self):
        self.fsm.request('opening')

