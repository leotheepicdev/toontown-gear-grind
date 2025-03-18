from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.toonbase import ToontownGlobals

import time

class DistributedPolarPlaceEffectMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedPolarPlaceEffectMgrAI')

    def addPolarPlaceEffect(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if av.getCheesyEffect()[0] != ToontownGlobals.CEBigWhite:
            expireTime = int(time.time() / 60 + 0.5) + 3600
            av.b_setCheesyEffect(ToontownGlobals.CEBigWhite, ToontownGlobals.TheBrrrgh, expireTime)