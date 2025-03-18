from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.distributed.OtpDoGlobals import *
import time

class ChatRelayAI(DistributedObjectAI):
    # TODO: all the suspicious security crap
    WHISPER_COOLDOWN = 1

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def relayMessage(self, message):
        sender = self.air.getAvatarIdFromSender()
        if not sender:
            return
        if sender in self.air.doId2do:
            av = self.air.doId2do[sender]
            account = self.air.getAccountIdFromSender()
            name = av.getName()
            av.sendUpdate('setTalk', [av.doId, account, name, message, 0])

    def relayWhisper(self, message, toId):
        sender = self.air.getAvatarIdFromSender()
        if not sender:
            return
        av = self.air.doId2do[sender]
        if time.time() - av.lastWhisperTime <= self.WHISPER_COOLDOWN:
            self.air.moderationManager.serverKick(sender, 'Whispering too fast!')
            return
        av.lastWhisperTime = time.time()
        account = self.air.getAccountIdFromSender()
        name = av.getName()
        dg = av.dclass.aiFormatUpdate('setTalkWhisperAI', toId, toId, OTP_ALL_CLIENTS, [av.doId, account, name, message, 0])
        self.air.send(dg)

    def relayWhisperSC(self, type, msgIndex, toId):
        sender = self.air.getAvatarIdFromSender()
        if not sender:
            return
        av = self.air.doId2do[sender]
        if time.time() - av.lastWhisperTime <= self.WHISPER_COOLDOWN:
            self.air.moderationManager.serverKick(sender, 'Whispering too fast!')
            return
        av.lastWhisperTime = time.time()
        account = self.air.getAccountIdFromSender()
        name = av.getName()
        dg = av.dclass.aiFormatUpdate('setTalkWhisperSCAI', toId, toId, OTP_ALL_CLIENTS, [av.doId, name, type, msgIndex])
        self.air.send(dg)