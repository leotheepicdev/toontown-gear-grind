from otp.speedchat.SCTerminal import SCTerminal
from toontown.chat import ResistanceChat
from toontown.toonbase import TTLocalizer
TTSCGreetingMsgEvent = 'TTSCGreetingMsg'

class TTSCGreetingTerminal(SCTerminal):

    def __init__(self, msg, textId):
        SCTerminal.__init__(self)
        self.text = msg
        self.textId = textId

    def isWhisperable(self):
        return False

    def handleSelect(self, cfType):
        SCTerminal.handleSelect(self)
        messenger.send(TTSCGreetingMsgEvent, [self.textId])
        base.localAvatar.setSystemMessage(0, TTLocalizer.TeleportGreetingSwapNotify % self.text)
