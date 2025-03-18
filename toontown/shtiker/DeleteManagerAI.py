from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DeleteManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('DeleteManagerAI')

    def setInventory(self, todo0):
        pass
