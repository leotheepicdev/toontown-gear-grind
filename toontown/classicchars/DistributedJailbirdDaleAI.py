from toontown.classicchars.DistributedDaleAI import DistributedDaleAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedJailbirdDaleAI(DistributedDaleAI):
    notify = directNotify.newCategory('DistributedJailbirdDaleAI')

