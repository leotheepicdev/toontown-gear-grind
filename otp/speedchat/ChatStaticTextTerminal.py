from .ChatTerminal import ChatTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)

class ChatStaticTextTerminal(ChatTerminal):

    def __init__(self, textId):
        ChatTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self, cfType):
        ChatTerminal.handleSelect(self, cfType)
        messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId, cfType])