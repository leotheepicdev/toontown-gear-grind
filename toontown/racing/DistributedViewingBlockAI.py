
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI
from direct.directnotify import DirectNotifyGlobal

class DistributedViewingBlockAI(DistributedStartingBlockAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedViewingBlockAI')

    def __init__(self, air):
        DistributedStartingBlockAI.__init__(self, air)



