from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class SnapshotRendererUD(DistributedObjectUD):
    notify = directNotify.newCategory('SnapshotRendererUD')

    def online(self):
        pass

    def requestRender(self, todo0, todo1, todo2):
        pass
