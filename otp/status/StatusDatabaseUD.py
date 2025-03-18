from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class StatusDatabaseUD(DistributedObjectUD):
    notify = directNotify.newCategory('StatusDatabaseUD')

    def requestOfflineAvatarStatus(self, todo0):
        pass

    def recvOfflineAvatarStatus(self, todo0, todo1):
        pass
