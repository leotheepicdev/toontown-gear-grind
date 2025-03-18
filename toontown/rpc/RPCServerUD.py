from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
from threading import Thread

class RPCServerUD:
    notify = directNotify.newCategory('RPCServerUD')

    def __init__(self, air):
        self.air = air

        # Start up the RPC service thread.
        Thread(target = self.startup, args = ()).start()

    @Request.application
    def application(self, request):
        # Dispatcher is dictionary {<method_name>: callable}.
        dispatcher['echo'] = lambda s: s
        dispatcher['add'] = lambda a, b: a + b
        dispatcher['action'] = self.handleAction

        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype = 'application/json')

    def handleAction(self, secretKey, action, arguments):
        if secretKey != config.GetString('rpc-secret'):
            return 'Nice try.'

        if action == 'systemMessage':
            message = arguments[0]
            self.sendSystemMessage(message)
            return 'Broadcasted system message to shard.'
        elif action == 'kickPlayer':
            if len(arguments) == 2:
                avatarId = arguments[0]
                reasonId = arguments[1]

                if reasonId not in OTPLocalizer.PresetKickReasons:
                    return 'Invalid kick reason!'

                errorCode = OTPLocalizer.PresetKickReasons[reasonId]
                reason = OTPLocalizer.CRBootedReasons[errorCode]
                self.air.moderationManager.serverKick(avatarId, reason, errorCode)
                return 'Kicked player from server.'

        return 'Unhandled action.'

    def sendSystemMessage(self, message):
        dclass = self.air.dclassesByName['ClientManagerUD']
        datagram = dclass.aiFormatUpdate('systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, 10, OtpDoGlobals.OTP_ALL_CLIENTS, [message])
        self.air.send(datagram)

    def startup(self):
        run_simple('0.0.0.0', 7969, self.application)