from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import MsgTypes
from otp.distributed import OtpDoGlobals

class ModerationManagerUD:
    notify = directNotify.newCategory('ModerationManagerUD')

    def __init__(self, air):
        self.air = air

    def ejectPlayer(self, avId, reason, errorCode):
        channel = avId + (1001 << 32)

        dg = PyDatagram()
        dg.addServerHeader(channel, OtpDoGlobals.OTP_ALL_CLIENTS, MsgTypes.CLIENTAGENT_EJECT)
        dg.addUint16(errorCode)
        dg.addString(reason)
        self.air.send(dg)

    def serverKick(self, avId, reason = '', errorCode = 155):
        self.notify.warning('Kicking avId {0}: {1}'.format(avId, reason))
        self.air.writeServerEvent('serverKick', avId = avId, reason = reason)
        self.ejectPlayer(avId, reason, errorCode)