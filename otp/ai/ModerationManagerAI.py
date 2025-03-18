from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.OtpDoGlobals import *

class ModerationManagerAI:
    notify = directNotify.newCategory('ModerationManagerAI')
    # TODO: log actions done by staff.

    def __init__(self, air):
        self.air = air

    def ejectPlayer(self, avId, reason, errorCode):
        channel = avId + (1001 << 32)

        dg = PyDatagram()
        dg.addServerHeader(channel, OTP_ALL_CLIENTS, CLIENTAGENT_EJECT)
        dg.addUint16(errorCode)
        dg.addString(reason)
        self.air.send(dg)

    def staffKick(self, avId, reason='', errorCode=154):
        self.ejectPlayer(avId, reason, errorCode)

    def serverKick(self, avId, reason='', errorCode=155):
        """
        Should a client exploit the game, the server will kick it.
        The player's attempt will be logged in order to track them down.
        """
        # TODO: should we system message any online administrators if this function has to be called?
        self.notify.warning('Kicking avId {0}: {1}'.format(avId, reason))
        self.air.writeServerEvent('serverKick', avId=avId, reason=reason)
        self.ejectPlayer(avId, reason, errorCode)

    def staffBan(self):
        pass

    def serverBan(self):
        pass