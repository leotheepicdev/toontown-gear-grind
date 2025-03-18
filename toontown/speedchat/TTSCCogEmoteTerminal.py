from direct.gui.DirectGui import *
from otp.speedchat.SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import DisguiseEmoteList
from otp.avatar import Emote
TTSCCogEmoteMsgEvent = 'TTSCCogEmoteMsg'

class TTSCCogEmoteTerminal(SCTerminal):

    def __init__(self, emoteId):
        SCTerminal.__init__(self)
        self.emoteId = emoteId
        self.text = DisguiseEmoteList[self.emoteId]

    def __emoteEnabled(self):
        if self.isWhispering():
            return 1
        return Emote.globalDisguiseEmote.isEnabled(self.emoteId)

    def finalize(self, dbArgs = {}):
        if not self.isDirty():
            return
        args = {}
        if not self.__emoteEnabled():
            args.update({'rolloverColor': (0, 0, 0, 0),
             'pressedColor': (0, 0, 0, 0),
             'rolloverSound': None,
             'text_fg': self.getColorScheme().getTextDisabledColor() + (1,)})
        if not self.__emoteEnabled():
            args.update({'clickSound': None})
        self.lastEmoteEnableState = self.__emoteEnabled()
        args.update(dbArgs)
        SCTerminal.finalize(self, dbArgs=args)

    def __emoteEnableStateChanged(self):
        if self.isDirty():
            self.notify.info("skipping __emoteEnableStateChanged; we're marked as dirty")
            return
        elif not hasattr(self, 'button'):
            self.notify.error('SCEmoteTerminal is not marked as dirty, but has no button!')
        btn = self.button
        if self.__emoteEnabled():
            rolloverColor = self.getColorScheme().getRolloverColor() + (1,)
            pressedColor = self.getColorScheme().getPressedColor() + (1,)
            btn.frameStyle[DGG.BUTTON_ROLLOVER_STATE].setColor(*rolloverColor)
            btn.frameStyle[DGG.BUTTON_DEPRESSED_STATE].setColor(*pressedColor)
            btn.updateFrameStyle()
            btn['text_fg'] = self.getColorScheme().getTextColor() + (1,)
            btn['rolloverSound'] = DGG.getDefaultRolloverSound()
            btn['clickSound'] = DGG.getDefaultClickSound()
        else:
            btn.frameStyle[DGG.BUTTON_ROLLOVER_STATE].setColor(0, 0, 0, 0)
            btn.frameStyle[DGG.BUTTON_DEPRESSED_STATE].setColor(0, 0, 0, 0)
            btn.updateFrameStyle()
            btn['text_fg'] = self.getColorScheme().getTextDisabledColor() + (1,)
            btn['rolloverSound'] = None
            btn['clickSound'] = None

    def enterVisible(self):
        SCTerminal.enterVisible(self)
        if hasattr(self, 'lastEmoteEnableState'):
            if self.lastEmoteEnableState != self.__emoteEnabled():
                self.invalidate()
        if not self.isWhispering():
            self.accept(Emote.globalDisguiseEmote.EmoteEnableStateChanged, self.__emoteEnableStateChanged)

    def exitVisible(self):
        SCTerminal.exitVisible(self)
        self.ignore(Emote.globalDisguiseEmote.EmoteEnableStateChanged)

    def handleSelect(self, cfType):
        if self.__emoteEnabled():
            SCTerminal.handleSelect(self, cfType)
            messenger.send(self.getEventName(TTSCCogEmoteMsgEvent), [self.emoteId])
