from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class CentralLoggerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('CentralLoggerUD')
    notify.setDebug(True)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def sendMessage(self, category, message, targetDISLid, targetAvId):
        self.notify.debug('Received Message from Client!')

        parts = message.split('|')
        msgType = parts[0]
        fields = {
            'targetDISLid': targetDISLid,
            'targetAvId': targetAvId
        }

        if self.notify.getDebug():
            event = {
                'category': category,
                'message': message,
                'type': msgType,
            }
            event.update(fields)

            data = json.dumps(event)
            print(data)

        self.air.writeServerEvent(category, messageType = msgType, message = message, **fields)

    def logAIGarbage(self):
        pass