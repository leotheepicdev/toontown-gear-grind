from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from toontown.toontowngui.ToontownButton import ToontownButton
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from otp.otpbase import OTPLocalizer
from otp.otpgui import OTPDialog
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
from toontown.toonbase import TTLocalizer, ToontownGlobals
import builtins, webbrowser

class ToontownLoginScreen(DirectObject):
    LOGIN_DONE_EVENT = 'loginDone'

    def __init__(self):
        DirectObject.__init__(self)
        self.fsm = ClassicFSM.ClassicFSM('ToontownLoginScreen', [
         State.State('off', self.enterOff, self.exitOff, ['intro', 'login']),
         State.State('intro', self.enterIntro, self.exitIntro, ['login']),
         State.State('login', self.enterLogin, self.exitLogin, [])], 'off', 'off')
        self.fsm.enterInitialState()
        self.booted = False
        self.introBackground = None
        self.introLogo = None
        self.loginBackground = None
        self.loginLogo = None
        self.loginLogoScaleTrack = None
        self.quitButton = None
        self.disconnectDialog = None
        self.loginDialog = None
        self.isLoaded = False

    def __handleQuit(self):
        base.exitFunc()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterIntro(self):
        self.introBackground = OnscreenImage(parent=render2d, image='phase_3/maps/intro-background.png')
        self.introBackground.setBin('fixed', 40)
        self.introLogo = OnscreenImage(parent=base.aspect2d, image='phase_3/maps/toontown-logo.png', scale=(1, 1, 0.000001), color=(1, 1, 1, 1))
        self.introLogo.setTransparency(1)
        self.introLogo.setBin('fixed', 50)

        self.introLogoFadeIn = Sequence(Parallel(Func(self.introLogo.setScale, (1, 1, 0.6)),
                                        LerpColorScaleInterval(self.introLogo, 2, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeIn')), Func(self.fsm.request, 'login'))
        self.introLogoFadeIn.start()

    def exitIntro(self):
        launcher.setPandaErrorCode(0)
        launcher.setPandaWindowOpen()
        ConfigVariableDouble('decompressor-step-time').setValue(0.01)
        ConfigVariableDouble('extractor-step-time').setValue(0.01)
        base.graphicsEngine.renderFrame()
        DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
        DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
        DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
        ToontownGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
        DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
        DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
        base.cr = ToontownClientRepository.ToontownClientRepository(base.config.GetString('server-version', 'no_version_set'), launcher)
        base.cr.loginScreen = self
        base.initNametagGlobals()
        base.setFrameRateMeter(builtins.Settings['frameRateMeter'])
        base.cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
        builtins.loader = base.loader
        self.introBackground.destroy()
        self.introLogo.destroy()

    def handleLostConnection(self):
        if self.booted:
            base.cr.cleanupWaitingForDatabase()
            if base.cr.bootedIndex != None and base.cr.bootedIndex in OTPLocalizer.CRBootedReasons:
                message = OTPLocalizer.CRBootedReasons[base.cr.bootedIndex] % {'name': base.cr.playToken, 'reason': base.cr.bootedText}
            elif base.cr.bootedIndex != None and base.cr.bootedIndex in OTPLocalizer.LoginErrors:
                message = OTPLocalizer.LoginErrors[base.cr.bootedIndex] % {'name': base.cr.playToken, 'reason': base.cr.bootedText}
            elif base.cr.bootedText != None:
                message = OTPLocalizer.CRBootedReasonUnknownCode % base.cr.bootedIndex
            else:
                message = OTPLocalizer.CRLostConnection
            base.cr.launcher.setDisconnectDetails(base.cr.bootedIndex, message)
            style = OTPDialog.Acknowledge
            dialogClass = OTPGlobals.getGlobalDialogClass()
            self.lostConnectionBox = dialogClass(doneEvent='lostConnectionAck', message=message, text_wordwrap=18, style=style)
            self.lostConnectionBox.show()
            self.accept('lostConnectionAck', self.handleLostConnectionAck)
            self.booted = False

    def handleLostConnectionAck(self):
        self.ignore('lostConnectionAck')
        self.lostConnectionBox.cleanup()
        del self.lostConnectionBox

    def enterLogin(self):
        if not self.loginBackground:
            self.createLoginBackground()
        if not self.loginLogo:
            self.createLoginLogo()
        self.usernameLabel = DirectLabel(parent=aspect2d, relief=None, scale=0.06, pos=(-0.4, 0, -0.2), text='Username', text_font=ToontownGlobals.getSignFont(), text_fg=Vec4(0.95, 0.95, 0.95, 1))
        self.passwordLabel = DirectLabel(parent=aspect2d, relief=None, scale=0.06, pos=(-0.4, 0, -0.4), text='Password', text_font=ToontownGlobals.getSignFont(), text_fg=Vec4(0.95, 0.95, 0.95, 1))
        self.usernameInput = DirectEntry(parent=aspect2d, overflow=1, focus=1, cursorKeys=1, scale=0.08, pos=(-0.15, 0, -0.2), width=10.5)
        self.passwordInput = DirectEntry(parent=aspect2d, overflow=1, focus=0, cursorKeys=1, obscured=1, scale=0.08, pos=(-0.15, 0, -0.4), width=10.5)
        if not base.cr.music:
            base.cr.music = loader.loadMusic('phase_3/audio/bgm/tt_theme.ogg')
            if base.cr.music:
                base.cr.music.setLoop(1)
                base.cr.music.play()
        self.acceptTab()
        base.updateDistrict('Login Screen')
        self.isLoaded = True
        
        base.cr.renderFrame()
        base.cr.renderFrame()
        seq = Sequence(
          Wait(0.1),
          Parallel(
              Func(self.loadButtons),
              Func(self.createQuitButton),
          )
        )
        seq.start()
        
    def loadButtons(self):
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.loginButton = ToontownButton(parent=aspect2d, relief=None, pos=(0, 0, -0.6), scale=0.92, enteranim='fadeinscale', anim='stretch',
                           image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP')), text=TTLocalizer.LoginScreenLogin,
                           text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.7, 1.1, 1.1), image1_scale=(1.8, 1.2, 1.2), image2_scale=(1.8, 1.2, 1.2), command=self.handleLogin)
        self.createAccountButton = ToontownButton(parent=aspect2d, relief=None, pos=(0, 0, -0.72), scale=0.92, enteranim='fadeinscale', anim='stretch',
                           image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP')), text=TTLocalizer.LoginScreenCreateAccount,
                           text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.7, 1.1, 1.1), image1_scale=(1.8, 1.2, 1.2), image2_scale=(1.8, 1.2, 1.2), command=self.handleCreateAccount)
        self.forgotPasswordButton = ToontownButton(parent=aspect2d, relief=None, pos=(0, 0, -0.84), scale=0.92, enteranim='fadeinscale', anim='stretch',
                           image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_UP')), text=TTLocalizer.LoginScreenForgotPassword,
                           text_scale=0.06, text_pos=(0, -0.02), image_scale=(1.7, 1.1, 1.1), image1_scale=(1.8, 1.2, 1.2), image2_scale=(1.8, 1.2, 1.2), command=self.handleForgotPassword)
        guiButton.removeNode()
        
    def acceptTab(self):
        self.accept('tab', self.switchEntries)

    def switchEntries(self):
        if self.usernameInput['focus']:
            self.usernameInput['focus'] = 0
            self.passwordInput['focus'] = 1
        elif self.passwordInput['focus']:
            self.passwordInput['focus'] = 0
            self.usernameInput['focus'] = 1
        else:
            self.usernameInput['focus'] = 1

    def handleBooted(self, showBooted=True):
        self.booted = showBooted
        if not self.isLoaded:
            self.handleLostConnection()
            self.fsm.request('login')
        else:
            self.loginButton['state'] = DGG.NORMAL
            self.createAccountButton['state'] = DGG.NORMAL
            self.forgotPasswordButton['state'] = DGG.NORMAL
            self.quitButton['state'] = DGG.NORMAL
            self.handleLostConnection()


    def exitLogin(self):
        if self.loginLogoScaleTrack:
            self.loginLogoScaleTrack.finish()
            self.loginLogoScaleTrack = None
        for x in (self.loginBackground, self.loginLogo, self.quitButton, self.usernameLabel, self.passwordLabel, self.usernameInput, self.passwordInput, self.loginButton, self.createAccountButton, self.forgotPasswordButton):
            x.destroy()
            x = None
        self.isLoaded = False

    def createLoginBackground(self):
        self.loginBackground = OnscreenImage(parent=render2d, pos=(0, 0, 0), scale=(render2d, VBase3(1)), image='phase_3/maps/loading_bg_town.jpg')
        self.loginBackground.setBin('fixed', 10)

    def createLoginLogo(self):
        self.loginLogo = OnscreenImage(parent=base.a2dTopCenter, image='phase_3/maps/toontown-logo.png', scale=(1, 1, 0.5), pos=(0, 0, -0.53))
        self.loginLogo.setTransparency(1)
        self.loginLogo.setBin('fixed', 20)
        self.loginLogoScaleTrack = Sequence(LerpScaleInterval(self.loginLogo, 3, (0.85, 1, 0.45), Vec3(1, 1, 0.5), blendType='easeInOut'),
                                            LerpScaleInterval(self.loginLogo, 3, (1, 1, 0.5), Vec3(0.85, 1, 0.45), blendType='easeInOut'))
        self.loginLogoScaleTrack.loop()

    def createQuitButton(self):
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        self.quitButton = ToontownButton(parent=base.a2dBottomRight, image=(gui.find('**/QuitBtn_UP'), gui.find('**/QuitBtn_DN'), gui.find('**/QuitBtn_RLVR')), relief=None, enteranim='fadeinscale', anim='stretch', text=TTLocalizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text0_fg=(0.152, 0.75, 0.258, 1), text1_fg=(0.152, 0.75, 0.258, 1), text2_fg=(0.977, 0.816, 0.133, 1), text3_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(-0.25, 0, 0.075), command=self.__handleQuit)
        gui.removeNode()

    def handleLogin(self):
        self.ignore('tab')
        base.cr.playToken = self.usernameInput.get()
        base.cr.password = self.passwordInput.get()
        if base.cr.playToken.isspace() or base.cr.playToken == '' or len(base.cr.playToken.split()) != 1:
            message = TTLocalizer.LoginScreenUsernameSpace
            style = OTPDialog.Acknowledge
            dialogClass = OTPGlobals.getGlobalDialogClass()
            self.loginBox = dialogClass(doneEvent='loginErrorAck', message=message, text_wordwrap=18, style=style)
            self.loginBox.show()
            self.accept('loginErrorAck', self.handleLoginErrorAck)
            return
        elif len(base.cr.playToken) > 40:
            message = TTLocalizer.LoginScreenUsernameLength
            style = OTPDialog.Acknowledge
            dialogClass = OTPGlobals.getGlobalDialogClass()
            self.loginBox = dialogClass(doneEvent='loginErrorAck', message=message, text_wordwrap=18, style=style)
            self.loginBox.show()
            self.accept('loginErrorAck', self.handleLoginErrorAck)
            return
        if __debug__:
            pass
        else:
            if base.cr.password.isspace() or base.cr.password == '' or len(base.cr.password.split()) != 1:
                message = TTLocalizer.LoginScreenPasswordSpace
                style = OTPDialog.Acknowledge
                dialogClass = OTPGlobals.getGlobalDialogClass()
                self.loginBox = dialogClass(doneEvent='loginErrorAck', message=message, text_wordwrap=18, style=style)
                self.loginBox.show()
                self.accept('loginErrorAck', self.handleLoginErrorAck)
                return
            elif len(base.cr.password) > 40:
                message = TTLocalizer.LoginScreenPasswordLength
                style = OTPDialog.Acknowledge
                dialogClass = OTPGlobals.getGlobalDialogClass()
                self.loginBox = dialogClass(doneEvent='loginErrorAck', message=message, text_wordwrap=18, style=style)
                self.loginBox.show()
                self.accept('loginErrorAck', self.handleLoginErrorAck)
                return
        base.startShow(base.cr)

    def handleLoginErrorAck(self):
        if self.loginBox:
            self.loginBox.cleanup()
            self.loginBox = None
            self.ignore('loginErrorAck')
        self.acceptTab()

    def handleConnectDone(self):
        self.acceptOnce(self.LOGIN_DONE_EVENT, self.handleLoginDone)

        if __debug__:
            base.cr.clientManager.performLogin(self.LOGIN_DONE_EVENT, False)
        else:
            base.cr.clientManager.performLogin(self.LOGIN_DONE_EVENT, True)

        base.cr.waitForDatabaseTimeout(requestName='ClientManager-LoginResponse')
        
    def handleFailedToConnect(self):
        self.acceptTab()

    def handleLoginDone(self, doneStatus):
        self.loginButton['state'] = DGG.DISABLED
        self.createAccountButton['state'] = DGG.DISABLED
        self.forgotPasswordButton['state'] = DGG.DISABLED
        self.quitButton['state'] = DGG.DISABLED
        base.cr.cleanupWaitingForDatabase()

    def handleCreateAccount(self):
        webbrowser.open('https://geargrind.tech/register')

    def handleForgotPassword(self):
        webbrowser.open('https://geargrind.tech/password/reset')
