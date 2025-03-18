from panda3d.core import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.char import Char
from otp.avatar import Avatar
from toontown.toon import Toon
from toontown.toon import LocalToon
from toontown.toon import ToonDNA
from toontown.char import CharDNA
from direct.fsm import ClassicFSM, State
from direct.fsm import StateData
from toontown.toonbase import ToontownGlobals
from direct.actor.Actor import Actor
from direct.task import Task
from direct.gui.DirectGui import *
from toontown.toontowngui.ToontownButton import ToontownButton
from toontown.toonbase import TTLocalizer
from .MakeAToonGlobals import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from . import GenderShop
from . import BodyShop
from . import ColorShop
from . import MakeClothesGUI
from . import NameShop
import random, time

class MakeAToon(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('MakeAToon')

    def __init__(self, parentFSM, avList, doneEvent, index, isPaid, isRewriteSession=False):
        self.isPaid = isPaid
        StateData.StateData.__init__(self, doneEvent)
        self.phase = 3
        self.names = ['',
         '',
         '',
         '']
        self.dnastring = None
        self.dna = None
        self.progressing = 0
        self.isRewriteSession = isRewriteSession
        self.toonPosition = Point3(-2, 1, 0)
        self.nameShopToonPosition = Point3(4, 1, 0)
        self.toonScale = Point3(1, 1, 1)
        self.toonHpr = Point3(180, 0, 0)
        self.leftTime = 1.6
        self.rightTime = 1
        self.slide = 0
        self.nameList = []
        self.warp = 0
        self.namelessPotAv = None
        for av in avList:
            if av.position == index:
                self.warp = 1
                self.namelessPotAv = av
            self.nameList.append(av.name)

        self.fsm = ClassicFSM.ClassicFSM('MakeAToon', [State.State('Init', self.enterInit, self.exitInit, ['GenderShop', 'NameShop', 'BodyShop']),
         State.State('GenderShop', self.enterGenderShop, self.exitGenderShop, ['BodyShop']),
         State.State('BodyShop', self.enterBodyShop, self.exitBodyShop, ['GenderShop', 'ColorShop']),
         State.State('ColorShop', self.enterColorShop, self.exitColorShop, ['BodyShop', 'ClothesShop', 'Done']),
         State.State('ClothesShop', self.enterClothesShop, self.exitClothesShop, ['ColorShop', 'NameShop']),
         State.State('NameShop', self.enterNameShop, self.exitNameShop, ['ClothesShop']),
         State.State('Done', self.enterDone, self.exitDone, [])], 'Init', 'Done')
        self.parentFSM = parentFSM
        self.parentFSM.getStateNamed('createAvatar').addChild(self.fsm)
        self.gs = GenderShop.GenderShop(self, 'GenderShop-done')
        self.bs = BodyShop.BodyShop('BodyShop-done')
        self.cos = ColorShop.ColorShop('ColorShop-done', self.namelessPotAv)
        self.cls = MakeClothesGUI.MakeClothesGUI('ClothesShop-done')
        self.ns = NameShop.NameShop(self, 'NameShop-done', avList, index, self.isPaid)
        self.shop = GENDERSHOP
        self.shopsVisited = []
        if self.warp:
            if self.isRewriteSession:
                self.shopsVisited = [GENDERSHOP, CLOTHESSHOP, NAMESHOP]
            else:
                self.shopsVisited = [GENDERSHOP,
                 BODYSHOP,
                 COLORSHOP,
                 CLOTHESSHOP]
        self.music = None
        self.soundBack = None
        self.fsm.enterInitialState()
        self.hprDelta = -1
        self.toon = None
        base.updateDistrict('Make A Toon')

    def getToon(self):
        return self.toon

    def enter(self):
        if base.wantDiscordPresence and base.haveDiscordOpen:
            activity = {
                'state': 'Making A Toon',
                'start': int(time.time()),
                'large_text': 'Toontown: Gear Grind',
                'large_image': 'rp'
            }

            base.cr.discordPresence.updatePresence(activity)

        self.notify.debug('Starting Make A Toon.')
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: MAKEATOON: Starting Make A Toon')
        base.camLens.setMinFov(ToontownGlobals.MakeAToonCameraFov/ (4/3))
        base.playMusic(self.music, looping=1, volume=self.musicVolume)
        camera.setPosHpr(0, -12.3501, 3.15, 0, 0, 0)
        if self.warp:
            if not self.isRewriteSession:
                if self.toon.style.torso[1] == 's':
                    self.toon.gender = 's'
                else:
                    self.toon.gender = 'd'
            else:
                self.toon.setPos(self.toonPosition)
                self.toon.setHpr(self.toonHpr)
            self.toon.reparentTo(render)
            self.toon.loop('neutral')
        self.guiTopBar.show()
        self.guiBottomBar.show()
        self.guiCancelButton.show()
        if self.warp:
            if self.isRewriteSession:
                self.progressing = 0
                self.guiLastButton.hide()
                self.fsm.request('BodyShop')
            else:
                self.progressing = 0
                self.guiLastButton.hide()
                self.fsm.request('NameShop')
        else:
            self.fsm.request('GenderShop')

    def exit(self):
        base.camLens.setMinFov(ToontownGlobals.DefaultCameraFov/(4/3))
        self.guiTopBar.hide()
        self.guiBottomBar.hide()
        self.guiCheckButton.hide()
        self.guiCancelButton.hide()
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        self.music.stop()
        self.fsm.request('Done')
        self.room.reparentTo(hidden)

    def load(self):
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        create_gui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        guiAcceptUp = gui.find('**/tt_t_gui_mat_okUp')
        guiAcceptDown = gui.find('**/tt_t_gui_mat_okDown')
        guiCancelUp = gui.find('**/tt_t_gui_mat_closeUp')
        guiCancelDown = gui.find('**/tt_t_gui_mat_closeDown')
        guiNextUp = gui.find('**/tt_t_gui_mat_nextUp')
        guiNextDown = gui.find('**/tt_t_gui_mat_nextDown')
        guiNextDisabled = gui.find('**/tt_t_gui_mat_nextDisabled')
        skipTutorialUp = gui.find('**/tt_t_gui_mat_skipUp')
        skipTutorialDown = gui.find('**/tt_t_gui_mat_skipDown')
        rotateUp = gui.find('**/tt_t_gui_mat_arrowRotateUp')
        rotateDown = gui.find('**/tt_t_gui_mat_arrowRotateDown')
        self.guiTopBar = DirectFrame(relief=None, image=create_gui.find('**/CrtATn_TopBar'), text=TTLocalizer.CreateYourToon, text_font=ToontownGlobals.getSignFont(), text_fg=(0.0, 0.65, 0.35, 1), text_scale=0.18, text_pos=(0, -0.03), pos=(0, 0, 0.86))
        self.guiTopBar.hide()
        self.guiBottomBar = DirectFrame(relief=None, image_scale=(1.25, 1, 1), pos=(0.01, 0, -0.86))
        self.guiBottomBar.hide()
        self.guiCheckButton = ToontownButton(parent=base.a2dBottomRight, anim='stretch', relief=None, image=(guiAcceptUp,
         guiAcceptDown,
         guiAcceptUp,
         guiAcceptDown), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.158333, 0, 0.122), command=self.__handleNext, text=('', TTLocalizer.MakeAToonDone, TTLocalizer.MakeAToonDone), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_align=TextNode.ARight, text_pos=(0.13, 0.13), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiCheckButton.hide()
        self.guiCancelButton = ToontownButton(parent=base.a2dBottomLeft, anim='stretch', relief=None, image=(guiCancelUp,
         guiCancelDown,
         guiCancelUp,
         guiCancelDown), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(0.164333, 0, 0.129), command=self.__handleCancel, text=('', TTLocalizer.MakeAToonCancel, TTLocalizer.MakeAToonCancel), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.MATguiCancelButton, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiCancelButton.hide()
        self.guiNextButton = ToontownButton(parent=base.a2dBottomRight, anim='stretch', relief=None, image=(guiNextUp,
         guiNextDown,
         guiNextUp,
         guiNextDisabled), image_scale=(0.3, 0.3, 0.3), image1_scale=(0.35, 0.35, 0.35), image2_scale=(0.35, 0.35, 0.35), pos=(-0.158333, 0, 0.122), command=self.__handleNext, text=('',
         TTLocalizer.MakeAToonNext,
         TTLocalizer.MakeAToonNext,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.MATguiNextButton, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiNextButton.hide()
        self.guiLastButton = ToontownButton(parent=base.a2dBottomRight, anim='stretch', relief=None, image=(guiNextUp,
         guiNextDown,
         guiNextUp,
         guiNextDown), image3_color=Vec4(0.5, 0.5, 0.5, 0.75), image_scale=(-0.3, 0.3, 0.3), image1_scale=(-0.35, 0.35, 0.35), image2_scale=(-0.35, 0.35, 0.35), pos=(-0.498333, 0, 0.122), command=self.__handleLast, text=('',
         TTLocalizer.MakeAToonLast,
         TTLocalizer.MakeAToonLast,
         ''), text_font=ToontownGlobals.getInterfaceFont(), text_scale=0.08, text_pos=(0, 0.115), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.guiLastButton.hide()
        self.rotateLeftButton = ToontownButton(parent=self.guiBottomBar, anim='stretch', relief=None, image=(rotateUp,
         rotateDown,
         rotateUp,
         rotateDown), image_scale=(-0.4, 0.4, 0.4), image1_scale=(-0.5, 0.5, 0.5), image2_scale=(-0.5, 0.5, 0.5), pos=(-0.729249, 0, 0.202961))
        self.rotateLeftButton.hide()
        self.rotateLeftButton.bind(DGG.B1PRESS, self.rotateToonLeft)
        self.rotateLeftButton.bind(DGG.B1RELEASE, self.stopToonRotateLeftTask)
        self.rotateRightButton = ToontownButton(parent=self.guiBottomBar, anim='stretch', relief=None, image=(rotateUp,
         rotateDown,
         rotateUp,
         rotateDown), image_scale=(0.4, 0.4, 0.4), image1_scale=(0.5, 0.5, 0.5), image2_scale=(0.5, 0.5, 0.5), pos=(-0.129249, 0, 0.206116))
        self.rotateRightButton.hide()
        self.rotateRightButton.bind(DGG.B1PRESS, self.rotateToonRight)
        self.rotateRightButton.bind(DGG.B1RELEASE, self.stopToonRotateRightTask)
        gui.removeNode()
        create_gui.removeNode()
        self.room = loader.loadModel('phase_3/models/makeatoon/MakeAToon')
        self.room.reparentTo(render)

        ee = DirectFrame(pos=(-1, 1, 1), frameSize=(-.01, 0.01, -.01, 0.01), frameColor=(0, 0, 0, 0.05), state='normal')
        ee.bind(DGG.B1PRESS, lambda x, ee = ee: self.toggleSlide())
        self.eee = ee
        smokeSeqNode = SequenceNode('smoke')
        smokeModel = loader.loadModel('phase_3/models/makeatoon/tt_m_ara_mat_smoke')
        smokeFrameList = list(smokeModel.findAllMatches('**/smoke_*'))
        smokeFrameList.reverse()
        for smokeFrame in smokeFrameList:
            smokeSeqNode.addChild(smokeFrame.node())

        smokeSeqNode.setFrameRate(12)
        self.smoke = render.attachNewNode(smokeSeqNode)
        self.smoke.setScale(1, 1, 0.75)
        self.smoke.hide()
        if self.warp:
            self.dna = ToonDNA.ToonDNA()
            self.dna.makeFromNetString(self.namelessPotAv.dna)
            self.toon = Toon.Toon()
            self.toon.setDNA(self.dna)
            self.toon.useLOD(1000)
            self.toon.setNameVisible(0)
            self.toon.startBlink()
            self.toon.startLookAround()
        self.gs.load()
        self.bs.load()
        self.cos.load()
        self.cls.load()
        self.ns.load()
        self.music = base.loader.loadMusic('phase_3/audio/bgm/create_a_toon.ogg')
        self.musicVolume = base.config.GetFloat('makeatoon-music-volume', 1)
        self.sfxVolume = base.config.GetFloat('makeatoon-sfx-volume', 1)
        self.soundBack = base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_back.ogg')
        self.crashSounds = []
        self.crashSounds.append(base.loader.loadSfx('phase_3/audio/sfx/tt_s_ara_mat_crash_boing.ogg'))
        self.crashSounds.append(base.loader.loadSfx('phase_3/audio/sfx/tt_s_ara_mat_crash_glassBoing.ogg'))
        self.crashSounds.append(base.loader.loadSfx('phase_3/audio/sfx/tt_s_ara_mat_crash_wood.ogg'))
        self.crashSounds.append(base.loader.loadSfx('phase_3/audio/sfx/tt_s_ara_mat_crash_woodBoing.ogg'))
        self.crashSounds.append(base.loader.loadSfx('phase_3/audio/sfx/tt_s_ara_mat_crash_woodGlass.ogg'))
        return

    def unload(self):
        self.exit()
        if self.toon:
            self.toon.stopBlink()
            self.toon.stopLookAroundNow()
        self.gs.unload()
        self.bs.unload()
        self.cos.unload()
        self.cls.unload()
        self.ns.unload()
        del self.gs
        del self.bs
        del self.cos
        del self.cls
        del self.ns
        self.guiTopBar.destroy()
        self.guiBottomBar.destroy()
        self.guiCancelButton.destroy()
        self.guiCheckButton.destroy()
        self.eee.destroy()
        self.guiNextButton.destroy()
        self.guiLastButton.destroy()
        self.rotateLeftButton.destroy()
        self.rotateRightButton.destroy()
        del self.guiTopBar
        del self.guiBottomBar
        del self.guiCancelButton
        del self.guiCheckButton
        del self.eee
        del self.guiNextButton
        del self.guiLastButton
        del self.rotateLeftButton
        del self.rotateRightButton
        del self.names
        del self.dnastring
        del self.nameList
        del self.music
        del self.soundBack
        del self.dna
        if self.toon:
            self.toon.delete()
        del self.toon
        self.room.removeNode()
        del self.room
        self.smoke.removeNode()
        del self.smoke
        while len(self.crashSounds):
            del self.crashSounds[0]

        self.parentFSM.getStateNamed('createAvatar').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        loader.unloadModel('phase_3/models/gui/create_a_toon_gui')
        loader.unloadModel('phase_3/models/gui/create_a_toon')
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def getDNA(self):
        return self.dnastring

    def __handleBodyShop(self):
        self.fsm.request('BodyShop')

    def __handleClothesShop(self):
        self.fsm.request('ClothesShop')

    def __handleColorShop(self):
        self.fsm.request('ColorShop')

    def __handleNameShop(self):
        self.fsm.request('NameShop')

    def __handleCancel(self):
        self.doneStatus = 'cancel'
        self.shopsVisited = []
        base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))

    def toggleSlide(self):
        self.slide = 1 - self.slide

    def goToNextShop(self):
        self.progressing = 1
        if self.shop == GENDERSHOP:
            self.fsm.request('BodyShop')
        elif self.shop == BODYSHOP:
            self.fsm.request('ColorShop')
        elif self.shop == COLORSHOP:
            self.fsm.request('ClothesShop')
        else:
            self.fsm.request('NameShop')

    def goToLastShop(self):
        self.progressing = 0
        if self.shop == BODYSHOP:
            self.fsm.request('GenderShop')
        elif self.shop == COLORSHOP:
            self.fsm.request('BodyShop')
        elif self.shop == CLOTHESSHOP:
            self.fsm.request('ColorShop')
        else:
            self.fsm.request('ClothesShop')

    def charSez(self, char, statement, dialogue = None):
        import pdb
        pdb.set_trace()
        char.setChatAbsolute(statement, CFSpeech, dialogue)

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterGenderShop(self):
        self.shop = GENDERSHOP
        if GENDERSHOP not in self.shopsVisited:
            self.shopsVisited.append(GENDERSHOP)
            self.guiNextButton['state'] = DGG.DISABLED
        self.guiTopBar['text'] = TTLocalizer.CreateYourToonTitle
        self.guiTopBar['text_fg'] = (1, 0.92, 0.2, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterGenderShop
        base.transitions.fadeIn()
        self.accept('GenderShop-done', self.__handleGenderShopDone)
        self.gs.enter()
        self.guiNextButton.show()
        self.gs.showButtons()
        self.rotateLeftButton.hide()
        self.rotateRightButton.hide()

    def exitGenderShop(self):
        self.gs.exit()
        self.ignore('GenderShop-done')

    def __handleGenderShopDone(self):
        self.guiNextButton.hide()
        self.gs.hideButtons()
        self.goToNextShop()

    def bodyShopOpening(self):
        self.bs.showButtons()
        self.guiNextButton.show()
        if not self.isRewriteSession:
            self.guiLastButton.show()
        self.rotateLeftButton.show()
        self.rotateRightButton.show()

    def enterBodyShop(self):
        self.toon.show()
        self.shop = BODYSHOP
        self.guiTopBar['text'] = TTLocalizer.ShapeYourToonTitle
        self.guiTopBar['text_fg'] = (0.0, 0.98, 0.5, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterBodyShop
        self.accept('BodyShop-done', self.__handleBodyShopDone)
        self.bs.enter(self.toon, self.shopsVisited)
        if BODYSHOP not in self.shopsVisited:
            self.shopsVisited.append(BODYSHOP)
        self.bodyShopOpening()

    def exitBodyShop(self):
        self.bs.exit()
        self.ignore('BodyShop-done')

    def __handleBodyShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.bs.doneStatus == 'next':
            self.bs.hideButtons()
            self.goToNextShop()
        else:
            self.bs.hideButtons()
            self.goToLastShop()

    def colorShopOpening(self):
        self.cos.showButtons()
        if not self.isRewriteSession:
            self.guiNextButton.show()
        self.guiLastButton.show()
        self.rotateLeftButton.show()
        self.rotateRightButton.show()

    def enterColorShop(self):
        self.shop = COLORSHOP
        self.guiTopBar['text'] = TTLocalizer.PaintYourToonTitle
        self.guiTopBar['text_fg'] = (0, 1, 1, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterColorShop
        self.accept('ColorShop-done', self.__handleColorShopDone)
        self.colorShopOpening()
        if self.isRewriteSession:
            self.guiNextButton.hide()
            self.guiCheckButton.show()
        self.cos.enter(self.toon, self.shopsVisited, self.isRewriteSession)
        if COLORSHOP not in self.shopsVisited:
            self.shopsVisited.append(COLORSHOP)

    def exitColorShop(self):
        self.cos.exit()
        self.ignore('ColorShop-done')

    def __handleColorShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.cos.doneStatus == 'next':
            if self.isRewriteSession:
                self.doneStatus = 'created'
                base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))
                return
            self.cos.hideButtons()
            self.goToNextShop()
        else:
            self.cos.hideButtons()
            self.goToLastShop()

    def clothesShopOpening(self):
        self.guiNextButton.show()
        self.guiLastButton.show()
        self.cls.showButtons()
        self.rotateLeftButton.show()
        self.rotateRightButton.show()

    def enterClothesShop(self):
        self.shop = CLOTHESSHOP
        self.guiTopBar['text'] = TTLocalizer.PickClothesTitle
        self.guiTopBar['text_fg'] = (1, 0.92, 0.2, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterClothesShop
        self.accept('ClothesShop-done', self.__handleClothesShopDone)
        self.toon.setScale(self.toonScale)
        self.toon.setPos(self.toonPosition)
        if not self.progressing:
            self.toon.setHpr(self.toonHpr)
        self.clothesShopOpening()
        self.cls.enter(self.toon)
        if CLOTHESSHOP not in self.shopsVisited:
            self.shopsVisited.append(CLOTHESSHOP)

    def exitClothesShop(self):
        self.cls.exit()
        self.ignore('ClothesShop-done')

    def __handleClothesShopDone(self):
        self.guiNextButton.hide()
        self.guiLastButton.hide()
        if self.cls.doneStatus == 'next':
            self.cls.hideButtons()
            self.goToNextShop()
        else:
            self.cls.hideButtons()
            self.goToLastShop()

    def nameShopOpening(self, task):
        self.guiCheckButton.show()
        self.guiLastButton.show()
        if self.warp:
            self.guiLastButton.hide()
        if NAMESHOP not in self.shopsVisited:
            self.shopsVisited.append(NAMESHOP)
        return Task.done

    def enterNameShop(self):
        self.shop = NAMESHOP
        self.guiTopBar['text'] = TTLocalizer.NameToonTitle
        self.guiTopBar['text_fg'] = (0.0, 0.98, 0.5, 1)
        self.guiTopBar['text_scale'] = TTLocalizer.MATenterNameShop
        self.accept('NameShop-done', self.__handleNameShopDone)
        self.rotateLeftButton.hide()
        self.rotateRightButton.hide()
        self.toon.setPos(self.nameShopToonPosition)
        self.toon.setHpr(self.toonHpr)
        if self.progressing:
            waittime = self.leftTime
        else:
            waittime = 0.2
        self.ns.enter(self.toon, self.nameList, self.warp)
        taskMgr.doMethodLater(waittime, self.nameShopOpening, 'nameShopOpeningTask')

    def exitNameShop(self):
        self.ns.exit()
        self.ignore('NameShop-done')
        taskMgr.remove('nameShopOpeningTask')

    def rejectName(self):
        self.ns.rejectName(TTLocalizer.RejectNameText)

    def __handleNameShopDone(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: MAKEATOON: Creating A Toon')
        self.guiLastButton.hide()
        self.guiCheckButton.hide()
        if self.ns.getDoneStatus() == 'last':
            self.ns.hideAll()
            self.goToLastShop()
        elif self.ns.getDoneStatus() == 'paynow':
            self.doneStatus = 'paynow'
            base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))
        else:
            self.doneStatus = 'created'
            base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent))

    def __handleNext(self):
        messenger.send('next')

    def __handleLast(self):
        messenger.send('last')

    def __handleSkipTutorial(self):
        messenger.send('skipTutorial')

    def enterDone(self):
        pass

    def exitDone(self):
        pass

    def create3DGui(self):
        self.proto = loader.loadModel('phase_3/models/makeatoon/tt_m_ara_mat_protoMachine')
        self.proto.setScale(0.2)
        self.proto.reparentTo(render)

    def setup3DPicker(self):
        self.accept('mouse1', self.mouseDown)
        self.accept('mouse1-up', self.mouseUp)
        self.pickerQueue = CollisionHandlerQueue()
        self.pickerTrav = CollisionTraverser('MousePickerTraverser')
        self.pickerTrav.setRespectPrevTransform(True)
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerTrav.addCollider(self.pickerNP, self.pickerQueue)

    def mouseDown(self):
        self.notify.debug('Mouse 1 Down')
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        self.pickerTrav.traverse(render)
        if self.pickerQueue.getNumEntries() > 0:
            self.pickerQueue.sortEntries()
            self.pickedObj = self.pickerQueue.getEntry(0).getIntoNodePath()

    def mouseUp(self):
        self.notify.debug('Mouse 1 Up')

    def setToon(self, toon):
        self.toon = toon

    def setNextButtonState(self, state):
        self.guiNextButton['state'] = state

    def playRandomCrashSound(self):
        index = random.randint(0, len(self.crashSounds) - 1)
        base.playSfx(self.crashSounds[index], volume=self.sfxVolume)

    def rotateToonLeft(self, event):
        taskMgr.add(self.rotateToonLeftTask, 'rotateToonLeftTask')

    def rotateToonLeftTask(self, task):
        self.toon.setH(self.toon.getH() + self.hprDelta)
        return task.cont

    def stopToonRotateLeftTask(self, event):
        taskMgr.remove('rotateToonLeftTask')

    def rotateToonRight(self, event):
        taskMgr.add(self.rotateToonRightTask, 'rotateToonRightTask')

    def rotateToonRightTask(self, task):
        self.toon.setH(self.toon.getH() - self.hprDelta)
        return task.cont

    def stopToonRotateRightTask(self, event):
        taskMgr.remove('rotateToonRightTask')
