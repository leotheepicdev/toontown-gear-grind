from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class SnapshotDispatcherAI(DistributedObjectAI):
    notify = directNotify.newCategory('SnapshotDispatcherAI')

    def online(self):
        pass

    def requestRender(self, todo0):
        pass

    def avatarDeleted(self, todo0):
        pass

    def requestNewWork(self, todo0):
        pass

    def errorFetchingAvatar(self, todo0, todo1):
        pass

    def errorRenderingAvatar(self, todo0, todo1):
        pass

    def renderSuccessful(self, todo0, todo1):
        pass
