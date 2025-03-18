from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.toonbase import TTLocalizer


class DistributedPartyTrampolineActivityAI(DistributedPartyActivityAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyTrampolineActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        FSM.__init__(self, 'DistributedPartyTrampolineActivityAI')
        self.currentToon = 0
        self.collected = 0
        self.record = 0
        self.jellybeans = []

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.demand('Idle')

    def delete(self):
        taskMgr.remove(self.uniqueName('leave-trampoline'))
        DistributedPartyActivityAI.delete(self)

    def awardBeans(self, numBeans, height):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to give beans while not using the trampoline!')
            return

        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to award beans while the game wasn\'t running!')
            return

        if numBeans != self.collected:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon reported incorrect number of collected jellybeans!')
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to award beans while not in district!')
            return

        reward = self.getTotalReward(self.collected * 2)
        message = TTLocalizer.PartyTrampolineBeanResults % self.collected
        if self.collected == PartyGlobals.TrampolineNumJellyBeans:
            reward += PartyGlobals.TrampolineJellyBeanBonus
            message = TTLocalizer.PartyTrampolineBonusBeanResults % (
                self.collected, PartyGlobals.TrampolineJellyBeanBonus)

        message += '\n\n' + TTLocalizer.PartyTrampolineTopHeightResults % height
        self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [reward, av.getMoney(), message])
        av.addMoney(reward)

    def reportHeightInformation(self, height):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to report height without being on the district!')
            return

        if height > self.record:
            self.record = height
            self.sendUpdate('setBestHeightInfo', [av.getName(), height])
        else:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon incorrectly reported height!')
            return

    def enterActive(self):
        self.jellybeans = list(range(PartyGlobals.TrampolineNumJellyBeans))
        taskMgr.doMethodLater(PartyGlobals.TrampolineDuration, self.__leaveTrampolineTask,
                              self.uniqueName('leave-trampoline'))
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])
        self.collected = 0

    def enterIdle(self):
        self.sendUpdate('setState', ['Idle', globalClockDelta.getRealNetworkTime()])
        self.currentToon = 0
        self.b_setToonsPlaying([])

    def enterRules(self):
        self.sendUpdate('setState', ['Rules', globalClockDelta.getRealNetworkTime()])

    def __leaveTrampolineTask(self, task):
        self.sendUpdate('leaveTrampoline')
        return task.done

    def requestAnim(self, anim):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to request an animation while not playing!')
            return

        if self.currentToon != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to request an anim for someone else!')
            return

        self.sendUpdate('requestAnimEcho', [anim])

    def removeBeans(self, beans):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to collect jellybeans while not playing!')
            return

        if self.currentToon != avId:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to collect jellybeans while someone else was playing!')
            return

        for bean in beans:
            if bean not in self.jellybeans:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to collect non-existent bean!')
                beans.remove(bean)
            else:
                self.collected += 1

        self.sendUpdate('removeBeansEcho', [beans])

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.state == 'Active':
            self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        self.currentToon = avId
        self.sendUpdate('setToonsPlaying', [[self.currentToon]])
        self.demand('Rules')

    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.state != 'Active':
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to leave a trampoline that was not running!')
            return

        if self.currentToon != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to exit trampoline for someone else!')
            return

        taskMgr.remove(self.uniqueName('leave-trampoline'))
        self.sendUpdate('leaveTrampoline')

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to exit trampoline they\'re not using!')
            return

        self.demand('Idle')

    def toonReady(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.state != 'Rules':
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to verify rules while the rules were not running!')
            return

        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to verify rules for someone else!')
            return

        self.demand('Active')
