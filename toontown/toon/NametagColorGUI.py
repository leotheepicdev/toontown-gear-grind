from lib.libotp import NametagGlobals
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.makeatoon.MakeAToonGlobals import *
from toontown.makeatoon import ShuffleButton
from . import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import random

class NametagColorGUI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, doneEvent, swapEvent = None, browsing=0):
        StateData.StateData.__init__(self, doneEvent)
        self.nametagColors = NametagGlobals.NAMETAG_COLOR_LIST
        self.oldNametagColor = 0
        self.oldNametagPanelColor = 0
        self.nametagColorChoice = 0
        self.nametagPanelColorChoice = 0
        self.toon = None
        self.swapEvent = swapEvent
        self.browsing = browsing

    def load(self):
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        self.jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        shuffleFrame = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleUp = self.gui.find('**/tt_t_gui_mat_shuffleUp')
        shuffleDown = self.gui.find('**/tt_t_gui_mat_shuffleDown')
        shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = self.gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        self.parentFrame = DirectFrame(relief=DGG.RAISED, parent=base.a2dTopRight, pos=(-0.353333, 0, -0.584), frameColor=(1, 0, 0, 0))
        self.nametagColorFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.4), hpr=(0, 0, -2), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.NametagColorShopColors, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.nametagColorLButton = DirectButton(parent=self.nametagColorFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapNametagColors, extraArgs=[-1])
        self.nametagColorRButton = DirectButton(parent=self.nametagColorFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapNametagColors, extraArgs=[1])
        
        
        self.nametagPanelColorFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.65), hpr=(0, 0, -2), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.NametagColorShopPanelColors, text_scale=0.0475, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.nametagPanelColorLButton = DirectButton(parent=self.nametagPanelColorFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapNametagPanelColors, extraArgs=[-1])
        self.nametagPanelColorRButton = DirectButton(parent=self.nametagPanelColorFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapNametagPanelColors, extraArgs=[1])        
        
        self.parentFrame.hide()
        self.buttonGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        if self.browsing == 0:
            self.button = DirectButton(relief=None, image=(self.buttonGui.find('**/CrtAtoon_Btn1_UP'), self.buttonGui.find('**/CrtAtoon_Btn1_DOWN'), self.buttonGui.find('**/CrtAtoon_Btn1_RLLVR')), pos=(-0.15, 0, -0.85), command=self.__handleButton, text=('', TTLocalizer.MakeAToonDone, TTLocalizer.MakeAToonDone), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        else:
            self.button = None
        self.cancelButton = DirectButton(relief=None, image=(self.buttonGui.find('**/CrtAtoon_Btn2_UP'), self.buttonGui.find('**/CrtAtoon_Btn2_DOWN'), self.buttonGui.find('**/CrtAtoon_Btn2_RLLVR')), pos=(0.15, 0, -0.85), command=self.__handleCancel, text=('', TTLocalizer.MakeAToonCancel, TTLocalizer.MakeAToonCancel), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.shuffleBtn = DirectButton(parent=self.parentFrame, relief=None, image=(shuffleUp, shuffleDown, shuffleUp), pos=(0, 0, -0.85), image_scale=halfButtonInvertScale, image1_scale=(-0.63, 0.6, 0.6), image2_scale=(-0.63, 0.6, 0.6), text=(TTLocalizer.ShuffleButton,
         TTLocalizer.ShuffleButton,
         TTLocalizer.ShuffleButton,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.SBshuffleBtn, text_pos=(0, -0.02), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), command=self.shuffleNametagColors)
        self.jarDisplay = DirectLabel(parent=self.parentFrame, relief=None, pos=(0, 0, -1.2), scale=0.75, text=str(base.localAvatar.getTotalMoney()), text_scale=0.2, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), image=self.jarGui.find('**/Jar'), text_font=ToontownGlobals.getSignFont())
        self.cost = DirectLabel(parent=base.a2dBottomCenter, relief=None, pos=(0, 0, 0.26), text=TTLocalizer.NametagColorShopCost % ToontownGlobals.NAMETAG_COLOR_COST, text_scale=0.12, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getSignFont())

    def unload(self):
        self.ignoreAll()
        self.gui.removeNode()
        del self.gui
        self.jarGui.removeNode()
        del self.jarGui
        self.buttonGui.removeNode()
        del self.buttonGui
        self.parentFrame.destroy()
        self.nametagColorFrame.destroy()
        self.nametagColorLButton.destroy()
        self.nametagColorRButton.destroy()
        del self.parentFrame
        del self.nametagColorFrame
        del self.nametagColorLButton
        del self.nametagColorRButton
        if self.button != None:
            self.button.destroy()
            del self.button
        self.cancelButton.destroy()
        del self.cancelButton
        self.shuffleBtn.destroy()
        del self.shuffleBtn
        self.jarDisplay.destroy()
        del self.jarDisplay
        self.cost.destroy()
        del self.cost

    def moneyChange(self, money):
        if self.jarDisplay:
            self.jarDisplay['text'] = str(base.localAvatar.getTotalMoney())

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()

    def __handleButton(self):
        messenger.send(self.doneEvent)

    def __handleCancel(self):
        self.resetNametagColors()
        messenger.send('last')

    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        if self.swapEvent != None:
            self.nametagColorChoice = 0
        self.setupButtons()

    def enter(self, toon):
        self.notify.debug('enter')
        base.disableMouse()
        self.accept(base.localAvatar.uniqueName('moneyChange'), self.moneyChange)
        self.accept(base.localAvatar.uniqueName('bankMoneyChange'), self.moneyChange)
        self.toon = toon
        self.dna = toon.getStyle()
        self.oldNametagColor = toon.getNametagColor()
        self.oldNametagPanelColor = toon.getNametagPanelColor()
        length = NametagGlobals.NAMETAG_COLOR_LEN
        self.nametagColorChoice = 0
        self.updateScrollButtons(self.nametagColorChoice, length, self.nametagColorLButton, self.nametagColorRButton)
        self.toon.setNametagColor(0)
        self.setupScrollInterface()

    def exit(self):
        try:
            del self.toon
        except:
            self.notify.warning('NametagColorGUI: toon not found')

        self.hideButtons()
        self.ignore('enter')
        self.ignore('last')

    def setupButtons(self):
        self.acceptOnce('last', self.__handleBackward)

    def swapNametagColors(self, offset):
        length = NametagGlobals.NAMETAG_COLOR_LEN
        self.nametagColorChoice = (self.nametagColorChoice + offset) % length
        self.updateScrollButtons(self.nametagColorChoice, length, self.nametagColorLButton, self.nametagColorRButton, color=True)
        newColor = self.nametagColors[self.nametagColorChoice]
        self.toon.setNametagColor(newColor)
        
    def swapNametagPanelColors(self, offset):
        length = NametagGlobals.NAMETAG_PANEL_COLOR_LEN
        self.nametagPanelColorChoice = (self.nametagPanelColorChoice + offset) % length
        self.updateScrollButtons(self.nametagPanelColorChoice, length, self.nametagPanelColorLButton, self.nametagPanelColorRButton)
        self.toon.setNametagPanelColor(self.nametagPanelColorChoice)

    def updateScrollButtons(self, choice, length, lButton, rButton, color=False):
        if choice >= length - 1:
            rButton['state'] = DGG.DISABLED
        else:
            rButton['state'] = DGG.NORMAL
        if choice <= 0:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL
        if self.button:
            if color:
                if choice == self.oldNametagColor and self.nametagPanelColorChoice == self.oldNametagPanelColor:
                    self.button.hide()
                    self.cost.hide()
                else:
                    self.button.show()
                    self.cost.show()
            else:
                if choice == self.oldNametagPanelColor and self.nametagColorChoice == self.oldNametagColor:
                    self.button.hide()
                    self.cost.hide()
                else:
                    self.button.show()
                    self.cost.show()

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def resetNametagColors(self):
        self.toon.setNametagColor(self.oldNametagColor)
        self.toon.setNametagPanelColor(self.oldNametagPanelColor)

    def shuffleNametagColors(self):
        choicePool = self.nametagColors.copy()
        choicePool.remove(self.nametagColorChoice)
        self.swapNametagColors(random.choice(choicePool))

    def getCurrToonSetting(self):
        return [self.nametagColors[self.nametagColorChoice]]
