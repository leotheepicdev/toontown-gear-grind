from direct.gui.DirectGui import *
from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from toontown.chat import ResistanceChat
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.suit import SuitDNA
from toontown.suit import Suit
from toontown.battle import SuitBattleGlobals
from toontown.toon import NPCToons
TTL = TTLocalizer

class SummonCogDialog(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('SummonCogDialog')
    notify.setInfo(True)

    def __init__(self, suitIndex):
        DirectFrame.__init__(self, parent=aspect2dp, pos=(0, 0, 0), relief=None, image=DGG.getDefaultDialogGeom(), image_scale=(1.6, 1, 1), image_pos=(0, 0, 0.18), image_color=ToontownGlobals.GlobalDialogColor, text=TTL.SummonDlgTitle, text_scale=0.12, text_pos=(0, 0.575), borderWidth=(0.01, 0.01), sortOrder=NO_FADE_SORT_INDEX)
        StateData.StateData.__init__(self, 'summon-cog-done')
        self.initialiseoptions(SummonCogDialog)
        self.suitIndex = suitIndex
        base.summonDialog = self
        self.popup = None
        self.suitName = SuitDNA.suitHeadTypes[self.suitIndex]
        self.suitFullName = SuitBattleGlobals.SuitAttributes[self.suitName]['name']

    def unload(self):
        if self.isLoaded == 0:
            return
        self.isLoaded = 0
        self.exit()
        base.summonDialog = None
        DirectFrame.destroy(self)

    def load(self):
        if self.isLoaded == 1:
            return
        self.isLoaded = 1
        gui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.head = Suit.attachSuitHead(self, self.suitName)
        z = self.head.getZ()
        self.head.setPos(-0.4, -0.1, z + 0.2)
        self.suitLabel = DirectLabel(parent=self, relief=None, text=self.suitFullName, text_font=ToontownGlobals.getSuitFont(), pos=(-0.4, 0, 0), scale=0.07)
        closeButtonImage = (gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr'))
        buttonImage = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        disabledColor = Vec4(0.5, 0.5, 0.5, 1)
        self.summonSingleButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton1, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.475), command=self.issueSummons, extraArgs=['single'])
        self.summonBuildingButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton2, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.35), command=self.issueSummons, extraArgs=['building'])
        self.summonOfficeButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton3, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.225), command=self.issueSummons, extraArgs=['office'])
        self.summonInvasionButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton4, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.1), command=self.issueSummons, extraArgs=['invasion'])
        self.summonSkelecogInvasionButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton5, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.05, text_pos=(0, -0.01), pos=(0.3, 0, -0.025), command=self.issueSummons, extraArgs=['skeleinvasion'])
        self.summonDanceButton = DirectButton(parent=self, relief=None, text=TTL.SummonDlgButton6, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, -0.15), command=self.issueSummons, extraArgs=['dance'])        
        self.sueButton = DirectButton(parent=self, relief=None, text=TTL.SueCogButton, image=buttonImage, image_scale=(0.5, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(-0.4, 0, -0.1), command=self.sue)
        self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_wordwrap=12, pos=(0.3, 0, 0.25), scale=0.07)
        self.cancel = DirectButton(parent=self, relief=None, image=closeButtonImage, pos=(0.75, 0, -0.25), command=self.__cancel)
        gui.removeNode()
        guiButton.removeNode()
        self.hide()

    def enter(self):
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        self.disableButtons()
        self.enableButtons()
        self.popup = None
        base.transitions.fadeScreen(0.5)
        self.show()

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        self.cleanupDialogs()
        base.transitions.noTransitions()
        self.ignoreAll()
        self.hide()
        messenger.send(self.doneEvent, [])

    def cleanupDialogs(self):
        self.head = None
        if self.popup != None:
            self.popup.cleanup()
            self.popup = None
        return

    def cogSummonsDone(self, returnCode, suitIndex, buildingId):
        self.cancel['state'] = DGG.NORMAL
        if self.summonsType == 'single':
            if returnCode == 'success':
                self.statusLabel['text'] = TTL.SummonDlgSingleSuccess
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = TTL.SummonDlgSingleBadLoc
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail
        elif self.summonsType == 'building':
            if returnCode == 'success':
                building = base.cr.doId2do.get(buildingId)
                dnaStore = base.cr.playGame.dnaStore
                buildingTitle = dnaStore.getTitleFromBlockNumber(building.block)
                buildingInteriorZone = building.zoneId + 500 + building.block
                npcName = TTLocalizer.SummonDlgShopkeeper
                npcId = NPCToons.zone2NpcDict.get(buildingInteriorZone)
                if npcId:
                    npcName = NPCToons.getNPCName(npcId[0])
                if buildingTitle:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess % (npcName, buildingTitle)
                else:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess2
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = TTL.SummonDlgBldgBadLoc
            elif returnCode == 'capacity':
                self.statusLabel['text'] = TTL.SummonDlgBldgCapacityReached
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail
        elif self.summonsType == 'office':
            if returnCode == 'success':
                building = base.cr.doId2do.get(buildingId)
                dnaStore = base.cr.playGame.dnaStore
                buildingTitle = dnaStore.getTitleFromBlockNumber(building.block)
                buildingInteriorZone = building.zoneId + 500 + building.block
                npcName = TTLocalizer.SummonDlgShopkeeper
                npcId = NPCToons.zone2NpcDict.get(buildingInteriorZone)
                if npcId:
                    npcName = NPCToons.getNPCName(npcId[0])
                if buildingTitle:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess % (npcName, buildingTitle)
                else:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess2
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = TTL.SummonDlgBldgBadLoc
            elif returnCode == 'capacity':
                self.statusLabel['text'] = TTL.SummonDlgBldgCapacityReached
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail
        elif self.summonsType == 'invasion' or self.summonsType == 'skeleinvasion':
            if returnCode == 'success':
                self.statusLabel['text'] = TTL.SummonDlgInvasionSuccess
            elif returnCode == 'busy':
                self.statusLabel['text'] = TTL.SummonDlgInvasionBusy % self.suitFullName
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail
        elif self.summonsType == 'dance':
            if returnCode == 'success':
                self.statusLabel['text'] = TTL.SummonDlgDanceSuccess
            elif returnCode == 'capacity':
                self.statusLabel['text'] = TTL.SummonDlgDanceCapacity
            else:
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail

    def hideSummonButtons(self):
        self.summonSingleButton.hide()
        self.summonBuildingButton.hide()
        self.summonOfficeButton.hide()
        self.summonInvasionButton.hide()
        self.summonSkelecogInvasionButton.hide()
        self.summonDanceButton.hide()
        self.sueButton.hide()

    def issueSummons(self, summonsType):
        if summonsType == 'single':
            text = TTL.SummonDlgSingleConf % (self.suitFullName, ToontownGlobals.COG_SUMMONS_COST)
        elif summonsType == 'building':
            text = TTL.SummonDlgBuildingConf % (self.suitFullName, ToontownGlobals.BUILDING_SUMMONS_COST)
        elif summonsType == 'office':
            text = TTL.SummonDlgBuildingConf % (self.suitFullName, ToontownGlobals.OFFICE_SUMMONS_COST)
        elif summonsType == 'invasion':
            text = TTL.SummonDlgInvasionConf % (self.suitFullName, ToontownGlobals.INVASION_SUMMONS_COST)
        elif summonsType == 'skeleinvasion':
            text = TTL.SummonDlgSkeleInvasionConf % (self.suitFullName, ToontownGlobals.SKELE_INVASION_SUMMONS_COST)
        elif summonsType == 'dance':
            text = TTL.SummonDlgDanceConf % (ToontownGlobals.DANCE_SUMMONS_COST)

        def handleResponse(resp):
            self.popup.cleanup()
            self.popup = None
            self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
            base.transitions.fadeScreen(0.5)
            if resp == DGG.DIALOG_OK:
                self.notify.info('issuing %s summons for %s' % (summonsType, self.suitIndex))
                self.accept('cog-summons-response', self.cogSummonsDone)
                self.summonsType = summonsType
                self.doIssueSummonsText()
                base.localAvatar.d_reqCogSummons(self.summonsType, self.suitIndex)
                self.hideSummonButtons()
                self.cancel['state'] = DGG.DISABLED
            else:
                self.enableButtons()

        self.reparentTo(self.getParent(), 0)
        self.disableButtons()
        self.popup = TTDialog.TTDialog(parent=aspect2dp, style=TTDialog.YesNo, text=text, fadeScreen=1, command=handleResponse)

    def doIssueSummonsText(self):
        self.statusLabel['text'] = TTL.SummonDlgDelivering
        
    def sue(self):
        messenger.send('wakeup')
        self.disableButtons()
        text = TTL.SueCogConf % (self.suitFullName, ToontownGlobals.SUE_COST)
        def handleResponse(resp):
            self.popup.cleanup()
            self.popup = None
            self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
            base.transitions.fadeScreen(0.5)
            if resp == DGG.DIALOG_OK:
                self.accept('sue-cog-response', self.sueCogDone)
                self.doSueingCogText()
                base.localAvatar.d_reqSueCog()
                self.hideSummonButtons()
                self.cancel['state'] = DGG.DISABLED
            else:
                self.enableButtons()
            return
        self.reparentTo(self.getParent(), 0)
        self.popup = TTDialog.TTDialog(parent=aspect2dp, style=TTDialog.YesNo, text=text, fadeScreen=1, command=handleResponse)
        
    def doSueingCogText(self):
        self.statusLabel['text'] = TTL.SueCogSueing
        
    def sueCogDone(self, reward, amount, type):
        if reward == ToontownGlobals.SUE_REWARD_JELLYBEANS:
            self.statusLabel['text'] = TTLocalizer.SueCogRewardJellybeans % amount
        elif reward == ToontownGlobals.SUE_REWARD_CLOTHING_TICKET:
            if amount > 1:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardClothingTicketP % amount
            else:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardClothingTicketS
        elif reward == ToontownGlobals.SUE_REWARD_GLOVE_TICKET:
            if amount > 1:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardClothingTicketP % amount
            else:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardClothingTicketS
        elif reward == ToontownGlobals.SUE_REWARD_PINK_SLIP:
            if amount > 1:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardPinkSlipP % amount
            else:
                self.statusLabel['text'] = TTLocalizer.SueCogRewardPinkSlipS
        elif reward == ToontownGlobals.SUE_REWARD_UNITE:
            self.statusLabel['text'] = TTLocalizer.SueCogRewardUniteS % ResistanceChat.getItemText(type)
        elif reward == ToontownGlobals.SUE_REWARD_SOS:
            self.statusLabel['text'] = TTLocalizer.SueCogRewardSosS % TTLocalizer.NPCToonNames[type]
        self['text'] = TTLocalizer.SueLawsuitWon
        self.cancel['state'] = DGG.NORMAL

    def disableButtons(self):
        self.summonSingleButton['state'] = DGG.DISABLED
        self.summonBuildingButton['state'] = DGG.DISABLED
        self.summonOfficeButton['state'] = DGG.DISABLED
        self.summonInvasionButton['state'] = DGG.DISABLED
        self.summonSkelecogInvasionButton['state'] = DGG.DISABLED
        self.summonDanceButton['state'] = DGG.DISABLED
        self.sueButton['state'] = DGG.DISABLED

    def enableButtons(self):
        if base.localAvatar.getSummons() >= ToontownGlobals.COG_SUMMONS_COST:
            self.summonSingleButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.BUILDING_SUMMONS_COST:
            self.summonBuildingButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.OFFICE_SUMMONS_COST:
            self.summonOfficeButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.INVASION_SUMMONS_COST:
            self.summonInvasionButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.SKELE_INVASION_SUMMONS_COST:
            self.summonSkelecogInvasionButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.DANCE_SUMMONS_COST:
            self.summonDanceButton['state'] = DGG.NORMAL
        if base.localAvatar.getSummons() >= ToontownGlobals.SUE_COST:
            self.sueButton['state'] = DGG.NORMAL

    def __cancel(self):
        self.exit()
