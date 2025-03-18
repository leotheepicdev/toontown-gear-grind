from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedWhitelistMgrUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedWhitelistMgrUD')

    def updateWhitelist(self):
        pass

    def whitelistMgrAIStartingUp(self, todo0, todo1):
        pass

    def newListUDtoAI(self):
        pass
