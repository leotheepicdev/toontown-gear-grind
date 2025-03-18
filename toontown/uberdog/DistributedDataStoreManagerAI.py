from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed import OtpDoGlobals

import json

class DistributedDataStoreManagerAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('DistributedDataStoreManagerAI')

    context = 0
    ctx2Callback = {}

    def startStore(self, typeId):
        self.sendUpdateToUD('startStore', [typeId])

    def stopStore(self, typeId):
        self.sendUpdateToUD('stopStore', [typeId])

    def queryStore(self, query, callback):
        self.context += 1
        self.ctx2Callback[self.context] = callback

        self.sendUpdateToUD('queryStore', [self.context, query])

    def receiveResults(self, context, results):
        callback = self.ctx2Callback.get(context)

        if not callback:
            self.notify.warning('Got receiveResults with unknown context: {}'.format(context))
            return

        results = json.loads(results)
        callback(results)
        del self.ctx2Callback[context]

    def deleteBackupStores(self):
        self.sendUpdateToUD('deleteBackupStores')

    def sendUpdateToUD(self, field, args = []):
        dg = self.dclass.aiFormatUpdate(field, OtpDoGlobals.OTP_DO_ID_TOONTOWN_TEMP_STORE_MANAGER, OtpDoGlobals.OTP_DO_ID_TOONTOWN_TEMP_STORE_MANAGER, self.doId, args)
        self.air.send(dg)

