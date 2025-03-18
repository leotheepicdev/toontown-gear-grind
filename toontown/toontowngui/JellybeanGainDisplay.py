from panda3d.core import TextNode, VBase4
from direct.gui.DirectGui import DirectLabel, OnscreenImage
from direct.interval.IntervalGlobal import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from .GuiUtil import *

class JellybeanGainDisplay:
    INDEX_2_POS = {
      0: (0.4, 0, 0.15),
      1: (0.6, 0, 0.15),
      2: (0.8, 0, 0.15),
      3: (1, 0, 0.15),
      4: (1.2, 0, 0.15),
    }

    def __init__(self):
        self.availableIndexes = []
        for index in self.INDEX_2_POS.keys():
             self.availableIndexes.append(index)
        self.queue = []
        self.displays = {}
        purchaseModels = loader.loadModel('phase_4/models/gui/purchase_gui')
        self.jarImage = purchaseModels.find('**/Jar')
        purchaseModels.removeNode()
        self.piggyBank = loadTextureModel(loader.loadTexture('phase_3.5/maps/piggy_bank.png'), transparency=True)
        self.piggyMax = 0
        
    def disable(self):
        for index, display in self.displays.items():
            display.removeNode()
            self.availableIndexes.append(index)
        self.displays.clear()
        self.queue.clear()
        self.availableIndexes.sort()
        
    def removeModels(self):
        self.jarImage.removeNode()
        self.piggyBank.removeNode()
        
    def preparePiggyMax(self, piggyMax):
        self.piggyMax = piggyMax
        
    def queueDisplay(self, displayType, amount):
        if not self.availableIndexes:
            self.queue.append((displayType, amount))
            return
        index = self.availableIndexes[0]
        
        if displayType == 1:
            image = self.piggyBank
            image_scale=0.3
        else:
            image = self.jarImage
            image_scale = 1
        
        self.availableIndexes.remove(index)
        display = DirectLabel(parent=base.a2dBottomLeft, relief=None, text='+%s' % amount, text_align=TextNode.ACenter, text_pos=(0.0, -0.07), text_scale=0.2, 
                              text_fg=(1, 0, 0, 1), text_font=ToontownGlobals.getSignFont(),
                              textMayChange=True, image=image, scale=0.4, image_scale=image_scale, pos=self.INDEX_2_POS[index])
        self.displays[index] = display
        piggyBankFull = 0

        if displayType == 1:
            piggyBank = base.localAvatar.getPiggyBank()
            if piggyBank[0] == 0:
                piggyBankFull = 1

        if piggyBankFull:
            seq = Parallel(
                Sequence(Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.PiggyBankFullMessage)),
                Sequence(Wait(1), Func(self.queueDisplay, 0, self.piggyMax)),
                Sequence(LerpColorScaleInterval(display, 1, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)), Wait(2), 
                         LerpColorScaleInterval(display, 1, colorScale=VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1)), Func(self.delete, index))
                ).start()
        else:
            seq = Sequence(LerpColorScaleInterval(display, 1, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)), Wait(2), 
                           LerpColorScaleInterval(display, 1, colorScale=VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1)), Func(self.delete, index)).start() 

    def delete(self, index):
        self.availableIndexes.append(index)
        self.availableIndexes.sort()
 
        self.displays[index].removeNode()
        del self.displays[index]

        if self.queue:
            nextItem = self.queue[0]
            nextDisplayType = nextItem[0]
            nextAmount = nextItem[1]
            del self.queue[0]
            self.queueDisplay(nextDisplayType, nextAmount)