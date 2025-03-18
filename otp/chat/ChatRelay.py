from direct.distributed.DistributedObject import DistributedObject

class ChatRelay(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        if self.cr.chatRelay != None:
            self.cr.chatRelay.delete()
        self.cr.chatRelay = self

    def delete(self):
        self.cr.chatRelay = None
        DistributedObject.delete(self)

    def relayMessage(self, message):
        try:
            message.encode().decode('ascii')
        except (UnicodeDecodeError, UnicodeEncodeError):
            base.localAvatar.setSystemMessage(0, 'Toontown: Gear Grind does not support non-ascii characters!')
            return

        self.sendUpdate('relayMessage', [message])

    def relayWhisper(self, message, toId):
        self.sendUpdate('relayWhisper', [message, toId])

    def relayWhisperSC(self, type, msgIndex, toId):
        self.sendUpdate('relayWhisperSC', [type, msgIndex, toId])