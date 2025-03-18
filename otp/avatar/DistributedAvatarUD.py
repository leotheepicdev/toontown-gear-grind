from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedAvatarUD(DistributedObjectUD):
    notify = directNotify.newCategory('DistributedAvatarUD')

    def setName(self, todo0):
        pass

    def friendsNotify(self, todo0, todo1):
        pass

    def checkAvOnShard(self, todo0):
        pass

    def confirmAvOnShard(self, todo0, todo1):
        pass
