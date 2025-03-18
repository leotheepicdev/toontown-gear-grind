from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
from . import DistributedBarrelBase
import random

class DistributedHealBarrel(DistributedBarrelBase.DistributedBarrelBase):

    def __init__(self, cr):
        DistributedBarrelBase.DistributedBarrelBase.__init__(self, cr)
        self.numGags = 0
        self.gagScale = 0.6

    def disable(self):
        DistributedBarrelBase.DistributedBarrelBase.disable(self)
        self.ignoreAll()

    def delete(self):
        self.gagModel.removeNode()
        del self.gagModel
        DistributedBarrelBase.DistributedBarrelBase.delete(self)

    def applyLabel(self):
        self.gagModel = loader.loadModel('phase_4/models/props/ttcTreasure')
        chosenInt = random.randint(0, 3)
        self.gagModel.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce%s.png' % chosenInt), 1)
        if chosenInt == 1:
            self.gagModel.find('**/cone').setTexture(loader.loadTexture('phase_4/maps/chocolate_cone.png'), 1)
        self.gagModel.reparentTo(self.gagNode)
        self.gagModel.setScale(self.gagScale)
        self.gagModel.setPos(0, 0, -.1 - self.gagScale)

    def setGrab(self, avId):
        DistributedBarrelBase.DistributedBarrelBase.setGrab(self, avId)
