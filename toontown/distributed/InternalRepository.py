from direct.distributed.AstronInternalRepository import AstronInternalRepository

from otp.distributed import OtpDoGlobals

class InternalRepository(AstronInternalRepository):
    GameGlobalsId = OtpDoGlobals.OTP_DO_ID_TOONTOWN
    dbId = 4003

    def __init__(self, baseChannel, serverId = None, dcFileNames = None, dcSuffix = 'AI', connectMethod = None, threadedNet = None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF