from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.ai.ModerationManagerUD import ModerationManagerUD

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed import OtpDoGlobals

from toontown.distributed.InternalRepository import InternalRepository
from toontown.parties.ToontownTimeManager import ToontownTimeManager
from toontown.discord.DiscordIntegrationServer import DiscordIntegrationServer
from toontown.rpc.RPCServerUD import RPCServerUD

import time

class UDRepository(InternalRepository):
    notify = directNotify.newCategory('UDRepository')

    GameGlobalsId = OtpDoGlobals.OTP_DO_ID_TOONTOWN

    def __init__(self, baseChannel, serverId):
        InternalRepository.__init__(self, baseChannel, serverId, dcSuffix = 'UD')

        self.notify.setInfo(True)
        self.notify.info('UberDOG is now starting up.')

    def handleConnected(self):
        InternalRepository.handleConnected(self)

        # Register our net messenger functions:
        self.netMessenger.register(0, 'avatarOnline')
        self.netMessenger.register(1, 'avatarInvisible')
        self.netMessenger.register(2, 'avatarOffline')

        self.notify.info('Generating root object...')
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        self.notify.info('Creating locals...')
        self.createLocals()

        self.notify.info('Generating managers...')
        self.generateManagers()

        self.notify.info('UberDOG is now ready.')

    def createLocals(self):
        self.toontownTimeManager = ToontownTimeManager(serverTimeUponLogin = int(time.time()), globalClockRealTimeUponLogin = globalClock.getRealTime())

        if config.GetBool('want-discord-integration', False):
            self.discordIntegration = DiscordIntegrationServer(self)

    def generateManagers(self):
        self.clientManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, 'ClientManager')
        self.toontownFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_TOONTOWN_FRIENDS_MANAGER, 'ToontownFriendsManager')
        self.centralLogger = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')
        self.partyManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER, 'DistributedPartyManager')
        self.dataStoreManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_TOONTOWN_TEMP_STORE_MANAGER, 'DistributedDataStoreManager')
        self.deliveryManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')
        self.moderationManager = ModerationManagerUD(self)
        self.rpcServer = RPCServerUD(self)