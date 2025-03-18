from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.makeatoon.MakeAToonGlobals import *
from toontown.makeatoon import ShuffleButton
from . import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import random

class GlovesGUI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, doneEvent, swapEvent = None, browsing=0):
        StateData.StateData.__init__(self, doneEvent)
        self.gloves = ToonDNA.defaultColorList
        self.oldGloveColor = 0
        self.gloveChoice = 0
        self.toon = None
        self.swapEvent = swapEvent
        self.browsing = browsing

    def load(self):
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        shuffleFrame = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleUp = self.gui.find('**/tt_t_gui_mat_shuffleUp')
        shuffleDown = self.gui.find('**/tt_t_gui_mat_shuffleDown')
        shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = self.gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        self.parentFrame = DirectFrame(relief=DGG.RAISED, parent=base.a2dTopRight, pos=(-0.353333, 0, -0.584), frameColor=(1, 0, 0, 0))
        self.gloveFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.65), hpr=(0, 0, -2), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.ColorShopGloves, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.gloveLButton = DirectButton(parent=self.gloveFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapGloves, extraArgs=[-1])
        self.gloveRButton = DirectButton(parent=self.gloveFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapGloves, extraArgs=[1])
        self.parentFrame.hide()
        self.buttonGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        if self.browsing == 0:
            self.button = DirectButton(relief=None, image=(self.buttonGui.find('**/CrtAtoon_Btn1_UP'), self.buttonGui.find('**/CrtAtoon_Btn1_DOWN'), self.buttonGui.find('**/CrtAtoon_Btn1_RLLVR')), pos=(-0.15, 0, -0.85), command=self.__handleButton, text=('', TTLocalizer.MakeAToonDone, TTLocalizer.MakeAToonDone), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        else:
            self.button = None
        self.cancelButton = DirectButton(relief=None, image=(self.buttonGui.find('**/CrtAtoon_Btn2_UP'), self.buttonGui.find('**/CrtAtoon_Btn2_DOWN'), self.buttonGui.find('**/CrtAtoon_Btn2_RLLVR')), pos=(0.15, 0, -0.85), command=self.__handleCancel, text=('', TTLocalizer.MakeAToonCancel, TTLocalizer.MakeAToonCancel), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.shuffleBtn = DirectButton(parent=self.parentFrame, relief=None, image=(shuffleUp, shuffleDown, shuffleUp), pos=(0, 0, -0.45), image_scale=halfButtonInvertScale, image1_scale=(-0.63, 0.6, 0.6), image2_scale=(-0.63, 0.6, 0.6), text=(TTLocalizer.ShuffleButton,
         TTLocalizer.ShuffleButton,
         TTLocalizer.ShuffleButton,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.SBshuffleBtn, text_pos=(0, -0.02), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), command=self.shuffleGloves)

    def unload(self):
        self.gui.removeNode()
        del self.gui
        self.buttonGui.removeNode()
        del self.buttonGui
        self.parentFrame.destroy()
        self.gloveFrame.destroy()
        self.gloveLButton.destroy()
        self.gloveRButton.destroy()
        del self.parentFrame
        del self.gloveFrame
        del self.gloveLButton
        del self.gloveRButton
        if self.button != None:
            self.button.destroy()
            del self.button
        self.cancelButton.destroy()
        del self.cancelButton
        self.shuffleBtn.destroy()
        del self.shuffleBtn

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()
        
    def __handleButton(self):
        messenger.send(self.doneEvent)

    def __handleCancel(self):
        self.resetGloves()
        messenger.send('last')
        
    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        if self.swapEvent != None:
            self.gloveChoice = 0
        self.setupButtons()

    def enter(self, toon):
        self.notify.debug('enter')
        base.disableMouse()
        self.toon = toon
        self.dna = toon.getStyle()
        self.oldGloveColor = self.dna.gloveColor
        length = len(self.gloves)
        self.gloveChoice = 0
        self.updateScrollButtons(self.gloveChoice, length, self.gloveLButton, self.gloveRButton)
        self.dna.gloveColor = 0
        self.toon.swapToonColor(self.dna)
        self.setupScrollInterface()

    def exit(self):
        try:
            del self.toon
        except:
            self.notify.warning('GlovesGUI: toon not found')

        self.hideButtons()
        self.ignore('enter')
        self.ignore('last')

    def setupButtons(self):
        self.acceptOnce('last', self.__handleBackward)
        
    def swapGloves(self, offset):
        length = len(self.gloves)
        self.gloveChoice = (self.gloveChoice + offset) % length
        self.updateScrollButtons(self.gloveChoice, length, self.gloveLButton, self.gloveRButton)
        newColor = self.gloves[self.gloveChoice]
        self.dna.gloveColor = newColor
        self.toon.swapToonColor(self.dna)

    def updateScrollButtons(self, choice, length, lButton, rButton):
        if choice >= length - 1:
            rButton['state'] = DGG.DISABLED
        else:
            rButton['state'] = DGG.NORMAL
        if choice <= 0:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL
        if self.button:
            if choice == self.oldGloveColor:
                self.button.hide()
            else:
                self.button.show()

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def resetGloves(self):
        self.dna.gloveColor = self.oldGloveColor
        self.toon.swapToonColor(self.dna)

    def shuffleGloves(self):
        choicePool = self.gloves.copy()
        choicePool.remove(self.gloveChoice)
        self.swapGloves(random.choice(choicePool))

    def getCurrToonSetting(self):
        return [self.gloves[self.gloveChoice]]
