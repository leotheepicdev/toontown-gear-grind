from otp.otpbase import OTPBase
from otp.otpbase import OTPLauncherGlobals
from otp.otpbase import OTPGlobals
from direct.showbase.PythonUtil import *
from . import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from . import ToontownLoader
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from panda3d.core import *
import sys
import os
import math
from lib import limeade
import os
from toontown.toonbase import ToontownAccess
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from toontown.launcher import ToontownDownloadWatcher
from toontown.toonbase.TTFrameRateMeter import TTFrameRateMeter
from lib.libotp import ChatBalloon, NametagGlobals, MarginManager
from direct.interval.IntervalGlobal import Sequence, Func, Wait

class ToonBase(OTPBase.OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonBase')

    def __init__(self):
        if not config.GetInt('ignore-user-options', 0):
            Settings.readSettings()
            mode = not Settings['windowedMode']
            music = Settings['music']
            sfx = Settings['sfx']
            toonChatSounds = Settings['toonChatSounds']
            musicVol = Settings['musicVolume']
            sfxVol = Settings['sfxVolume']
            resList = [(640, 480),
             (800, 600),
             (1024, 768),
             (1280, 1024),
             (1600, 1200)]
            resolutionDimensions = Settings['resolutionDimensions']
            res = (resolutionDimensions[0], resolutionDimensions[1])
            if res not in resList:
                res = (800, 600)
            if mode == None:
                mode = 1
            loadPrcFileData('toonBase Settings Window Res', 'win-size %s %s' % (res[0], res[1]))
            loadPrcFileData('toonBase Settings Window FullScreen', 'fullscreen %s' % mode)
            loadPrcFileData('toonBase Settings Music Active', 'audio-music-active %s' % music)
            loadPrcFileData('toonBase Settings Sound Active', 'audio-sfx-active %s' % sfx)
            loadPrcFileData('toonBase Settings Music Volume', 'audio-master-music-volume %s' % musicVol)
            loadPrcFileData('toonBase Settings Sfx Volume', 'audio-master-sfx-volume %s' % sfxVol)
            loadPrcFileData('toonBase Settings Toon Chat Sounds', 'toon-chat-sounds %s' % toonChatSounds)
        OTPBase.OTPBase.__init__(self)
        if not self.isMainWindowOpen():
            try:
                launcher.setPandaErrorCode(7)
            except:
                pass

            sys.exit(1)
        self.disableShowbaseMouse()
        self.addCullBins()
        base.debugRunningMultiplier /= OTPGlobals.ToonSpeedFactor
        self.toonChatSounds = self.config.GetBool('toon-chat-sounds', 1)
        self.placeBeforeObjects = config.GetBool('place-before-objects', 1)
        self.endlessQuietZone = False
        self.wantDynamicShadows = 0
        self.exitErrorCode = 0
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(ToontownGlobals.DefaultCameraFov / (4. / 3.))
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        self.musicManager.setVolume(0.65)
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        tpm = TextPropertiesManager.getGlobalPtr()
        candidateActive = TextProperties()
        candidateActive.setTextColor(0, 0, 1, 1)
        tpm.setProperties('candidate_active', candidateActive)
        candidateInactive = TextProperties()
        candidateInactive.setTextColor(0.3, 0.3, 0.7, 1)
        tpm.setProperties('candidate_inactive', candidateInactive)
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.exitFunc = self.userExit
        if 'launcher' in __builtins__ and launcher:
            launcher.setPandaErrorCode(11)
        globalClock.setMaxDt(0.2)
        if self.config.GetBool('want-particles', 1) == 1:
            self.notify.debug('Enabling particles')
            self.enableParticles()
        self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)
        self.accept('f3', self.toggleGui)
        self.accept('panda3d-render-error', self.panda3dRenderError)
        oldLoader = self.loader
        self.loader = ToontownLoader.ToontownLoader(self)
        __builtins__['loader'] = self.loader
        oldLoader.destroy()
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.friendMode = self.config.GetBool('switchboard-friends', 0)
        self.wantPets = self.config.GetBool('want-pets', 1)
        self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
        self.wantKarts = self.config.GetBool('want-karts', 1)
        self.wantNewSpecies = self.config.GetBool('want-new-species', 0)
        self.inactivityTimeout = self.config.GetFloat('inactivity-timeout', ToontownGlobals.KeyboardTimeout)
        if self.inactivityTimeout:
            self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
            self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
        self.randomMinigameAbort = self.config.GetBool('random-minigame-abort', 0)
        self.randomMinigameDisconnect = self.config.GetBool('random-minigame-disconnect', 0)
        self.randomMinigameNetworkPlugPull = self.config.GetBool('random-minigame-netplugpull', 0)
        self.autoPlayAgain = self.config.GetBool('auto-play-again', 0)
        self.skipMinigameReward = self.config.GetBool('skip-minigame-reward', 0)
        self.wantMinigameDifficulty = self.config.GetBool('want-minigame-difficulty', 0)
        self.minigameDifficulty = self.config.GetFloat('minigame-difficulty', -1.0)
        if self.minigameDifficulty == -1.0:
            del self.minigameDifficulty
        self.minigameSafezoneId = self.config.GetInt('minigame-safezone-id', -1)
        if self.minigameSafezoneId == -1:
            del self.minigameSafezoneId
        cogdoGameSafezoneId = self.config.GetInt('cogdo-game-safezone-id', -1)
        cogdoGameDifficulty = self.config.GetFloat('cogdo-game-difficulty', -1)
        if cogdoGameDifficulty != -1:
            self.cogdoGameDifficulty = cogdoGameDifficulty
        if cogdoGameSafezoneId != -1:
            self.cogdoGameSafezoneId = cogdoGameSafezoneId
        ToontownBattleGlobals.SkipMovie = self.config.GetBool('skip-battle-movies', 0)
        self.creditCardUpFront = self.config.GetInt('credit-card-up-front', -1)
        if self.creditCardUpFront == -1:
            del self.creditCardUpFront
        else:
            self.creditCardUpFront = self.creditCardUpFront != 0
        self.housingEnabled = self.config.GetBool('want-housing', 1)
        self.cannonsEnabled = self.config.GetBool('estate-cannons', 0)
        self.fireworksEnabled = self.config.GetBool('estate-fireworks', 0)
        self.dayNightEnabled = self.config.GetBool('estate-day-night', 0)
        self.cloudPlatformsEnabled = self.config.GetBool('estate-clouds', 0)
        self.greySpacing = self.config.GetBool('allow-greyspacing', 0)
        self.goonsEnabled = self.config.GetBool('estate-goon', 0)
        self.restrictTrialers = self.config.GetBool('restrict-trialers', 1)
        self.roamingTrialers = self.config.GetBool('roaming-trialers', 1)
        self.slowQuietZone = self.config.GetBool('slow-quiet-zone', 0)
        self.slowQuietZoneDelay = self.config.GetFloat('slow-quiet-zone-delay', 5)
        self.killInterestResponse = self.config.GetBool('kill-interest-response', 0)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.3)
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        del tpMgr
        self.lastScreenShotTime = globalClock.getRealTime()
        self.accept('InputState-forward', self.__walking)
        self.canScreenShot = 1
        self.glitchCount = 0
        self.walking = 0
        self.oldX = max(1, base.win.getXSize())
        self.oldY = max(1, base.win.getYSize())
        self.aspectRatio = float(self.oldX) / self.oldY
        def printDOs():
            print(base.cr.doId2do)
        if __debug__:
            self.accept('f4', printDOs)
            self.accept('f10', base.oobe)
            self.accept(ToontownGlobals.LimeadeHotkey, self.refreshCode)
        self.frameRateMeter = None
        self.SCREENSHOT_PATH = 'user/screenshots'
        self.DISTRICT_FILENAME = 'user/last-district.txt'
        self.snapshotSfx = loader.loadSfx('phase_4/audio/sfx/Photo_shutter.ogg')
        self.flashTrack = None
        self.summonDialog = None
        self.wantDiscordPresence = config.GetBool('want-discord-presence', False)
        self.haveDiscordOpen = False

    def isClientBuilt(self):
        try:
            from data import TTGGData
            return True
        except:
            return False

    def openMainWindow(self, *args, **kw):
        result = OTPBase.OTPBase.openMainWindow(self, *args, **kw)

        self.setCursorAndIcon()

        return result

    def setCursorAndIcon(self):
        wp = WindowProperties()

        if self.isClientBuilt():
            wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/toonmono.cur')))
            wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/icon.ico')))
        else:
            wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/phase_3/etc/toonmono.cur')))
            wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/phase_3/etc/icon.ico')))

        self.win.requestProperties(wp)

    def windowEvent(self, win):
        OTPBase.OTPBase.windowEvent(self, win)
        if not config.GetInt('keep-aspect-ratio', 0):
            return
        x = max(1, win.getXSize())
        y = max(1, win.getYSize())
        maxX = base.pipe.getDisplayWidth()
        maxY = base.pipe.getDisplayHeight()
        cwp = win.getProperties()
        originX = 0
        originY = 0
        if cwp.hasOrigin():
            originX = cwp.getXOrigin()
            originY = cwp.getYOrigin()
            if originX > maxX:
                originX = originX - maxX
            if originY > maxY:
                oringY = originY - maxY
        maxX -= originX
        maxY -= originY
        if math.fabs(x - self.oldX) > math.fabs(y - self.oldY):
            newY = x / self.aspectRatio
            newX = x
            if newY > maxY:
                newY = maxY
                newX = self.aspectRatio * maxY
        else:
            newX = self.aspectRatio * y
            newY = y
            if newX > maxX:
                newX = maxX
                newY = maxX / self.aspectRatio
        wp = WindowProperties()
        wp.setSize(newX, newY)
        base.win.requestProperties(wp)
        base.cam.node().getLens().setFilmSize(newX, newY)
        self.oldX = newX
        self.oldY = newY

    def disableShowbaseMouse(self):
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.detachNode()
        if base.mouse2cam:
            self.mouse2cam.detachNode()

    def updateDistrict(self, districtName):
        if Settings['streamerSupport']:
            with open(self.DISTRICT_FILENAME, 'w') as f:
                f.write(districtName)

    def addCullBins(self):
        cullBinMgr = CullBinManager.getGlobalPtr()
        cullBinMgr.addBin('gui-popup', CullBinManager.BTUnsorted, 60)
        cullBinMgr.addBin('shadow', CullBinManager.BTFixed, 15)
        cullBinMgr.addBin('ground', CullBinManager.BTFixed, 14)

    def __walking(self, pressed):
        self.walking = pressed

    def toggleGui(self):
        if aspect2d.isHidden():
            aspect2d.show()
        else:
            aspect2d.hide()

    def takeScreenShot(self):
        if not os.path.exists(self.SCREENSHOT_PATH):
            os.makedirs(self.SCREENSHOT_PATH)

        namePrefix = '{0}/screenshot'.format(self.SCREENSHOT_PATH)
        namePrefix = launcher.logPrefix + namePrefix
        timedif = globalClock.getRealTime() - self.lastScreenShotTime
        if self.glitchCount > 10 and self.walking:
            return
        if timedif < 1.0 and self.walking:
            self.glitchCount += 1
            return
        if not hasattr(self, 'localAvatar'):
            self.screenshot(namePrefix=namePrefix)
            self.lastScreenShotTime = globalClock.getRealTime()
            return
        coordOnScreen = self.config.GetBool('screenshot-coords', 0)
        self.localAvatar.stopThisFrame = 1
        ctext = self.localAvatar.getAvPosStr()
        self.screenshotStr = ''
        messenger.send('takingScreenshot')
        if coordOnScreen:
            coordTextLabel = DirectLabel(pos=(-0.81, 0.001, -0.87), text=ctext, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
            coordTextLabel.setBin('gui-popup', 0)
            strTextLabel = None
            if len(self.screenshotStr):
                strTextLabel = DirectLabel(pos=(0.0, 0.001, 0.9), text=self.screenshotStr, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
                strTextLabel.setBin('gui-popup', 0)
        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix=namePrefix, imageComment=ctext + ' ' + self.screenshotStr)
        self.lastScreenShotTime = globalClock.getRealTime()
        if coordOnScreen:
            if strTextLabel is not None:
                strTextLabel.destroy()
            coordTextLabel.destroy()
        if self.flashTrack and self.flashTrack.isPlaying():
            self.flashTrack.finish()
        base.playSfx(self.snapshotSfx)
        self.transitions.setFadeColor(1, 1, 1)
        self.transitions.fadeOut(0.15)
        self.flashTrack = Sequence(Func(self.transitions.fadeIn, 0.8), Wait(1), Func(self.transitions.setFadeColor, 0, 0, 0))
        self.flashTrack.start()
        return

    def addScreenshotString(self, str):
        if len(self.screenshotStr):
            self.screenshotStr += '\n'
        self.screenshotStr += str

    def initNametagGlobals(self):
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox').node())
        thought3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_thought_cutout').node())
        speech2d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_noarrow').node())
        chatButtonGui = loader.loadModel('phase_3/models/gui/chat_button_gui')
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/Horiz_Arrow_UP'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/Horiz_Arrow_DN'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/Horiz_Arrow_Rllvr'))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find('**/CloseBtn_UP'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find('**/CloseBtn_DN'))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find('**/CloseBtn_Rllvr'))
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        self.leftCells = [mm.addGridCell(0, 1, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -1.5)), mm.addGridCell(0, 2, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -1.16667)), mm.addGridCell(0, 3, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -0.833333))]
        self.bottomCells = [mm.addGridCell(0.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (-0.888889, 0, 0.166667)),
         mm.addGridCell(1.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (-0.444444, 0, 0.166667)),
         mm.addGridCell(2.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0, 0, 0.166667)),
         mm.addGridCell(3.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0.444444, 0, 0.166667)),
         mm.addGridCell(4.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0.888889, 0, 0.166667))]
        self.rightCells = [mm.addGridCell(5, 2, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopRight, (-0.222222, 0, -1.16667)), mm.addGridCell(5, 1, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopRight, (-0.222222, 0, -1.5))]

    def setCellsAvailable(self, cell_list, available):
        for cell in cell_list:
            self.marginManager.setCellAvailable(cell, available)

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        self.downloadWatcher = None
        return

    def startShow(self, cr, launcherServer = None):
        self.cr = cr
        base.graphicsEngine.renderFrame()
        self.downloadWatcher = ToontownDownloadWatcher.ToontownDownloadWatcher(TTLocalizer.LauncherPhaseNames)
        if launcher.isDownloadComplete():
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce('launcherAllPhasesComplete', self.cleanupDownloadWatcher)

        if __debug__:
            gameServer = os.getenv('TOONTOWN_GAMESERVER')
        else:
            gameServer = config.GetString('game-server', 'game.geargrind.tech')

        if gameServer:
            self.notify.info('Using game-server from Configrc: %s ' % gameServer)
        elif launcherServer:
            gameServer = launcherServer
            self.notify.info('Using gameServer from launcher: %s ' % gameServer)
        else:
            gameServer = '127.0.0.1'
        serverPort = base.config.GetInt('server-port', 6667)
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            url.setScheme('s')

            if url.getServer() == '127.0.0.1' or 'game.geargrind.tech':
                url.setScheme('')

            if not url.hasPort():
                url.setPort(serverPort)
            serverList.append(url)

        if len(serverList) == 1:
            failover = base.config.GetString('server-failover', '')
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)

        cr.loginFSM.request('connect', [serverList])
        self.ttAccess = ToontownAccess.ToontownAccess()
        self.ttAccess.initModuleInfo()

    def removeGlitchMessage(self):
        self.ignore('InputState-forward')
        print('ignoring InputState-forward')

    def exitShow(self, errorCode = None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        if errorCode:
            launcher.setPandaErrorCode(errorCode)
        else:
            launcher.setPandaErrorCode(0)
        sys.exit()

    def setExitErrorCode(self, code):
        self.exitErrorCode = code
        if os.name == 'nt':
            exitCode2exitPage = {OTPLauncherGlobals.ExitEnableChat: 'chat',
             OTPLauncherGlobals.ExitSetParentPassword: 'setparentpassword',
             OTPLauncherGlobals.ExitPurchase: 'purchase'}
            if code in exitCode2exitPage:
                launcher.setRegistry('EXIT_PAGE', exitCode2exitPage[code])

    def getExitErrorCode(self):
        return self.exitErrorCode

    def userExit(self):
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass

        if hasattr(self, 'ttAccess'):
            self.ttAccess.delete()
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)
        base.cr._userLoggingOut = False
        try:
            localAvatar
        except:
            pass
        else:
            messenger.send('clientLogout')
            self.cr.dumpAllSubShardObjects()

        self.cr.loginFSM.request('shutdown')
        self.notify.warning('Could not request shutdown; exiting anyway.')
        self.exitShow()

    def panda3dRenderError(self):
        launcher.setPandaErrorCode(14)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        OTPBase.OTPBase.playMusic(self, music, looping, interrupt, volume, time)

    def setFrameRateMeter(self, flag):
        if flag:
            if not self.frameRateMeter:
                self.frameRateMeter = TTFrameRateMeter('frameRateMeter')
                self.frameRateMeter.setupWindow(self.win)
        else:
            if self.frameRateMeter:
                self.frameRateMeter.clearWindow()
                self.frameRateMeter = None

    def refreshCode(self):
        limeade.refresh()

        if hasattr(self, 'localAvatar'):
            self.localAvatar.setSystemMessage(0, 'Refreshed client modules.')