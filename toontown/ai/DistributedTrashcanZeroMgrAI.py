from toontown.ai.DistributedPhaseEventMgrAI import DistributedPhaseEventMgrAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedTrashcanZeroMgrAI(DistributedPhaseEventMgrAI):
    notify = directNotify.newCategory('DistributedTrashcanZeroMgrAI')

