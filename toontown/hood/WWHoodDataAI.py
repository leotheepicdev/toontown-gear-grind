from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals

class WWHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('WWHoodDataAI')
    # TODO

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.WackyWest
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

    def shutdown(self):
        HoodDataAI.HoodDataAI.shutdown(self)
