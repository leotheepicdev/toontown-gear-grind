from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedMailManagerUD(DistributedObjectUD):
    notify = directNotify.newCategory('DistributedMailManagerUD')

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass
