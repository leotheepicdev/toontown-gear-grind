from direct.directnotify.DirectNotifyGlobal import directNotify

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed import MsgTypes

from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer

import _thread, socket, json

class DiscordIntegrationServer:
    notify = directNotify.newCategory('DiscordIntegrationServer')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air

        self.startServer()

    def setupServer(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 6668))
        server.listen(10)

        while True:
            client, ipAddress = server.accept()
            data = client.recv(4096)

            try:
                data = json.loads(data)
            except:
                # Skid, log the attempt.
                self.notify.warning('Client {0} tried to send non-JSON data!'.format(ipAddress))
                return

            whatToDo = data['whatToDo']
            signature = data['signature']
            actualSignature = config.GetString('discord-signature')

            if signature != actualSignature:
                # Skid, log the attempt.
                self.notify.warning('Client {0} sent invalid signature: {0}!'.format(ipAddress, signature))
                return

            if whatToDo == 'kickRequest':
                avId = int(data['avId'])
                reason = str(data['reason'])

                channel = avId + (1001 << 32)

                errorCode = 154

                datagram = PyDatagram()
                datagram.addServerHeader(channel, simbase.air.ourChannel, MsgTypes.CLIENTAGENT_EJECT)
                datagram.addUint16(errorCode)
                datagram.addString(reason)
                simbase.air.send(datagram)
            elif whatToDo == 'systemMessage':
                message = data['message']

                dclass = simbase.air.dclassesByName['ClientManagerUD']

                datagram = dclass.aiFormatUpdate('systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, 10, OtpDoGlobals.OTP_ALL_CLIENTS, [message])
                simbase.air.send(datagram)
            elif whatToDo == 'approveName':
                avId = int(data['avId'])

                def handleAvatar(dclass, fields):
                    toonDclass = simbase.air.dclassesByName['DistributedToonUD']

                    if dclass != toonDclass:
                        return

                    pendingName = fields['WishName'][0]

                    fields = {
                        'WishNameState': ('APPROVED',)
                    }

                    simbase.air.dbInterface.updateObject(simbase.air.dbId, avId, toonDclass, fields)

                    message = 'Your name has been approved by the Toon Council!'

                    channel = avId + (1001 << 32)

                    dclass = simbase.air.dclassesByName['ClientManagerUD']
                    datagram = dclass.aiFormatUpdate('systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, channel, OtpDoGlobals.OTP_ALL_CLIENTS, [message])
                    simbase.air.send(datagram)

                # Query the avatar to get the pending name.
                simbase.air.dbInterface.queryObject(simbase.air.dbId, avId, handleAvatar)
            elif whatToDo == 'rejectName':
                avId = int(data['avId'])

                def handleAvatar(dclass, fields):
                    toonDclass = simbase.air.dclassesByName['DistributedToonUD']

                    if dclass != toonDclass:
                        return

                    fields = {
                        'WishNameState': ('REJECTED',)
                    }

                    simbase.air.dbInterface.updateObject(simbase.air.dbId, avId, toonDclass, fields)

                    message = 'Your name has been rejected by the Toon Council!'

                    channel = avId + (1001 << 32)

                    dclass = simbase.air.dclassesByName['ClientManagerUD']
                    datagram = dclass.aiFormatUpdate('systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, channel, OtpDoGlobals.OTP_ALL_CLIENTS, [message])
                    simbase.air.send(datagram)

                # Query the avatar to get the pending name.
                simbase.air.dbInterface.queryObject(simbase.air.dbId, avId, handleAvatar)

    def startServer(self):
        serverThread = _thread.start_new_thread(self.setupServer, ())

        self.notify.info('Successfully started socket server.')