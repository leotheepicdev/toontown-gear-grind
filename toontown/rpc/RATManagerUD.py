from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class RATManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('RATManagerUD')

