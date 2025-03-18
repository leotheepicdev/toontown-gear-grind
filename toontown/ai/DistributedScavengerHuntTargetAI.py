from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedScavengerHuntTargetAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedScavengerHuntTargetAI')

    def __init__(self, air, holidayMgr):
        DistributedObjectAI.__init__(self, air)

        self.holidayMgr = holidayMgr

    def attemptScavengerHunt(self):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)

        if not toon:
            message = 'Unknown player {} tried to attempt scavenger hunt!'.format(avId)
            self.notify.warning(message)
            self.air.writeServerEvent('suspicious', avId, message)
            return

        self.holidayMgr.attemptScavengerHunt(toon, self.zoneId)
