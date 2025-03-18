from direct.gui.DirectGui import *
from panda3d.core import *
from otp.otpgui.OTPDialog import YesNo
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer
import random

class TrackPoster(DirectFrame):
    normalTextColor = (0.3, 0.25, 0.2, 1)

    def __init__(self, trackId):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(TrackPoster)
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        trackName = ToontownBattleGlobals.Tracks[trackId].capitalize()
        self.poster = DirectFrame(parent=self, relief=None, image=bookModel.find('**/questCard'), image_scale=(0.8, 0.58, 0.58))
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        iconGeom = invModel.find('**/' + ToontownBattleGlobals.AvPropsNew[trackId][1])
        invModel.removeNode()
        self.pictureFrame = DirectFrame(parent=self.poster, relief=None, image=bookModel.find('**/questPictureFrame'), image_scale=0.25, image_color=(0.45, 0.8, 0.45, 1), text=trackName, text_font=ToontownGlobals.getInterfaceFont(), text_pos=(0, -0.16), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ACenter, text_wordwrap=8.0, textMayChange=0, geom=iconGeom, pos=(-0.2, 0, 0.06))
        bookModel.removeNode()
        if trackId == ToontownBattleGlobals.HEAL_TRACK:
            help = TTLocalizer.TrackChoiceGuiHEAL
        elif trackId == ToontownBattleGlobals.TRAP_TRACK:
            help = TTLocalizer.TrackChoiceGuiTRAP
        elif trackId == ToontownBattleGlobals.LURE_TRACK:
            help = TTLocalizer.TrackChoiceGuiLURE
        elif trackId == ToontownBattleGlobals.SOUND_TRACK:
            help = TTLocalizer.TrackChoiceGuiSOUND
        elif trackId == ToontownBattleGlobals.DROP_TRACK:
            help = TTLocalizer.TrackChoiceGuiDROP
        else:
            help = ''
        self.helpText = DirectFrame(parent=self.poster, relief=None, text=help, text_font=ToontownGlobals.getInterfaceFont(), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ALeft, text_wordwrap=8.0, textMayChange=0, pos=(-0.05, 0, 0.14))
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.chooseButton = DirectButton(parent=self.poster, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiChoose, text_scale=0.06, text_pos=(0, -0.02), command=self.handleChooseButtonPressed, extraArgs=[trackId], pos=(0, 0, -0.13), scale=0.8)
        guiButton.removeNode()

    def handleChooseButtonPressed(self, trackId):
        messenger.send('chooseButtonPressed', [trackId])

class TrackChoiceGui(DirectFrame):

    def __init__(self, tracks, timeout):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=Vec4(0.8, 0.6, 0.4, 1), geom_scale=(1.5, 1, 0.9), geom_hpr=(0, 0, -90), parent=base.a2dTopLeft, pos=(0.483333, 0, -1))
        self.initialiseoptions(TrackChoiceGui)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.cancelButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiCancel, pos=(0.15, 0, -0.535), text_scale=0.06, text_pos=(0, -0.02), command=self.chooseTrack, extraArgs=[-1])
        self.randomButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.1, 1, 1), text=TTLocalizer.TrackChoiceGuiChooseRandom, pos=(0.15, 0, -0.655), text_scale=0.06, text_pos=(0, -0.02), command=self.openConfirmationDialog, extraArgs=[-1])
        guiButton.removeNode()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.35)
        self.timer.setPos(-0.2, 0, -0.6)
        self.timer.countdown(timeout, self.timeout)
        self.trackChoicePosters = []
        for trackId in tracks:
            tp = TrackPoster(trackId)
            tp.reparentTo(self)
            self.trackChoicePosters.append(tp)
            
        self.tracks = tracks

        self.trackChoicePosters[0].setPos(0, 0, -0.2)
        self.trackChoicePosters[1].setPos(0, 0, 0.4)
        self.dialog = None
        self.accept('chooseButtonPressed', self.openConfirmationDialog)
        
    def openConfirmationDialog(self, trackId):
        if trackId == -1:
            message = TTLocalizer.MessageConfirmTrackRandom
            trackId = random.choice(self.tracks)
        else:
            trackName = ToontownBattleGlobals.Tracks[trackId].capitalize()
            message = TTLocalizer.MessageConfirmTrackChoice % trackName
        dialogClass = ToontownGlobals.getDialogClass()
        self.dialog = dialogClass(text=message, dialogName='confirmationDialog', command=self.handleTrackChoice, extraArgs=[trackId], style=YesNo)
        self.dialog.show()

    def handleTrackChoice(self, status, trackId):
        self.dialog.cleanup()
        self.dialog = None
        if status == 1:
            self.ignore('chooseButtonPressed')
            self.chooseTrack(trackId)

    def chooseTrack(self, trackId):
        self.timer.stop()
        messenger.send('chooseTrack', [trackId])

    def timeout(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        messenger.send('chooseTrack', [-1])
