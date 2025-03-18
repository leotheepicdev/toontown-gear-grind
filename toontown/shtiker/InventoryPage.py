from . import ShtikerPage
from toontown.toonbase import ToontownBattleGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toontowngui.GuiUtil import *
import time

class InventoryPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.currentTrackInfo = None
        self.onscreen = 0
        self.lastInventoryTime = globalClock.getRealTime()
        return

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.gagFrame = DirectFrame(parent=self, relief=None, pos=(0.1, 0, -0.47), scale=(0.35, 0.35, 0.35), geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor)
        self.trackInfo = DirectFrame(parent=self, relief=None, pos=(-0.4, 0, -0.47), scale=(0.35, 0.35, 0.35), geom=DGG.getDefaultDialogGeom(), geom_scale=(1.4, 1, 1), geom_color=ToontownGlobals.GlobalDialogColor, text='', text_wordwrap=11, text_align=TextNode.ALeft, text_scale=0.12, text_pos=(-0.65, 0.3), text_fg=(0.05, 0.14, 0.4, 1))
        self.trackProgress = DirectWaitBar(parent=self.trackInfo, pos=(0, 0, -0.2), relief=DGG.SUNKEN, frameSize=(-0.6,
         0.6,
         -0.1,
         0.1), borderWidth=(0.025, 0.025), scale=1.1, frameColor=(0.4, 0.6, 0.4, 1), barColor=(0.9, 1, 0.7, 1), text='0/0', text_scale=0.15, text_fg=(0.05, 0.14, 0.4, 1), text_align=TextNode.ACenter, text_pos=(0, -0.22))
        self.trackProgress.hide()
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        piggyBankGui = loadTextureModel(loader.loadTexture('phase_3.5/maps/piggy_bank.png'), transparency=True)
        self.moneyDisplay = DirectLabel(parent=self, relief=None, pos=(0.55, 0, -0.5), scale=0.8, text=str(base.localAvatar.getMoney()), text_scale=0.18, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), image=jarGui.find('**/Jar'), text_font=ToontownGlobals.getSignFont())
        
        self.piggyDisplay = DirectLabel(parent=self, relief=None, pos=(-0.65, 0, 0.75), scale=0.8, text='', text_scale=0.12, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.05, 0), image=piggyBankGui, image_scale=0.2, text_font=ToontownGlobals.getSignFont())
        self.piggyTimer = DirectLabel(parent=self, relief=None, text=TTLocalizer.PiggyBankFetchingInfo, text_scale=0.08, text_fg=(0.95, 0.95, 0.5, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ALeft, pos=(-0.5, 0, 0.63))
        jarGui.removeNode()
        piggyBankGui.removeNode()

    def unload(self):
        ShtikerPage.ShtikerPage.unload(self)

    def __moneyChange(self, money):
        self.moneyDisplay['text'] = str(money)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        base.localAvatar.inventory.setActivateMode('book')
        base.localAvatar.inventory.show()
        base.localAvatar.inventory.reparentTo(self)
        self.moneyDisplay['text'] = str(base.localAvatar.getMoney())
        self.accept('enterBookDelete', self.enterDeleteMode)
        self.accept('exitBookDelete', self.exitDeleteMode)
        self.accept('enterTrackFrame', self.updateTrackInfo)
        self.accept('exitTrackFrame', self.clearTrackInfo)
        self.accept(localAvatar.uniqueName('moneyChange'), self.__moneyChange)
        self.piggyTimer['text'] = TTLocalizer.PiggyBankFetchingInfo
        taskMgr.doMethodLater(1, self.updatePiggyTime, self.uniqueName('updatePiggyTime'))

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
        self.clearTrackInfo(self.currentTrackInfo)
        self.ignore('enterBookDelete')
        self.ignore('exitBookDelete')
        self.ignore('enterTrackFrame')
        self.ignore('exitTrackFrame')
        self.ignore(localAvatar.uniqueName('moneyChange'))
        self.makePageWhite(None)
        base.localAvatar.inventory.hide()
        base.localAvatar.inventory.reparentTo(hidden)
        self.exitDeleteMode()
        taskMgr.remove(self.uniqueName('updatePiggyTime'))
        self.piggyDisplay['text'] = ''
        self.piggyDisplay.setColorScale(1, 1, 1, 1)
        self.piggyTimer['text'] = ''

    def enterDeleteMode(self):
        self.book['image_color'] = Vec4(1, 1, 0, 1)

    def exitDeleteMode(self):
        self.book['image_color'] = Vec4(1, 1, 1, 1)

    def updateTrackInfo(self, trackIndex):
        self.currentTrackInfo = trackIndex
        trackName = TextEncoder.upper(ToontownBattleGlobals.Tracks[trackIndex])
        if base.localAvatar.hasTrackAccess(trackIndex):
            curExp, nextExp = base.localAvatar.inventory.getCurAndNextExpValues(trackIndex)
            trackText = '%s / %s' % (curExp, nextExp)
            self.trackProgress['range'] = nextExp
            self.trackProgress['value'] = curExp
            if curExp >= ToontownBattleGlobals.regMaxSkill:
                str = TTLocalizer.InventoryPageTrackFull % trackName
                trackText = TTLocalizer.RewardPanelMeritsMaxed
                self.trackProgress['range'] = 1
                self.trackProgress['value'] = 1
            else:
                morePoints = nextExp - curExp
                if morePoints == 1:
                    str = TTLocalizer.InventoryPageSinglePoint % {'trackName': trackName,
                     'numPoints': morePoints}
                else:
                    str = TTLocalizer.InventoryPagePluralPoints % {'trackName': trackName,
                     'numPoints': morePoints}
            self.trackInfo['text'] = str
            self.trackProgress['text'] = trackText
            self.trackProgress['frameColor'] = (ToontownBattleGlobals.TrackColors[trackIndex][0] * 0.6,
             ToontownBattleGlobals.TrackColors[trackIndex][1] * 0.6,
             ToontownBattleGlobals.TrackColors[trackIndex][2] * 0.6,
             1)
            self.trackProgress['barColor'] = (ToontownBattleGlobals.TrackColors[trackIndex][0],
             ToontownBattleGlobals.TrackColors[trackIndex][1],
             ToontownBattleGlobals.TrackColors[trackIndex][2],
             1)
            self.trackProgress.show()
        else:
            str = TTLocalizer.InventoryPageNoAccess % trackName
            self.trackInfo['text'] = str
            self.trackProgress.hide()

    def clearTrackInfo(self, trackIndex):
        if self.currentTrackInfo == trackIndex:
            self.trackInfo['text'] = ''
            self.trackProgress.hide()
            self.currentTrackInfo = None

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.InventoryHotkeyOn, self.showInventoryOnscreen)
        self.accept(ToontownGlobals.InventoryHotkeyOff, self.hideInventoryOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.InventoryHotkeyOn)
        self.ignore(ToontownGlobals.InventoryHotkeyOff)

    def showInventoryOnscreen(self):
        messenger.send('wakeup')
        timedif = globalClock.getRealTime() - self.lastInventoryTime
        if timedif < 0.7:
            return
        self.lastInventoryTime = globalClock.getRealTime()
        if self.onscreen or base.localAvatar.questPage.onscreen:
            return
        self.onscreen = 1
        base.localAvatar.inventory.setActivateMode('book')
        base.localAvatar.inventory.show()
        base.localAvatar.inventory.reparentTo(self)
        self.moneyDisplay['text'] = str(base.localAvatar.getMoney())
        self.accept('enterTrackFrame', self.updateTrackInfo)
        self.accept('exitTrackFrame', self.clearTrackInfo)
        self.accept(localAvatar.uniqueName('moneyChange'), self.__moneyChange)
        self.reparentTo(aspect2d)
        self.show()
        self.piggyTimer['text'] = TTLocalizer.PiggyBankFetchingInfo
        taskMgr.doMethodLater(1, self.updatePiggyTime, self.uniqueName('updatePiggyTime'))

    def hideInventoryOnscreen(self):
        if not self.onscreen:
            return
        self.onscreen = 0
        self.ignore('enterTrackFrame')
        self.ignore('exitTrackFrame')
        self.ignore(localAvatar.uniqueName('moneyChange'))
        base.localAvatar.inventory.hide()
        base.localAvatar.inventory.reparentTo(hidden)
        self.reparentTo(self.book)
        self.hide()
        taskMgr.remove(self.uniqueName('updatePiggyTime'))
        self.piggyDisplay['text'] = ''
        self.piggyDisplay.setColorScale(1, 1, 1, 1)
        self.piggyTimer['text'] = ''
        
    def updatePiggyTime(self, task=None):
        piggyBank = base.localAvatar.getPiggyBank()
        timeLeft = piggyBank[2] - int(time.time())
        if timeLeft <= 0:
            self.piggyDisplay['text'] = '%s/%s' % (piggyBank[0], piggyBank[1])
            self.piggyDisplay.setColorScale(1, 1, 1, 1)
            self.piggyTimer['text'] = TTLocalizer.FillUpPiggyBank
        else:
            self.piggyDisplay['text'] = ''
            self.piggyDisplay.setColorScale(1, 1, 1, 0.3)
            self.piggyTimer['text'] = TTLocalizer.PiggyBankAvailableIn % TTLocalizer.getTimeLeft(timeLeft, 5, 1)
        if task:
            return task.again
