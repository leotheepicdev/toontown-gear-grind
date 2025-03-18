from direct.directnotify import DirectNotifyGlobal
import random
from direct.task import Task
from toontown.effects import DistributedFireworkShowAI

class HolidayBaseAI:

    def __init__(self, air, holidayId):
        self.air = air
        self.holidayId = holidayId
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def getRunningState(self):
        return self.running
