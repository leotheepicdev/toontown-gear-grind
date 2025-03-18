from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedInGameNewsMgrUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedInGameNewsMgrUD')

    def setLatestIssueStr(self, todo0):
        pass

    def inGameNewsMgrAIStartingUp(self, todo0, todo1):
        pass

    def newIssueUDtoAI(self, todo0):
        pass
