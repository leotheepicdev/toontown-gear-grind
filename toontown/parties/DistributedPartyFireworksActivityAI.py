import random

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM

from toontown.effects import FireworkShows
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI

class DistributedPartyFireworksActivityAI(DistributedPartyActivityAI, FSM):
    notify = directNotify.newCategory('DistributedPartyFireworksActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        FSM.__init__(self, 'DistributedPartyFireworksActivityAI')

        self.state = 'Idle'
        self.eventId = PartyGlobals.FireworkShows.Summer
        self.showStyle = random.randint(0, len(FireworkShows.shows[self.eventId]) - 1)

    def delete(self):
        taskMgr.remove(self.uniqueName('disable-party-fireworks'))
        DistributedPartyActivityAI.delete(self)

    def setEventId(self, eventId):
        self.eventId = eventId

    def d_setEventId(self, eventId):
        self.sendUpdate('setEventId', [eventId])

    def b_setEventId(self, eventId):
        self.setEventId(eventId)
        self.d_setEventId(eventId)

    def getEventId(self):
        return self.eventId

    def setShowStyle(self, showStyle):
        self.showStyle = showStyle

    def d_setShowStyle(self, showStyle):
        self.sendUpdate('setShowStyle', [showStyle])

    def b_setShowStyle(self, showStyle):
        self.setShowStyle(showStyle)
        self.d_setShowStyle(showStyle)

    def getShowStyle(self):
        return self.showStyle

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        party = self.air.doId2do.get(self.parent)
        if not party:
            return

        hostId = party.hostId
        if not hostId:
            return

        if avId == hostId and self.state == 'Idle':
            self.request('Active')
            duration = (FireworkShows.getShowDuration(self.getEventId(),
                                                      self.getShowStyle()) + PartyGlobals.FireworksPostLaunchDelay)
            taskMgr.doMethodLater(duration, self.showEnded, self.uniqueName('disable-party-fireworks'))
            return

        self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [PartyGlobals.DenialReasons.Default])

    def showEnded(self, task):
        self.request('Disabled')
        return task.done

    def enterActive(self):
        self.sendUpdate('setState', ['Active', globalClockDelta.getRealNetworkTime()])
        messenger.send('fireworks-started-%s' % self.getPartyDoId())

    def enterIdle(self):
        self.sendUpdate('setState', ['Idle', globalClockDelta.getRealNetworkTime()])

    def enterDisabled(self):
        self.sendUpdate('setState', ['Disabled', globalClockDelta.getRealNetworkTime()])
        messenger.send('fireworks-finished-%s' % self.getPartyDoId())
