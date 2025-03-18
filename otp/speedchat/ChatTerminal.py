from .ChatElement import ChatElement
from .SCObject import SCObject
from .SCMenu import SCMenu
from direct.fsm.StatePush import StateVar, FunctionCall
from direct.showbase.DirectObject import DirectObject
from lib.libotp._constants import CFSpeech

ChatTerminalSelectedEvent = 'ChatTerminalSelected'
SCWhisperModeChangeEvent = 'SCWhisperModeChange'

class ChatTerminal(ChatElement):

    def __init__(self):
        ChatElement.__init__(self)
        scGui = loader.loadModel(SCMenu.GuiModelName)
        self.__numCharges = -1
        self._handleWhisperModeSV = StateVar(False)
        self._handleWhisperModeFC = None

    def destroy(self):
        self._handleWhisperModeSV.set(False)
        if self._handleWhisperModeFC:
            self._handleWhisperModeFC.destroy()
        self._handleWhisperModeSV.destroy()
        ChatElement.destroy(self)

    def privSetSettingsRef(self, settingsRef):
        ChatElement.privSetSettingsRef(self, settingsRef)
        if self._handleWhisperModeFC is None:
            self._handleWhisperModeFC = FunctionCall(self._handleWhisperModeSVChanged, self._handleWhisperModeSV)
            self._handleWhisperModeFC.pushCurrentState()
        self._handleWhisperModeSV.set(self.settingsRef is not None and not self.isWhisperable())
        return

    def _handleWhisperModeSVChanged(self, handleWhisperMode):
        if handleWhisperMode:
            self._wmcListener = DirectObject()
            self._wmcListener.accept(self.getEventName(SCWhisperModeChangeEvent), self._handleWhisperModeChange)
        elif hasattr(self, '_wmcListener'):
            self._wmcListener.ignoreAll()
            del self._wmcListener
            self.invalidate()

    def _handleWhisperModeChange(self, whisperMode):
        self.invalidate()

    def handleSelect(self, cfType=CFSpeech):
        messenger.send(self.getEventName(ChatTerminalSelectedEvent))

    def isWhisperable(self):
        return True

    def getCharges(self):
        return self.__numCharges

    def setCharges(self, nCharges):
        self.__numCharges = nCharges

    def exitVisible(self):
        ChatElement.exitVisible(self)
        self.ignore(self.getEventName(SCWhisperModeChangeEvent))

    def getDisplayText(self):
        if self.getCharges() != -1:
            return self.text + ' (%s)' % self.getCharges()
        else:
            return self.text
