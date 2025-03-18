from toontown.classicchars.DistributedChipAI import DistributedChipAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedPoliceChipAI(DistributedChipAI):
    notify = directNotify.newCategory('DistributedPoliceChipAI')

