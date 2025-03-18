from toontown.classicchars.DistributedMickeyAI import DistributedMickeyAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedWitchMinnieAI(DistributedMickeyAI):
    notify = directNotify.newCategory('DistributedWitchMinnieAI')

