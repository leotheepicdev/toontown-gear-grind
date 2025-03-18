from .DistributedNPCToonBaseAI import DistributedNPCToonBaseAI

class DistributedNPCClerkAI(DistributedNPCToonBaseAI):

    def setInventory(self, inventory, money):
        av = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not av:
            return
        if av.inventory.validatePurchase(av.inventory.makeFromNetString(inventory), av.getMoney(), money):
            av.b_setMoney(money)
            av.d_setInventory(av.inventory.makeNetString())