from toontown.classicchars.DistributedDaisyAI import DistributedDaisyAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedSockHopDaisyAI(DistributedDaisyAI):
    notify = directNotify.newCategory('DistributedSockHopDaisyAI')

