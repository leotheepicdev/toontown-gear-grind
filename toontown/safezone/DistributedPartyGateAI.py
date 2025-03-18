from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.parties import PartyGlobals

class DistributedPartyGateAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedPartyGateAI')

    def getPartyList(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'listAllPublicParties', [self.air.partyManager.getPublicParties()])

    def partyChoiceRequest(self, shardId, zoneId):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        publicParties = self.air.partyManager.publicParties
        if (shardId, zoneId) in self.air.partyManager.shardAndZone2Party:
            partyId = self.air.partyManager.shardAndZone2Party[(shardId, zoneId)]
            party = publicParties[partyId]
            if party.get('shardId', 0 == shardId and party.get('zoneId', 0) == zoneId):
                self.air.partyManager.toonHasEnteredPartyAiToUd(avId, partyId, self.doId)
                return
        self.sendUpdateToAvatarId(avId, 'partyRequestDenied', [PartyGlobals.PartyGateDenialReasons.Unavailable])
