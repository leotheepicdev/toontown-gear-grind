from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorExtAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal

class DistributedCogTowerElevatorAI(DistributedElevatorExtAI.DistributedElevatorExtAI):

    def __init__(self, air, bldg):
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg)
        self.type = ELEVATOR_COG_TOWER
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.activeCogTowerZone = None
        self.players = []

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()
        if numPlayers > 0:
            self.players = []
            for i in self.seats:
                if i not in [None, 0]:
                    self.players.append(i)
            self.activeCogTowerZone = self.bldg.createCogTowerInterior(self.players)
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setCogTowerZone', [self.activeCogTowerZone])
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning('The elevator left, but was empty.')
        self.fsm.request('closed')
		
    def enterClosed(self):
        DistributedElevatorExtAI.DistributedElevatorExtAI.enterClosed(self)
        self.__doorsClosed()
		
    def __doorsClosed(self):
        self.fsm.request('opening')       

