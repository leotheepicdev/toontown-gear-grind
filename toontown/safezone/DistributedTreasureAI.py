from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
import random

class DistributedTreasureAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air, treasurePlanner, x, y, z, sillySurgeChance = 0):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.treasurePlanner = treasurePlanner
        self.pos = (x, y, z)
        self.sillySurge = 0
        if sillySurgeChance > 0:
            if random.random() <= sillySurgeChance:
                self.sillySurge = 1
        self.variations = []
        self.variant = 0

    def requestGrab(self):
        avId = self.air.getAvatarIdFromSender()
        self.treasurePlanner.grabAttempt(avId, self.getDoId())

    def validAvatar(self, av):
        return 1

    def d_setGrab(self, avId):
        self.sendUpdate('setGrab', [avId])

    def d_setReject(self):
        self.sendUpdate('setReject', [])
        
    def getVariant(self):
        if self.variations != []:
            self.variant = random.choice(self.variations)
        return self.variant

    def getPosition(self):
        return self.pos

    def setPosition(self, x, y, z):
        self.pos = (x, y, z)

    def b_setPosition(self, x, y, z):
        self.setPosition(x, y, z)
        self.d_setPosition(x, y, z)

    def d_setPosition(self, x, y, z):
        self.sendUpdate('setPosition', [x, y, z])
        
    def getSillySurge(self):
        return self.sillySurge
