from direct.gui.DirectGui import *
from toontown.battle import BattleBase
from toontown.toontowngui.ToontownLabel import ToontownLabel
from toontown.toontowngui.ToontownButton import ToontownButton
from toontown.toonbase import TTLocalizer, ToontownGlobals
from otp.otpbase import OTPGlobals

class RevivePrompt(DirectFrame):
    
    def __init__(self, cost):
        self.cost = cost
        fadeModel = loader.loadModel('phase_3/models/misc/fade')
        if fadeModel:
            self.fade = DirectFrame(
                parent=aspect2dp,
                relief=None,
                image=fadeModel,
                image_color=(0, 0, 0, 0.4),
                image_scale=3.0,
                state=DGG.NORMAL)
            self.fade.reparentTo(render2d, FADE_SORT_INDEX)
            fadeModel.removeNode()
        else:
            print('Problem loading fadeModel.')
            self.fade = None
        DirectFrame.__init__(self,
            parent=aspect2dp,
            pos=(0, 0, 0),
            relief=None,
            image=DGG.getDefaultDialogGeom(),
            image_scale=(0.9, 1, 1),
            image_color=OTPGlobals.GlobalDialogColor,
            suppressKeys=True)
            
        self.initialiseoptions(RevivePrompt)
        
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        self.title = ToontownLabel(
          parent=self,
          relief=None,
          anim='popinoutfast',
          text=TTLocalizer.RevivePromptTitle,
          text_font=ToontownGlobals.getSignFont(),
          text_scale=0.12,
          text_fg=(1, 0.5, 0, 1),
          pos=(0, 0, 0.38)
        )
        self.desc = ToontownLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.ReviveAsk % (self.cost, base.localAvatar.getTotalMoney()),
            text_wordwrap=13.0,
            text_scale=0.065,
            pos=(0, 0, 0.18)
        )
        self.yesButton = ToontownButton(
          parent=self,
          relief=None,
          image=(gui.find('**/QuitBtn_UP'), gui.find('**/QuitBtn_DN'), gui.find('**/QuitBtn_RLVR')),
          image_scale=(1.3, 1.3, 1.3),
          anim='stretch',
          text=TTLocalizer.lYes,
          text_font=ToontownGlobals.getSignFont(),
          text_fg=(0.95, 0.95, 0.95, 1),
          text_scale=0.12,
          text_pos=(0, -0.03),
          pos=(0, 0, -0.22),
          command=self.handleButtonPress,
          extraArgs=[BattleBase.REVIVE_YES],
        )
        self.noButton = ToontownButton(
          parent=self,
          relief=None,
          image=(gui.find('**/QuitBtn_UP'), gui.find('**/QuitBtn_DN'), gui.find('**/QuitBtn_RLVR')),
          image_scale=(1.3, 1.3, 1.3),
          anim='stretch',
          text=TTLocalizer.lGoSad,
          text_font=ToontownGlobals.getSignFont(),
          text_fg=(0.95, 0.95, 0.95, 1),
          text_scale=0.12,
          text_pos=(0, -0.03),
          pos=(0, 0, -0.37),
          command=self.handleButtonPress,
          extraArgs=[BattleBase.REVIVE_NO],
        )
        gui.removeNode()
        
    def destroy(self):
        if self.fade:
            self.fade.destroy()
        DirectFrame.destroy(self)
        
    def handleButtonPress(self, response):
        if self.fade:
            self.fade.hide()
        self.hide()
        messenger.send('revive-prompt-response', [response])