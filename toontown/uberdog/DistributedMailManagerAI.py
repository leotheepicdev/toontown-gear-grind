from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedMailManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedMailManagerAI')

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass
