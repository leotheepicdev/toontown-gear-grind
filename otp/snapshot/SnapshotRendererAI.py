from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class SnapshotRendererAI(DistributedObjectAI):
    notify = directNotify.newCategory('SnapshotRendererAI')

    def online(self):
        pass

    def requestRender(self, todo0, todo1, todo2):
        pass
