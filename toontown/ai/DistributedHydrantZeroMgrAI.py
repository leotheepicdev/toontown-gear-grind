from toontown.ai.DistributedPhaseEventMgrAI import DistributedPhaseEventMgrAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedHydrantZeroMgrAI(DistributedPhaseEventMgrAI):
    notify = directNotify.newCategory('DistributedHydrantZeroMgrAI')

