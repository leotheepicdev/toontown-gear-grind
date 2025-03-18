from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class CentralLoggerAI(DistributedObjectAI):
    notify = directNotify.newCategory('CentralLoggerAI')

    def sendMessage(self, todo0):
        pass

    def logAIGarbage(self):
        pass
