from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals

class RRHHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('RRHHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.ResistanceRangerHideout
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

    def shutdown(self):
        HoodDataAI.HoodDataAI.shutdown(self)
