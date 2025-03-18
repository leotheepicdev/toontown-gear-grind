from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedDirectoryAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedDirectoryAI')

    def setParentingRules(self, todo0, todo1):
        pass
