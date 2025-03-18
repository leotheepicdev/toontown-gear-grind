from toontown.ai.DistributedScavengerHuntTargetAI import DistributedScavengerHuntTargetAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedTrickOrTreatTargetAI(DistributedScavengerHuntTargetAI):
    notify = directNotify.newCategory('DistributedTrickOrTreatTargetAI')

