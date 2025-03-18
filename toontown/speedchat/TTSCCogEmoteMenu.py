from otp.speedchat.SCMenu import SCMenu
from otp.otpbase import OTPLocalizer
from .TTSCCogEmoteTerminal import TTSCCogEmoteTerminal

class TTSCCogEmoteMenu(SCMenu):

    def __init__(self):
        SCMenu.__init__(self)
        self.__changeCogEmotes()

    def destroy(self):
        SCMenu.destroy(self)

    def __changeCogEmotes(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
                
        for i in range(len(OTPLocalizer.DisguiseEmoteList)):
            self.append(TTSCCogEmoteTerminal(i))
