from toontown.classicchars.DistributedDonaldAI import DistributedDonaldAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals

class DistributedFrankenDonaldAI(DistributedDonaldAI):
    notify = directNotify.newCategory('DistributedFrankenDonaldAI')

    def walkSpeed(self):
        return ToontownGlobals.FrankenDonaldSpeed
