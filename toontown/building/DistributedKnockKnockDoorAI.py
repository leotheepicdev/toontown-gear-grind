from otp.ai.AIBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from . import DistributedAnimatedPropAI
from direct.task.Task import Task
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
import time

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI.DistributedAnimatedPropAI):

    def __init__(self, air, propId):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.__init__(self, air, propId)
        self.fsm.setName('DistributedKnockKnockDoor')
        self.propId = propId
        self.doLaterTask = None

    def enterOff(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterOff(self)

    def exitOff(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitOff(self)

    def attractTask(self, task):
        self.fsm.request('attract')
        return Task.done

    def enterAttract(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterAttract(self)

    def exitAttract(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitAttract(self)

    def enterPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterPlaying(self)
        self.doLaterTask = taskMgr.doMethodLater(9, self.attractTask, self.uniqueName('knockKnock-timer'))

    def exitPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitPlaying(self)
        taskMgr.remove(self.doLaterTask)
        self.doLaterTask = None

    def requestGetToonup(self):
        sender = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(sender)
        if not av:
            return
        if av.getNextKnockKnockHeal() > time.time():
            return
        if av.getHp() == av.getMaxHp():
            return
        zoneId = ZoneUtil.getCanonicalHoodId(av.zoneId)
        if zoneId in ToontownGlobals.Hood2KnockKnockHeal:
            heal = ToontownGlobals.Hood2KnockKnockHeal[zoneId]
        else:
            heal = 5
        av.toonUp(heal)
        av.b_setNextKnockKnockHeal(int(time.time() + ToontownGlobals.KnockKnockCooldown))
