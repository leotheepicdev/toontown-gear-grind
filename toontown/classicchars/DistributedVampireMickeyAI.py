from toontown.classicchars.DistributedMickeyAI import DistributedMickeyAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals

class DistributedVampireMickeyAI(DistributedMickeyAI):
    notify = directNotify.newCategory('DistributedVampireMickeyAI')

    def walkSpeed(self):
        return ToontownGlobals.VampireMickeySpeed
