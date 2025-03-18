from toontown.classicchars.DistributedPlutoAI import DistributedPlutoAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals

class DistributedWesternPlutoAI(DistributedPlutoAI):
    notify = directNotify.newCategory('DistributedWesternPlutoAI')

    def walkSpeed(self):
        return ToontownGlobals.WesternPlutoSpeed
