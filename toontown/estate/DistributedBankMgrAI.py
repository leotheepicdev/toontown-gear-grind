from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedBankMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedBankMgrAI')

    def transferMoney(self, avId, amount):
        av = self.air.doId2do.get(avId)
        if av:
            transactionAmount = amount
            jarMoney = av.getMoney()
            maxJarMoney = av.getMaxMoney()
            bankMoney = av.getBankMoney()
            maxBankMoney = av.getMaxBankMoney()
            transactionAmount = min(transactionAmount, jarMoney)
            transactionAmount = min(transactionAmount, maxBankMoney - bankMoney)
            transactionAmount = -min(-transactionAmount, maxJarMoney - jarMoney)
            transactionAmount = -min(-transactionAmount, bankMoney)
            newJarMoney = jarMoney - transactionAmount
            newBankMoney = bankMoney + transactionAmount
            if newJarMoney > maxJarMoney:
                return
            if newBankMoney > maxBankMoney:
                return
            av.b_setMoney(newJarMoney)
            av.b_setBankMoney(newBankMoney)