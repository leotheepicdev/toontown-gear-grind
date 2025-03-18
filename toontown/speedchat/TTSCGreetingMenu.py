from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from .TTSCGreetingTerminal import TTSCGreetingTerminal
from otp.otpbase import OTPLocalizer
   
GreetingMsgs = [
 31000,
 31001,
 31002,
 31003,
 31004,
 31005,
 31006,
 31007,
]

class TTSCGreetingMenu(SCMenu):

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('greetingMessagesChanged', self.__greetingMessagesChanged)
        self.__greetingMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __greetingMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
            
        greetingId = lt.getTeleportGreeting()

        for msgId in GreetingMsgs:
            gid = OTPLocalizer.GreetingMsg2Id[msgId]
            staticText = TTSCGreetingTerminal(OTPLocalizer.SpeedChatStaticTextToontown[msgId], msgId)
            if gid == greetingId:
                staticText.setDisabled(True)
            self.append(staticText)
