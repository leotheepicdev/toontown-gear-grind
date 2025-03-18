from toontown.ai.DistributedPhaseEventMgrAI import DistributedPhaseEventMgrAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedMailboxZeroMgrAI(DistributedPhaseEventMgrAI):
    notify = directNotify.newCategory('DistributedMailboxZeroMgrAI')

