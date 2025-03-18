from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class DistributedDeliveryManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedDeliveryManagerUD')

    def requestAck(self):
        avId = self.air.getAvatarIdFromSender()

        if not avId:
            return

        self.sendUpdateToAvatarId(avId, 'returnAck', [])
