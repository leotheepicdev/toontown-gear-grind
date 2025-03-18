from toontown.ai.DistributedScavengerHuntTargetAI import DistributedScavengerHuntTargetAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedWinterCarolingTargetAI(DistributedScavengerHuntTargetAI):
    notify = directNotify.newCategory('DistributedWinterCarolingTargetAI')

