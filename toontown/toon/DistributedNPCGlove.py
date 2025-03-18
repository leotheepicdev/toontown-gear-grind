from panda3d.core import *
from .DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from panda3d.core import *
from . import NPCToons
from direct.task.Task import Task
from . import GlovesGUI
from toontown.toonbase import TTLocalizer
from lib.libotp._constants import CFSpeech, CFTimeout

class DistributedNPCGlove(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.glovesGUI = None
        self.av = None
        self.browsing = 0
        self.button = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.glovesGUI:
            self.glovesGUI.exit()
            self.glovesGUI.unload()
            self.glovesGUI = None
            self.counter.show()
            del self.counter
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetShop(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.glovesGUI:
            self.glovesGUI.hideButtons()
            self.glovesGUI.exit()
            self.glovesGUI.unload()
            self.glovesGUI = None
            self.counter.show()
            del self.counter
            self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        self.av = None
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return
        if mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignore(self.purchaseDoneEvent)
                self.ignore(self.swapEvent)
            if self.glovesGUI:
                self.glovesGUI.resetGloves()
                self.__handlePurchaseDone(timeout=1)
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetShop()
        elif mode == NPCToons.PURCHASE_MOVIE_START or mode == NPCToons.PURCHASE_MOVIE_START_BROWSE:
            if mode == NPCToons.PURCHASE_MOVIE_START:
                self.browsing = 0
            elif mode == NPCToons.PURCHASE_MOVIE_START_BROWSE:
                self.browsing = 1
            elif mode == NPCToons.PURCHASE_MOVIE_START_NOROOM:
                self.browsing = 0
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            style = self.av.getStyle()
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                LerpPosQuatInterval(camera, 1, Point3(-5, 9, self.getHeight() - 0.5), Point3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera')).start()
            if self.browsing == 0:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING, CFSpeech | CFTimeout)
            else:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_BROWSING_GLOVES, CFSpeech | CFTimeout)
            if self.isLocalToon:
                taskMgr.doMethodLater(3.0, self.popupPurchaseGUI, self.uniqueName('popupPurchaseGUI'))
        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
            self.resetShop()
        elif mode == NPCToons.PURCHASE_MOVIE_NO_MONEY:
            self.notify.warning('PURCHASE_MOVIE_NO_MONEY should not be called')
            self.resetShop()

    def popupPurchaseGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.purchaseDoneEvent = 'purchaseDone'
        self.swapEvent = 'swap'
        self.acceptOnce(self.purchaseDoneEvent, self.__handlePurchaseDone)
        self.glovesGUI = GlovesGUI.GlovesGUI(self.purchaseDoneEvent, self.swapEvent, self.browsing)
        self.glovesGUI.load()
        self.glovesGUI.enter(self.av)
        self.glovesGUI.showButtons()
        camera.setPosHpr(base.localAvatar, -4.16, 8.25, 2.47, -152.89, 0.0, 0.0)
        self.counter = render.find('**/*mo1_TI_counter')
        self.counter.hide()
        self.hide()
        return Task.done

    def __handlePurchaseDone(self, timeout = 0):
        if self.glovesGUI.doneStatus == 'last' or timeout == 1:
            self.sendUpdate('requestClearMovie')
        else:
            self.d_setDNA(self.av.getStyle().makeNetString())

    def d_setDNA(self, dnaString):
        self.sendUpdate('setDNA', [dnaString])
