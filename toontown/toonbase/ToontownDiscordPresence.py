from pypresence import Presence
from direct.directnotify.DirectNotifyGlobal import directNotify
import time

class ToontownDiscordPresence:
    notify = directNotify.newCategory('ToontownDiscordPresence')
    notify.setInfo(True)

    def __init__(self):
        self.clientId = config.GetString('discord-client-id')

        self.rpcClient = None

        self.initialData = {
            'start': time.time(),
            'large_image': 'rp'
        }

        try:
            self.initialize()
            base.haveDiscordOpen = True
        except:
            # Discord is not running.
            self.notify.warning('Discord is not running.')
            base.haveDiscordOpen = False

    def initialize(self):
        self.rpcClient = Presence(self.clientId)
        self.rpcClient.connect()

        self.sendGeneral()

    def sendGeneral(self):
        # Send our initial data.
        self.updatePresence(self.initialData)

    def updatePresence(self, data, inGame = False):
        buttons = [
            {
                'label': 'Website', 'url': 'https://geargrind.tech/register'
            },
            {
                'label': 'Discord', 'url': 'https://discord.gg/cfa6fxRhWA'
            }
        ]

        if inGame:
            # Edit the data to include our toon.
            toonName = base.localAvatar.getName()
            toonHp = base.localAvatar.getHp()

            data['small_image'] = 'icon'
            data['small_text'] = '{0} - {1} Laff'.format(toonName, toonHp)

        # Send the update to the RPC client.
        self.notify.info('Updating RPC with data: {0}'.format(data))
        self.rpcClient.update(**data, buttons = buttons)