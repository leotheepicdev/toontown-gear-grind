from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from . HolidayBaseAI import HolidayBaseAI

class DistributedBlackCatMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedBlackCatMgrAI')

    def setAvId(self, avId):
        self.avId = avId

    def getAvId(self):
        return self.avId

    def doBlackCatTransformation(self):
        avId = self.air.getAvatarIdFromSender()

        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId, 'Got black cat attempt for {} while we\'re expecting for {}!'.format(avId, self.avId))
            return

        toon = self.air.doId2do.get(avId)

        if not toon:
            self.air.writeServerEvent('suspicious', avId, 'Unknown avatar {} tried to create a black cat!'.format(avId))
            return

        toon.makeBlackCat()

class BlackCatDayHolidayAI(HolidayBaseAI):
    PostName = 'BlackCatDay'

    def start(self):
        HolidayBaseAI.start(self)
        bboard.post(self.PostName, True)

    def stop(self):
        HolidayBaseAI.stop(self)
        bboard.remove(self.PostName)
