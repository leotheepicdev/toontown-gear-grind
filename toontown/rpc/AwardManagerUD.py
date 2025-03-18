from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class AwardManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('AwardManagerUD')

    def giveAwardToToon(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass
