from pandac.PandaModules import *
from . import ShtikerPage
from toontown.toontowngui import TTDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from . import DisplaySettingsDialog
from direct.task import Task
from otp.speedchat import SpeedChat
from otp.speedchat import ChatColorScheme, SCColorScheme
from otp.speedchat import ChatStaticTextTerminal, SCStaticTextTerminal
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
speedChatStyles = ((2000,
  (200 / 255.0, 60 / 255.0, 229 / 255.0),
  (200 / 255.0, 135 / 255.0, 255 / 255.0),
  (220 / 255.0, 195 / 255.0, 229 / 255.0)),
 (2001,
  (0 / 255.0, 0 / 255.0, 255 / 255.0),
  (140 / 255.0, 150 / 255.0, 235 / 255.0),
  (201 / 255.0, 215 / 255.0, 255 / 255.0)),
 (2002,
  (90 / 255.0, 175 / 255.0, 225 / 255.0),
  (120 / 255.0, 215 / 255.0, 255 / 255.0),
  (208 / 255.0, 230 / 255.0, 250 / 255.0)),
 (2003,
  (130 / 255.0, 235 / 255.0, 235 / 255.0),
  (120 / 255.0, 225 / 255.0, 225 / 255.0),
  (234 / 255.0, 255 / 255.0, 255 / 255.0)),
 (2004,
  (0 / 255.0, 200 / 255.0, 70 / 255.0),
  (0 / 255.0, 200 / 255.0, 80 / 255.0),
  (204 / 255.0, 255 / 255.0, 204 / 255.0)),
 (2005,
  (235 / 255.0, 230 / 255.0, 0 / 255.0),
  (255 / 255.0, 250 / 255.0, 100 / 255.0),
  (255 / 255.0, 250 / 255.0, 204 / 255.0)),
 (2006,
  (255 / 255.0, 153 / 255.0, 0 / 255.0),
  (229 / 255.0, 147 / 255.0, 0 / 255.0),
  (255 / 255.0, 234 / 255.0, 204 / 255.0)),
 (2007,
  (255 / 255.0, 0 / 255.0, 50 / 255.0),
  (229 / 255.0, 0 / 255.0, 50 / 255.0),
  (255 / 255.0, 204 / 255.0, 204 / 255.0)),
 (2008,
  (255 / 255.0, 153 / 255.0, 193 / 255.0),
  (240 / 255.0, 157 / 255.0, 192 / 255.0),
  (255 / 255.0, 215 / 255.0, 238 / 255.0)),
 (2009,
  (170 / 255.0, 120 / 255.0, 20 / 255.0),
  (165 / 255.0, 120 / 255.0, 50 / 255.0),
  (210 / 255.0, 200 / 255.0, 180 / 255.0)),
 (2010,
  (0.4, 0.4, 0.4),
  (0.3, 0.3, 0.3),
  (0.5, 0.5, 0.5)))
chatStyles = (
 (11000, (1, 1, 1, 1)),
 (11001, (0.86274509803, 0.76470588235, 0.89803921568, 1)),
 (11002, (0.78823529411, 0.8431372549, 1, 1)),
 (11003, (0.81568627451, 0.90196078431, 0.98039215686, 1)),
 (11004, (0.91764705882, 1, 1, 1)),
 (11005, (0.8, 1, 0.8, 1)),
 (11006, (1, 0.98039215686, 0.8, 1)),
 (11007, (1, 0.91764705882, 0.8, 1)),
 (11008, (1, 0.8, 0.8, 1)),
 (11009, (1, 0.8431372549, 0.93333333333, 1)),
 (11010, (0.82352941176, 0.78431372549, 0.70588235294, 1)),
 (11011, (0.5, 0.5, 0.5, 1)))

PageMode = PythonUtil.Enum('Options, Codes')

class OptionsPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.optionsTabPage = OptionsTabPage(self)
        self.optionsTabPage.hide()
        self.codesTabPage = CodesTabPage(self)
        self.codesTabPage.hide()
        titleHeight = 0.61
        self.title = DirectLabel(parent=self, relief=None, text='', text_scale=0.12, pos=(0, 0, titleHeight))
        normalColor = (1, 1, 1, 1)
        clickColor = (0.8, 0.8, 0, 1)
        rolloverColor = (0.15, 0.82, 1.0, 1)
        diabledColor = (1.0, 0.98, 0.15, 1)
        gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        self.optionsTab = DirectButton(parent=self, relief=None, text=TTLocalizer.OptionsPageTitle, text_scale=TTLocalizer.OPoptionsTab, text_align=TextNode.ALeft, text_pos=(0.01, 0.0, 0.0), image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Options], pos=(-0.36, 0, 0.77))
        self.codesTab = DirectButton(parent=self, relief=None, text=TTLocalizer.OptionsPageCodesTab, text_scale=TTLocalizer.OPoptionsTab, text_align=TextNode.ALeft, text_pos=(-0.035, 0.0, 0.0), image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode.Codes], pos=(0.11, 0, 0.77))
        return

    def enter(self):
        self.setMode(PageMode.Options, updateAnyways=1)
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.optionsTabPage.exit()
        self.codesTabPage.exit()
        ShtikerPage.ShtikerPage.exit(self)

    def unload(self):
        self.optionsTabPage.unload()
        del self.title
        ShtikerPage.ShtikerPage.unload(self)

    def setMode(self, mode, updateAnyways = 0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return
            else:
                self.mode = mode
        if mode == PageMode.Options:
            self.mode = PageMode.Options
            self.title['text'] = ''
            self.optionsTab['state'] = DGG.DISABLED
            self.optionsTabPage.enter()
            self.codesTab['state'] = DGG.NORMAL
            self.codesTabPage.exit()
        elif mode == PageMode.Codes:
            self.mode = PageMode.Codes
            self.title['text'] = TTLocalizer.CdrPageTitle
            self.optionsTab['state'] = DGG.NORMAL
            self.optionsTabPage.exit()
            self.codesTab['state'] = DGG.DISABLED
            self.codesTabPage.enter()
        else:
            raise Exception('OptionsPage::setMode - Invalid Mode %s' % mode)


class OptionsTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsTabPage')
    DisplaySettingsTaskName = 'save-display-settings'
    DisplaySettingsDelay = 60
    ChangeDisplaySettings = base.config.GetBool('change-display-settings', 1)
    ChangeDisplayAPI = base.config.GetBool('change-display-api', 0)
    DisplaySettingsApiMap = {'OpenGL': Settings.GL,
     'DirectX7': Settings.DX7,
     'DirectX8': Settings.DX8}

    def __init__(self, parent = aspect2d):
        self.parent = parent
        self.currentSizeIndex = None
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        self.displaySettings = None
        self.displaySettingsChanged = 0
        self.displaySettingsSize = (None, None)
        self.displaySettingsFullscreen = None
        self.displaySettingsEmbedded = None
        self.displaySettingsApi = None
        self.displaySettingsApiChanged = 0
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        titleHeight = 0.61
        textStartHeight = 0.6
        textRowHeight = 0.145
        leftMargin = -0.72
        buttonbase_xcoord = 0.35
        buttonbase_ycoord = 0.6
        button_image_scale = (0.7, 1, 1)
        button_textpos = (0, -0.02)
        options_text_scale = 0.052
        disabled_arrow_color = Vec4(0.6, 0.6, 0.6, 1.0)
        self.speed_chat_scale = 0.055
        self.Music_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, pos=(leftMargin, 0, textStartHeight))
        self.SoundFX_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - textRowHeight))
        self.Friends_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - 3 * textRowHeight))
        self.Whispers_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - 4 * textRowHeight))
        self.DisplaySettings_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=10, pos=(leftMargin, 0, textStartHeight - 5 * textRowHeight))
        self.SpeedChatStyle_Label = DirectLabel(parent=self, relief=None, text=TTLocalizer.OptionsPageSpeedChatStyleLabel, text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=10, pos=(leftMargin, 0, textStartHeight - 6 * textRowHeight))
        self.ChatStyle_Label = DirectLabel(parent=self, relief=None, text=TTLocalizer.OptionsPageChatStyleLabel, text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=10, pos=(leftMargin, 0, textStartHeight - 7 * textRowHeight))
        self.ToonChatSounds_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=15, pos=(leftMargin, 0, textStartHeight - 2 * textRowHeight + 0.025))
        self.ToonChatSounds_Label.setScale(0.9)
        self.Music_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord), command=self.__doToggleMusic)
        self.SoundFX_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight), command=self.__doToggleSfx)
        self.Friends_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 3), command=self.__doToggleAcceptFriends)
        self.Whispers_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 4), command=self.__doToggleAcceptWhispers)
        self.DisplaySettingsButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=button_image_scale, text=TTLocalizer.OptionsPageChange, text3_fg=(0.5, 0.5, 0.5, 0.75), text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 5), command=self.__doDisplaySettings)
        self.speedChatStyleLeftArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), scale=(-1.0, 1.0, 1.0), pos=(0.25, 0, buttonbase_ycoord - textRowHeight * 6), command=self.__doSpeedChatStyleLeft)
        self.speedChatStyleRightArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), pos=(0.65, 0, buttonbase_ycoord - textRowHeight * 6), command=self.__doSpeedChatStyleRight)
        self.chatStyleLeftArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), scale=(-1.0, 1.0, 1.0), pos=(0.25, 0, buttonbase_ycoord - textRowHeight * 7), command=self.__doChatStyleLeft)
        self.chatStyleRightArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), pos=(0.65, 0, buttonbase_ycoord - textRowHeight * 7), command=self.__doChatStyleRight)
        self.ToonChatSounds_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'),
         guiButton.find('**/QuitBtn_DN'),
         guiButton.find('**/QuitBtn_RLVR'),
         guiButton.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=button_image_scale, text='', text3_fg=(0.5, 0.5, 0.5, 0.75), text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 2 + 0.025), command=self.__doToggleToonChatSounds)
        self.ToonChatSounds_toggleButton.setScale(0.8)
        self.speedChatStyleText = SpeedChat.SpeedChat(name='OptionsPageStyleText', structure=[2000], backgroundModelName='phase_3/models/gui/ChatPanel', guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChatStyleText.setScale(self.speed_chat_scale)
        self.speedChatStyleText.setPos(0.37, 0, buttonbase_ycoord - textRowHeight * 6 + 0.03)
        self.speedChatStyleText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)
        self.chatStyleText = SpeedChat.SpeedChat(name='OptionsPageChatStyleText', structure=[2000], backgroundModelName='phase_3/models/gui/ChatPanel', guiModelName='phase_3.5/models/gui/speedChatGui')
        self.chatStyleText.setScale(self.speed_chat_scale)
        self.chatStyleText.setPos(0.37, 0, buttonbase_ycoord - textRowHeight * 7 + 0.03)
        self.chatStyleText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)
        self.whitelistButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=1.15, text='', text_scale=options_text_scale, text_pos=button_textpos, textMayChange=0, pos=(0.45, 0, -0.6), command=self.__toggleWhitelist)
        self.daylightButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=1.15, text='', text_scale=options_text_scale, text_pos=button_textpos, textMayChange=0, pos=(-0.45, 0, -0.6), command=self.__toggleDaylight)
        guiButton.removeNode()
        gui.removeNode()
        return

    def enter(self):
        self.show()
        taskMgr.remove(self.DisplaySettingsTaskName)
        self.settingsChanged = 0
        self.__setWhitelistButton()
        self.__setDaylightButton()
        self.__setMusicButton()
        self.__setSoundFXButton()
        self.__setAcceptFriendsButton()
        self.__setAcceptWhispersButton()
        self.__setDisplaySettings()
        self.__setToonChatSoundsButton()
        self.speedChatStyleText.enter()
        self.speedChatStyleIndex = base.localAvatar.getSpeedChatStyleIndex()
        self.chatStyleText.enter()
        self.chatStyleIndex = base.localAvatar.getChatStyleIndex()
        self.updateSpeedChatStyle()
        self.updateChatStyle()

    def exit(self):
        self.ignore('confirmDone')
        self.hide()
        if self.settingsChanged != 0:
            Settings.writeSettings()
        self.speedChatStyleText.exit()
        self.chatStyleText.exit()
        if self.displaySettingsChanged:
            taskMgr.doMethodLater(self.DisplaySettingsDelay, self.writeDisplaySettings, self.DisplaySettingsTaskName)

    def unload(self):
        self.writeDisplaySettings()
        taskMgr.remove(self.DisplaySettingsTaskName)
        if self.displaySettings != None:
            self.ignore(self.displaySettings.doneEvent)
            self.displaySettings.unload()
        self.displaySettings = None
        self.whitelistButton.destroy()
        self.Music_toggleButton.destroy()
        self.SoundFX_toggleButton.destroy()
        self.Friends_toggleButton.destroy()
        self.Whispers_toggleButton.destroy()
        self.DisplaySettingsButton.destroy()
        self.speedChatStyleLeftArrow.destroy()
        self.speedChatStyleRightArrow.destroy()
        self.chatStyleLeftArrow.destroy()
        self.chatStyleRightArrow.destroy()
        del self.whitelistButton
        del self.SoundFX_Label
        del self.Music_Label
        del self.Friends_Label
        del self.Whispers_Label
        del self.SpeedChatStyle_Label
        del self.ChatStyle_Label
        del self.SoundFX_toggleButton
        del self.Music_toggleButton
        del self.Friends_toggleButton
        del self.Whispers_toggleButton
        del self.speedChatStyleLeftArrow
        del self.speedChatStyleRightArrow
        self.speedChatStyleText.exit()
        self.speedChatStyleText.destroy()
        del self.speedChatStyleText
        del self.chatStyleLeftArrow
        del self.chatStyleRightArrow
        self.chatStyleText.exit()
        self.chatStyleText.destroy()
        del self.chatStyleText
        self.currentSizeIndex = None
        
    def __toggleWhitelist(self):
        messenger.send('wakeup')
        if Settings['wantWhitelist']:
            Settings['wantWhitelist'] = False
        else:
            Settings['wantWhitelist'] = True
        self.settingsChanged = 1
        self.__setWhitelistButton()
        
    def __setWhitelistButton(self):
        if Settings['wantWhitelist']:
            self.whitelistButton['text'] = TTLocalizer.OptionsPageWhitelistOnLabel
        else:
            self.whitelistButton['text'] = TTLocalizer.OptionsPageWhitelistOffLabel
            
    def __toggleDaylight(self):
        messenger.send('wakeup')
        if Settings['wantDaylight']:
            Settings['wantDaylight'] = False
        else:
            Settings['wantDaylight'] = True
        self.settingsChanged = 1
        self.__setDaylightButton()
        messenger.send('daylightSettingsChange')
        
    def __setDaylightButton(self):
        if Settings['wantDaylight']:
            self.daylightButton['text'] = TTLocalizer.OptionsPageDaylightOnLabel
        else:
            self.daylightButton['text'] = TTLocalizer.OptionsPageDaylightOffLabel

    def __doToggleMusic(self):
        messenger.send('wakeup')
        if base.musicActive:
            base.enableMusic(0)
            Settings['music'] = 0
        else:
            base.enableMusic(1)
            Settings['music'] = 1
        self.settingsChanged = 1
        self.__setMusicButton()

    def __setMusicButton(self):
        if base.musicActive:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOnLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOffLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __doToggleSfx(self):
        messenger.send('wakeup')
        if base.sfxActive:
            base.enableSoundEffects(0)
            Settings['sfx'] = 0
        else:
            base.enableSoundEffects(1)
            Settings['sfx'] = 1
        self.settingsChanged = 1
        self.__setSoundFXButton()

    def __doToggleToonChatSounds(self):
        messenger.send('wakeup')
        if base.toonChatSounds:
            base.toonChatSounds = 0
            Settings['toonChatSounds'] = 0
        else:
            base.toonChatSounds = 1
            Settings['toonChatSounds'] = 1
        self.settingsChanged = 1
        self.__setToonChatSoundsButton()

    def __setSoundFXButton(self):
        if base.sfxActive:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOnLabel
            self.SoundFX_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOffLabel
            self.SoundFX_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        self.__setToonChatSoundsButton()

    def __setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

    def __doToggleAcceptFriends(self):
        messenger.send('wakeup')
        if base.localAvatar.acceptingNewFriends:
            base.localAvatar.acceptingNewFriends = 0
            Settings['acceptingNewFriends'] = 0
        else:
            base.localAvatar.acceptingNewFriends = 1
            Settings['acceptingNewFriends'] = 1
        self.settingsChanged = 1
        self.__setAcceptFriendsButton()

    def __doToggleAcceptWhispers(self):
        messenger.send('wakeup')
        if base.localAvatar.acceptingNonFriendWhispers:
            base.localAvatar.acceptingNonFriendWhispers = 0
            Settings['acceptingNonFriendWhispers'] = 0
        else:
            base.localAvatar.acceptingNonFriendWhispers = 1
            Settings['acceptingNonFriendWhispers'] = 1
        self.settingsChanged = 1
        self.__setAcceptWhispersButton()

    def __setAcceptFriendsButton(self):
        if base.localAvatar.acceptingNewFriends:
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsEnabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsDisabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __setAcceptWhispersButton(self):
        if base.localAvatar.acceptingNonFriendWhispers:
            self.Whispers_Label['text'] = TTLocalizer.OptionsPageWhisperEnabledLabel
            self.Whispers_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Whispers_Label['text'] = TTLocalizer.OptionsPageWhisperDisabledLabel
            self.Whispers_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __doDisplaySettings(self):
        if self.displaySettings == None:
            self.displaySettings = DisplaySettingsDialog.DisplaySettingsDialog()
            self.displaySettings.load()
            self.accept(self.displaySettings.doneEvent, self.__doneDisplaySettings)
        self.displaySettings.enter(self.ChangeDisplaySettings, self.ChangeDisplayAPI)
        return

    def __doneDisplaySettings(self, anyChanged, apiChanged):
        if anyChanged:
            self.__setDisplaySettings()
            properties = base.win.getProperties()
            self.displaySettingsChanged = 1
            self.displaySettingsSize = (properties.getXSize(), properties.getYSize())
            self.displaySettingsFullscreen = properties.getFullscreen()
            self.displaySettingsEmbedded = self.isPropertiesEmbedded(properties)
            self.displaySettingsApi = base.pipe.getInterfaceName()
            self.displaySettingsApiChanged = apiChanged

    def isPropertiesEmbedded(self, properties):
        result = False
        if properties.getParentWindow():
            result = True
        return result

    def __setDisplaySettings(self):
        properties = base.win.getProperties()
        if properties.getFullscreen():
            screensize = '%s x %s' % (properties.getXSize(), properties.getYSize())
        else:
            screensize = TTLocalizer.OptionsPageDisplayWindowed
        isEmbedded = self.isPropertiesEmbedded(properties)
        if isEmbedded:
            screensize = TTLocalizer.OptionsPageDisplayEmbedded
        api = base.pipe.getInterfaceName()
        settings = {'screensize': screensize,
         'api': api}
        if self.ChangeDisplayAPI:
            OptionsPage.notify.debug('change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettings % settings
        else:
            OptionsPage.notify.debug('no change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettingsNoApi % settings
        self.DisplaySettings_Label['text'] = text

    def __doSpeedChatStyleLeft(self):
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleIndex = self.speedChatStyleIndex - 1
            self.updateSpeedChatStyle()

    def __doSpeedChatStyleRight(self):
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleIndex = self.speedChatStyleIndex + 1
            self.updateSpeedChatStyle()

    def updateSpeedChatStyle(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[self.speedChatStyleIndex]
        newSCColorScheme = SCColorScheme.SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChatStyleText.setColorScheme(newSCColorScheme)
        self.speedChatStyleText.clearMenu()
        colorName = SCStaticTextTerminal.SCStaticTextTerminal(nameKey)
        self.speedChatStyleText.append(colorName)
        self.speedChatStyleText.finalize()
        self.speedChatStyleText.setPos(0.445 - self.speedChatStyleText.getWidth() * self.speed_chat_scale / 2, 0, self.speedChatStyleText.getPos()[2])
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleLeftArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleLeftArrow['state'] = DGG.DISABLED
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleRightArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleRightArrow['state'] = DGG.DISABLED
        base.localAvatar.b_setSpeedChatStyleIndex(self.speedChatStyleIndex)
        
    def __doChatStyleLeft(self):
        if self.chatStyleIndex > 0:
            self.chatStyleIndex = self.chatStyleIndex - 1
            self.updateChatStyle()

    def __doChatStyleRight(self):
        if self.chatStyleIndex < len(chatStyles) - 1:
            self.chatStyleIndex = self.chatStyleIndex + 1
            self.updateChatStyle()
            
    def updateChatStyle(self):
        nameKey, color = chatStyles[self.chatStyleIndex]
        newChatColorScheme = ChatColorScheme.ChatColorScheme(frameColor=(color[0], color[1], color[2]))
        self.chatStyleText.setColorScheme(newChatColorScheme)
        self.chatStyleText.clearMenu()
        colorName = ChatStaticTextTerminal.ChatStaticTextTerminal(nameKey)
        self.chatStyleText.append(colorName)
        self.chatStyleText.finalize()
        self.chatStyleText.setPos(0.445 - self.chatStyleText.getWidth() * self.speed_chat_scale / 2, 0, self.chatStyleText.getPos()[2])
        if self.chatStyleIndex > 0:
            self.chatStyleLeftArrow['state'] = DGG.NORMAL
        else:
            self.chatStyleLeftArrow['state'] = DGG.DISABLED
        if self.chatStyleIndex < len(chatStyles) - 1:
            self.chatStyleRightArrow['state'] = DGG.NORMAL
        else:
            self.chatStyleRightArrow['state'] = DGG.DISABLED
        base.localAvatar.b_setChatStyleIndex(self.chatStyleIndex)

    def writeDisplaySettings(self, task = None):
        if not self.displaySettingsChanged:
            return
        taskMgr.remove(self.DisplaySettingsTaskName)
        self.notify.info('writing new display settings %s, fullscreen %s, embedded %s, %s to SettingsFile.' % (self.displaySettingsSize,
         self.displaySettingsFullscreen,
         self.displaySettingsEmbedded,
         self.displaySettingsApi))
        Settings['resolutionDimensions'] = [self.displaySettingsSize[0], self.displaySettingsSize[1]]
        Settings['windowedMode'] = not self.displaySettingsFullscreen
        Settings['embeddedMode'] = self.displaySettingsEmbedded
        if self.displaySettingsApiChanged:
            api = self.DisplaySettingsApiMap.get(self.displaySettingsApi)
            if api == None:
                self.notify.warning('Cannot save unknown display API: %s' % self.displaySettingsApi)
            else:
                Settings.setDisplayDriver(api)
        Settings.writeSettings()
        self.displaySettingsChanged = 0
        return Task.done


class CodesTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodesTabPage')

    def __init__(self, parent = aspect2d):
        self.parent = parent
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        instructionGui = cdrGui.find('**/tt_t_gui_sbk_cdrPresent')
        flippyGui = cdrGui.find('**/tt_t_gui_sbk_cdrFlippy')
        codeBoxGui = cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox')
        self.resultPanelSuccessGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_success')
        self.resultPanelFailureGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_failure')
        self.resultPanelErrorGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_error')
        self.successSfx = base.loader.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.ogg')
        self.failureSfx = base.loader.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.ogg')
        self.instructionPanel = DirectFrame(parent=self, relief=None, image=instructionGui, image_scale=0.8, text=TTLocalizer.CdrInstructions, text_pos=TTLocalizer.OPCodesInstructionPanelTextPos, text_align=TextNode.ACenter, text_scale=TTLocalizer.OPCodesResultPanelTextScale, text_wordwrap=TTLocalizer.OPCodesInstructionPanelTextWordWrap, pos=(-0.429, 0, -0.05))
        self.codeBox = DirectFrame(parent=self, relief=None, image=codeBoxGui, pos=(0.433, 0, 0.35))
        self.flippyFrame = DirectFrame(parent=self, relief=None, image=flippyGui, pos=(0.44, 0, -0.353))
        self.codeInput = DirectEntry(parent=self.codeBox, relief=DGG.GROOVE, scale=0.08, pos=(-0.33, 0, -0.006), borderWidth=(0.05, 0.05), frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL, text_align=TextNode.ALeft, text_scale=TTLocalizer.OPCodesInputTextScale, width=10.5, numLines=1, focus=1, backgroundFocus=0, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0, command=self.__submitCode)
        submitButtonGui = loader.loadModel('phase_3/models/gui/quit_button')
        self.submitButton = DirectButton(parent=self, relief=None, image=(submitButtonGui.find('**/QuitBtn_UP'),
         submitButtonGui.find('**/QuitBtn_DN'),
         submitButtonGui.find('**/QuitBtn_RLVR'),
         submitButtonGui.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=1.15, state=DGG.NORMAL, text=TTLocalizer.NameShopSubmitButton, text_scale=TTLocalizer.OPCodesSubmitTextScale, text_align=TextNode.ACenter, text_pos=TTLocalizer.OPCodesSubmitTextPos, text3_fg=(0.5, 0.5, 0.5, 0.75), textMayChange=0, pos=(0.45, 0.0, 0.0896), command=self.__submitCode)
        self.resultPanel = DirectFrame(parent=self, relief=None, image=self.resultPanelSuccessGui, text='', text_pos=TTLocalizer.OPCodesResultPanelTextPos, text_align=TextNode.ACenter, text_scale=TTLocalizer.OPCodesResultPanelTextScale, text_wordwrap=TTLocalizer.OPCodesResultPanelTextWordWrap, pos=(-0.42, 0, -0.0567))
        self.resultPanel.hide()
        closeButtonGui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.closeButton = DirectButton(parent=self.resultPanel, pos=(0.296, 0, -0.466), relief=None, state=DGG.NORMAL, image=(closeButtonGui.find('**/CloseBtn_UP'), closeButtonGui.find('**/CloseBtn_DN'), closeButtonGui.find('**/CloseBtn_Rllvr')), image_scale=(1, 1, 1), command=self.__hideResultPanel)
        closeButtonGui.removeNode()
        cdrGui.removeNode()
        submitButtonGui.removeNode()
        return

    def enter(self):
        self.show()
        localAvatar.chatMgr.fsm.request('otherDialog')
        self.codeInput['focus'] = 1
        self.codeInput.enterText('')
        self.__enableCodeEntry()

    def exit(self):
        self.resultPanel.hide()
        self.hide()
        localAvatar.chatMgr.fsm.request('mainMenu')

    def unload(self):
        self.instructionPanel.destroy()
        self.instructionPanel = None
        self.codeBox.destroy()
        self.codeBox = None
        self.flippyFrame.destroy()
        self.flippyFrame = None
        self.codeInput.destroy()
        self.codeInput = None
        self.submitButton.destroy()
        self.submitButton = None
        self.resultPanel.destroy()
        self.resultPanel = None
        self.closeButton.destroy()
        self.closeButton = None
        del self.successSfx
        del self.failureSfx
        return

    def __submitCode(self, input = None):
        if input == None:
            input = self.codeInput.get()
        self.codeInput['focus'] = 1
        if input == '':
            return
        messenger.send('wakeup')
        if hasattr(base, 'codeRedemptionMgr'):
            base.codeRedemptionMgr.redeemCode(input, self.__getCodeResult)
        self.codeInput.enterText('')
        self.__disableCodeEntry()
        return

    def __getCodeResult(self, result, awardMgrResult):
        self.notify.debug('result = %s' % result)
        self.notify.debug('awardMgrResult = %s' % awardMgrResult)
        self.__enableCodeEntry()
        if result == 0:
            self.resultPanel['image'] = self.resultPanelSuccessGui
            self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
        elif result == 1 or result == 3:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultInvalidCode
        elif result == 2:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultExpiredCode
        elif result == 4:
            self.resultPanel['image'] = self.resultPanelErrorGui
            if awardMgrResult == 0:
                self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
            elif awardMgrResult == 1 or awardMgrResult == 2 or awardMgrResult == 15 or awardMgrResult == 16:
                self.resultPanel['text'] = TTLocalizer.CdrResultUnknownError
            elif awardMgrResult == 3 or awardMgrResult == 4:
                self.resultPanel['text'] = TTLocalizer.CdrResultMailboxFull
            elif awardMgrResult == 5 or awardMgrResult == 10:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInMailbox
            elif awardMgrResult == 6 or awardMgrResult == 7 or awardMgrResult == 11:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInQueue
            elif awardMgrResult == 8:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInCloset
            elif awardMgrResult == 9:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyBeingWorn
            elif awardMgrResult == 12 or awardMgrResult == 13 or awardMgrResult == 14:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyReceived
        elif result == 5:
            self.resultPanel['text'] = TTLocalizer.CdrResultTooManyFails
            self.__disableCodeEntry()
        elif result == 6:
            self.resultPanel['text'] = TTLocalizer.CdrResultServiceUnavailable
            self.__disableCodeEntry()
        if result == 0:
            self.successSfx.play()
        else:
            self.failureSfx.play()
        self.resultPanel.show()

    def __hideResultPanel(self):
        self.resultPanel.hide()

    def __disableCodeEntry(self):
        self.codeInput['state'] = DGG.DISABLED
        self.submitButton['state'] = DGG.DISABLED

    def __enableCodeEntry(self):
        self.codeInput['state'] = DGG.NORMAL
        self.codeInput['focus'] = 1
        self.submitButton['state'] = DGG.NORMAL
