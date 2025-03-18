from toontown.classicchars.DistributedGoofySpeedwayAI import DistributedGoofySpeedwayAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals

class DistributedSuperGoofyAI(DistributedGoofySpeedwayAI):
    notify = directNotify.newCategory('DistributedSuperGoofyAI')

    def walkSpeed(self):
        return ToontownGlobals.SuperGoofySpeed
