from . import ShtikerPage
from direct.task.Task import Task
from . import SummonCogDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpgui.OTPDialog import YesNo
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.suit import SuitDNA
from toontown.suit import Suit
from toontown.battle import SuitBattleGlobals
from .CogPageGlobals import *
SCALE_FACTOR = 1.5
RADAR_DELAY = 0.2
BUILDING_RADAR_POS = (0.375,
 0.065,
 -0.225,
 -0.5)
PANEL_COLORS = (Vec4(0.8, 0.78, 0.77, 1),
 Vec4(0.75, 0.78, 0.8, 1),
 Vec4(0.75, 0.82, 0.79, 1),
 Vec4(0.825, 0.76, 0.77, 1))
PANEL_COLORS_COMPLETE1 = (Vec4(0.7, 0.725, 0.545, 1),
 Vec4(0.625, 0.725, 0.65, 1),
 Vec4(0.6, 0.75, 0.525, 1),
 Vec4(0.675, 0.675, 0.55, 1))
PANEL_COLORS_COMPLETE2 = (Vec4(0.9, 0.725, 0.32, 1),
 Vec4(0.825, 0.725, 0.45, 1),
 Vec4(0.8, 0.75, 0.325, 1),
 Vec4(0.875, 0.675, 0.35, 1))

class SuitPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        frameModel = loader.loadModel('phase_3.5/models/gui/suitpage_frame')
        frameModel.setScale(0.0452 / base.getAspectRatio(), 0.03, 0.045)
        frameModel.setPos(0, 10, -0.575)
        self.guiTop = NodePath('guiTop')
        self.guiTop.reparentTo(self)
        self.frameNode = NodePath('frameNode')
        self.frameNode.reparentTo(self.guiTop)
        self.panelNode = NodePath('panelNode')
        self.panelNode.reparentTo(self.guiTop)
        self.iconNode = NodePath('iconNode')
        self.iconNode.reparentTo(self.guiTop)
        self.enlargedPanelNode = NodePath('enlargedPanelNode')
        self.enlargedPanelNode.reparentTo(self.guiTop)
        frame = frameModel.find('**/frame')
        frame.wrtReparentTo(self.frameNode)
        screws = frameModel.find('**/screws')
        screws.wrtReparentTo(self.iconNode)
        icons = frameModel.find('**/icons')
        del frameModel
        self.title = DirectLabel(parent=self.iconNode, relief=None, text=TTLocalizer.SuitPageTitle, text_scale=0.1, text_pos=(0.04, 0), textMayChange=0)
        self.radarButtons = []
        icon = icons.find('**/corp_icon')
        self.corpRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[0])
        self.radarButtons.append(self.corpRadarButton)
        icon = icons.find('**/legal_icon')
        self.legalRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[1])
        self.radarButtons.append(self.legalRadarButton)
        icon = icons.find('**/money_icon')
        self.moneyRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[2])
        self.radarButtons.append(self.moneyRadarButton)
        icon = icons.find('**/sales_icon')
        self.salesRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[3])
        self.radarButtons.append(self.salesRadarButton)
        for radarButton in self.radarButtons:
            radarButton.building = 0
            radarButton.buildingRadarLabel = None

        gui = loader.loadModel('phase_3.5/models/gui/suitpage_gui')
        self.panelModel = gui.find('**/card')

        del gui
        self.makePanels()
        self.radarOn = [0,
         0,
         0,
         0]
        gui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        summonsImage = gui.find('**/summons')
        self.summonsLabel = DirectButton(parent=self, relief=None, pos=(0, 0, -0.69), scale=0.1, image=summonsImage, image_pos=(-0.4, 0, 0.4), text=str(base.localAvatar.getSummons()), text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getSignFont(), text_align=TextNode.ALeft, command=self.__throwSummonsDialog)
        self.summonsLabel.bind(DGG.ENTER, self.summonsLabelGrow)
        self.summonsLabel.bind(DGG.EXIT, self.summonsLabelShrink)
        self.accept('update-summons', self.__updateSummonsLabel)
        gui.removeNode()
        self.guiTop.setZ(0.625)

    def unload(self):
        self.ignoreAll()
        self.title.destroy()
        self.summonsLabel.destroy()
        self.corpRadarButton.destroy()
        self.legalRadarButton.destroy()
        self.moneyRadarButton.destroy()
        self.salesRadarButton.destroy()
        for panel in self.panels:
            panel.destroy()

        del self.panels

        self.panelModel.removeNode()
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        self.updatePage()
        self.bigPanel = None
        self.nextPanel = None
        ShtikerPage.ShtikerPage.enter(self)
        return

    def exit(self):
        taskMgr.remove('buildingListResponseTimeout-later')
        taskMgr.remove('suitListResponseTimeout-later')
        taskMgr.remove('showCogRadarLater')
        taskMgr.remove('showBuildingRadarLater')
        for index in range(0, len(self.radarOn)):
            if self.radarOn[index]:
                self.toggleRadar(index)
                self.radarButtons[index]['state'] = DGG.NORMAL

        ShtikerPage.ShtikerPage.exit(self)

    def __updateSummonsLabel(self):
        self.summonsLabel['text'] = str(base.localAvatar.getSummons())

    def grow(self, panel, pos):
        if self.bigPanel:
            print('setting next panel - ' + str(panel))
            self.nextPanel = panel
            self.nextPanelPos = pos
            return
        print('big panel - ' + str(panel))
        self.bigPanel = panel
        panel.reparentTo(self.enlargedPanelNode)
        panel.setScale(panel.getScale() * SCALE_FACTOR)
        if panel.summonButton:
            panel.summonButton.show()
            panel.summonButton['state'] = DGG.NORMAL

    def shrink(self, panel, pos):
        print('trying to shrink - ' + str(panel))
        if panel != self.bigPanel:
            self.nextPanel = None
            return
        print('shrink panel - ' + str(panel))
        self.bigPanel = None
        panel.setScale(panel.scale)
        panel.reparentTo(self.panelNode)
        if panel.summonButton:
            panel.summonButton.hide()
            panel.summonButton['state'] = DGG.DISABLED
        if self.nextPanel:
            self.grow(self.nextPanel, self.nextPanelPos)
        return

    def toggleRadar(self, deptNum):
        messenger.send('wakeup')
        if self.radarOn[deptNum]:
            self.radarOn[deptNum] = 0
        else:
            self.radarOn[deptNum] = 1
        deptSize = SuitDNA.suitsPerDept
        panels = self.panels[deptSize * deptNum:SuitDNA.suitsPerDept * (deptNum + 1)]
        if self.radarOn[deptNum]:
            if hasattr(base.cr, 'currSuitPlanner'):
                if base.cr.currSuitPlanner != None:
                    base.cr.currSuitPlanner.d_suitListQuery()
                    self.acceptOnce('suitListResponse', self.updateCogRadar, extraArgs=[deptNum, panels])
                    taskMgr.doMethodLater(1.0, self.suitListResponseTimeout, 'suitListResponseTimeout-later', extraArgs=(deptNum, panels))
                    if self.radarButtons[deptNum].building:
                        base.cr.currSuitPlanner.d_buildingListQuery()
                        self.acceptOnce('buildingListResponse', self.updateBuildingRadar, extraArgs=[deptNum])
                        taskMgr.doMethodLater(1.0, self.buildingListResponseTimeout, 'buildingListResponseTimeout-later', extraArgs=(deptNum,))
                else:
                    self.updateCogRadar(deptNum, panels)
                    self.updateBuildingRadar(deptNum)
            else:
                self.updateCogRadar(deptNum, panels)
                self.updateBuildingRadar(deptNum)
            self.radarButtons[deptNum]['state'] = DGG.DISABLED
        else:
            self.updateCogRadar(deptNum, panels)
            self.updateBuildingRadar(deptNum)
        return

    def suitListResponseTimeout(self, deptNum, panels):
        self.updateCogRadar(deptNum, panels, 1)

    def buildingListResponseTimeout(self, deptNum):
        self.updateBuildingRadar(deptNum, 1)

    def makePanels(self):
        self.panels = []
        base.panels = []
        xStart = -0.66
        yStart = -0.18
        xOffset = 0.199
        yOffset = 0.284
        for dept in range(0, len(SuitDNA.suitDepts)):
            row = []
            color = PANEL_COLORS[dept]
            for type in range(0, SuitDNA.suitsPerDept):
                panel = DirectLabel(parent=self.panelNode, pos=(xStart + type * xOffset, 0.0, yStart - dept * yOffset), relief=None, state=DGG.NORMAL, image=self.panelModel, image_scale=(1, 1, 1), image_color=color, text=TTLocalizer.SuitPageMystery, text_scale=0.045, text_fg=(0, 0, 0, 1), text_pos=(0, 0.185, 0), text_font=ToontownGlobals.getSuitFont(), text_wordwrap=7)
                panel.scale = 0.6
                panel.setScale(panel.scale)
                panel.quotaLabel = None
                panel.head = None
                panel.count = 0
                panel.summonButton = None
                self.addCogRadarLabel(panel)
                self.panels.append(panel)
                base.panels.append(panel)

    def addQuotaLabel(self, panel):
        index = self.panels.index(panel)
        count = str(base.localAvatar.cogCounts[index])
        if base.localAvatar.cogs[index] < COG_COMPLETE1:
            quota = str(COG_QUOTAS[0][index % SuitDNA.suitsPerDept])
        else:
            quota = str(COG_QUOTAS[1][index % SuitDNA.suitsPerDept])
        quotaLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DGG.DISABLED, text=TTLocalizer.SuitPageQuota % (count, quota), text_scale=0.045, text_fg=(0, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        panel.quotaLabel = quotaLabel

    def addSuitHead(self, panel, suitName):
        panelIndex = self.panels.index(panel)
        panel.head = Suit.attachSuitHead(panel, suitName)

    def addCogRadarLabel(self, panel):
        cogRadarLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DGG.DISABLED, text='', text_scale=0.05, text_fg=(0, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        panel.cogRadarLabel = cogRadarLabel
        return

    def addSummonButton(self, panel):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        gui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        iconGeom = gui.find('**/summons')
        summonButton = DirectButton(parent=panel, pos=(0.1, 0.0, -0.13), scale=0.1, relief=None, state=DGG.NORMAL, image=okButtonList, image_scale=13.0, geom=iconGeom, geom_scale=0.7, text=('',
         TTLocalizer.IssueSummons,
         TTLocalizer.IssueSummons,
         ''), text_scale=0.4, text_pos=(-1.1, -0.4), command=self.summonButtonPressed, extraArgs=[panel])
        panel.summonButton = summonButton

    def summonButtonPressed(self, panel):
        panelIndex = self.panels.index(panel)
        self.summonDialog = SummonCogDialog.SummonCogDialog(panelIndex)
        self.summonDialog.load()
        self.accept(self.summonDialog.doneEvent, self.summonDone, extraArgs=[panel])
        self.summonDialog.enter()

    def summonDone(self, panel):
        if self.summonDialog:
            self.summonDialog.unload()
            self.summonDialog = None
        index = self.panels.index(panel)

    def addBuildingRadarLabel(self, button):
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        zPos = BUILDING_RADAR_POS[self.radarButtons.index(button)]
        buildingRadarLabel = DirectLabel(parent=button, relief=None, pos=(0.225, 0.0, zPos), state=DGG.DISABLED, image=gui.find('**/avatar_panel'), image_hpr=(0, 0, 90), image_scale=(0.05, 1, 0.1), image_pos=(0, 0, 0.015), text=TTLocalizer.SuitPageBuildingRadarP % '0', text_scale=0.05, text_fg=(1, 0, 0, 1), text_font=ToontownGlobals.getSuitFont())
        gui.removeNode()
        button.buildingRadarLabel = buildingRadarLabel
        return

    def resetPanel(self, dept, type):
        panel = self.panels[dept * SuitDNA.suitsPerDept + type]
        panel['text'] = TTLocalizer.SuitPageMystery
        if panel.cogRadarLabel:
            panel.cogRadarLabel.hide()
        if panel.quotaLabel:
            panel.quotaLabel.hide()
        if panel.head:
            panel.head.hide()
        if panel.summonButton:
            panel.summonButton.hide()
        color = PANEL_COLORS[dept]
        panel['image_color'] = color
        for button in self.radarButtons:
            if button.buildingRadarLabel:
                button.buildingRadarLabel.hide()

    def setPanelStatus(self, panel, status):
        index = self.panels.index(panel)
        if status == COG_UNSEEN:
            panel['text'] = TTLocalizer.SuitPageMystery
        elif status == COG_BATTLED:
            suitName = SuitDNA.suitHeadTypes[index]
            suitFullName = SuitBattleGlobals.SuitAttributes[suitName]['name']
            panel['text'] = suitFullName
            if panel.quotaLabel:
                panel.quotaLabel.show()
            else:
                self.addQuotaLabel(panel)
            if panel.head:
                panel.head.show()
            else:
                self.addSuitHead(panel, suitName)
            if panel.summonButton:
                panel.summonButton.show()
            else:
                self.addSummonButton(panel)
        elif status == COG_DEFEATED:
            count = str(base.localAvatar.cogCounts[index])
            if base.localAvatar.cogs[index] < COG_COMPLETE1:
                quota = str(COG_QUOTAS[0][index % SuitDNA.suitsPerDept])
            else:
                quota = str(COG_QUOTAS[1][index % SuitDNA.suitsPerDept])
            panel.quotaLabel['text'] = TTLocalizer.SuitPageQuota % (count, quota)
        elif status == COG_COMPLETE1:
            panel['image_color'] = PANEL_COLORS_COMPLETE1[index // SuitDNA.suitsPerDept]
        elif status == COG_COMPLETE2:
            panel['image_color'] = PANEL_COLORS_COMPLETE2[index // SuitDNA.suitsPerDept]

    def updateAllCogs(self, status):
        for index in range(0, len(base.localAvatar.cogs)):
            base.localAvatar.cogs[index] = status

        self.updatePage()

    def updatePage(self):
        index = 0
        cogs = base.localAvatar.cogs
        for dept in range(0, len(SuitDNA.suitDepts)):
            for type in range(0, SuitDNA.suitsPerDept):
                self.updateCogStatus(dept, type, cogs[index])
                index += 1

        self.updateCogRadarButtons(base.localAvatar.cogRadar)
        self.updateBuildingRadarButtons(base.localAvatar.buildingRadar)

    def updateCogStatus(self, dept, type, status):
        if dept < 0 or dept > len(SuitDNA.suitDepts):
            print('ucs: bad cog dept: ', dept)
        elif type < 0 or type > SuitDNA.suitsPerDept:
            print('ucs: bad cog type: ', type)
        elif status < COG_UNSEEN or status > COG_COMPLETE2:
            print('ucs: bad status: ', status)
        else:
            self.resetPanel(dept, type)
            panel = self.panels[dept * SuitDNA.suitsPerDept + type]
            if status == COG_UNSEEN:
                self.setPanelStatus(panel, COG_UNSEEN)
            elif status == COG_BATTLED:
                self.setPanelStatus(panel, COG_BATTLED)
            elif status == COG_DEFEATED:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
            elif status == COG_COMPLETE1:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE1)
            elif status == COG_COMPLETE2:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE2)

    def updateCogRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index]['state'] = DGG.NORMAL

    def updateCogRadar(self, deptNum, panels, timeout = 0):
        taskMgr.remove('suitListResponseTimeout-later')
        if not timeout and hasattr(base.cr, 'currSuitPlanner') and base.cr.currSuitPlanner != None:
            cogList = base.cr.currSuitPlanner.suitList
        else:
            cogList = []
        for panel in panels:
            panel.count = 0

        for cog in cogList:
            self.panels[cog].count += 1

        for panel in panels:
            panel.cogRadarLabel['text'] = TTLocalizer.SuitPageCogRadar % panel.count
            if self.radarOn[deptNum]:
                panel.quotaLabel.hide()

                def showLabel(label):
                    label.show()

                taskMgr.doMethodLater(RADAR_DELAY * panels.index(panel), showLabel, 'showCogRadarLater', extraArgs=(panel.cogRadarLabel,))

                def activateButton(s = self, index = deptNum):
                    self.radarButtons[index]['state'] = DGG.NORMAL
                    return Task.done

                if not self.radarButtons[deptNum].building:
                    taskMgr.doMethodLater(RADAR_DELAY * len(panels), activateButton, 'activateButtonLater')
            else:
                panel.cogRadarLabel.hide()
                panel.quotaLabel.show()

        return

    def updateBuildingRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index].building = 1

    def updateBuildingRadar(self, deptNum, timeout = 0):
        taskMgr.remove('buildingListResponseTimeout-later')
        if not timeout and hasattr(base.cr, 'currSuitPlanner') and base.cr.currSuitPlanner != None:
            buildingList = base.cr.currSuitPlanner.buildingList
        else:
            buildingList = [0,
             0,
             0,
             0]
        button = self.radarButtons[deptNum]
        if button.building:
            if not button.buildingRadarLabel:
                self.addBuildingRadarLabel(button)
            if self.radarOn[deptNum]:
                num = buildingList[deptNum]
                if num == 1:
                    button.buildingRadarLabel['text'] = TTLocalizer.SuitPageBuildingRadarS % num
                else:
                    button.buildingRadarLabel['text'] = TTLocalizer.SuitPageBuildingRadarP % num

                def showLabel(button):
                    button.buildingRadarLabel.show()
                    button['state'] = DGG.NORMAL

                taskMgr.doMethodLater(RADAR_DELAY * SuitDNA.suitsPerDept, showLabel, 'showBuildingRadarLater', extraArgs=(button,))
            else:
                button.buildingRadarLabel.hide()
        return
        
    def summonsLabelGrow(self, hotTubs):
        self.summonsLabel.setScale(0.12)
        
    def summonsLabelShrink(self, hotTubs):
        self.summonsLabel.setScale(0.1)

    def __throwSummonsDialog(self):
        if base.localAvatar.pieType == 7:
            message = TTLocalizer.SuitPageRemoveSummons
        else:
            if not base.localAvatar.getSummons():
                return
            message = TTLocalizer.SuitPageThrowSummons
        dialogClass = ToontownGlobals.getDialogClass()
        self.dialog = dialogClass(text=message, dialogName='summonsThrowDialog', command=self.handleThrowSummonsChoice, style=YesNo)
        self.dialog.show()

    def handleThrowSummonsChoice(self, status):
        self.dialog.cleanup()
        self.dialog = None
        if status == 1:
            base.localAvatar.sendUpdate('reqThrowSummons')