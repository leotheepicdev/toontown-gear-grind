from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.catalog import CatalogItem

class DistributedDeliveryManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedDeliveryManagerAI')

    def hello(self, todo0):
        pass

    def rejectHello(self, todo0):
        pass

    def helloResponse(self, todo0):
        pass

    def getName(self, todo0):
        pass

    def receiveRejectGetName(self, todo0):
        pass

    def receiveAcceptGetName(self, todo0):
        pass

    def addName(self, todo0, todo1):
        pass

    def receiveRejectAddName(self, todo0):
        pass

    def receiveAcceptAddName(self, todo0):
        pass

    def addGift(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def receiveRejectAddGift(self, todo0):
        pass

    def receiveAcceptAddGift(self, todo0, todo1, todo2, todo3):
        pass

    def deliverGifts(self, todo0, todo1):
        pass

    def receiveAcceptDeliverGifts(self, todo0, todo1):
        pass

    def receiveRejectDeliverGifts(self, todo0, todo1):
        pass

    def receiveRequestPayForGift(self, todo0, todo1, todo2):
        pass

    def receiveRequestPurchaseGift(self, todo0, todo1, todo2, todo3):
        pass

    def receiveAcceptPurchaseGift(self, todo0, todo1, todo2):
        pass

    def receiveRejectPurchaseGift(self, todo0, todo1, todo2, todo3):
        pass

    def heartbeat(self):
        pass

    def giveBeanBonus(self, todo0, todo1):
        pass

    def requestAck(self):
        pass

    def returnAck(self):
        pass

    def givePartyRefund(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def sendDeliverGifts(self, avId, now):
        if not avId:
            return

        av = self.air.doId2do.get(avId)

        if not av:
            return

        _, remainingGifts = av.onGiftOrder.extractDeliveryItems(now)
        av.sendUpdate('setGiftSchedule', [remainingGifts.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)])