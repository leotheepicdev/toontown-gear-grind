from panda3d.core import *
from .DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from panda3d.core import *
from . import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.fishing import FishSellGUI
from direct.task.Task import Task
from lib.libotp._constants import CFSpeech, CFTimeout

class DistributedNPCFisherman(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.fishGui = None
        return

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupFishGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.fishGui:
            self.fishGui.destroy()
            self.fishGui = None
        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)
        return

    def generate(self):
        DistributedNPCToonBase.generate(self)
        self.fishGuiDoneEvent = 'fishGuiDone'

    def announceGenerate(self):
        DistributedNPCToonBase.announceGenerate(self)

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        npcOrigin = self.cr.playGame.hood.loader.geom.find('**/npc_fisherman_origin_%s;+s' % self.posIndex)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning('announceGenerate: Could not find npc_fisherman_origin_' + str(self.posIndex))
        return

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        return

    def setupAvatars(self, av):
        self.ignoreAvatars()
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def resetFisherman(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupFishGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.fishGui:
            self.fishGui.destroy()
            self.fishGui = None
        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.SELL_MOVIE_CLEAR:
            return
        if mode == NPCToons.SELL_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignore(self.fishGuiDoneEvent)
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)
                if self.fishGui:
                    self.fishGui.destroy()
                    self.fishGui = None
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                quat = Quat()
                quat.setHpr((-150, -2, 0))
                camera.posQuatInterval(1, Point3(-5, 9, base.localAvatar.getHeight() - 0.5), quat, other=self, blendType='easeOut', name=self.uniqueName('lerpCamera')).start()
            if self.isLocalToon:
                taskMgr.doMethodLater(1.0, self.popupFishGUI, self.uniqueName('popupFishGUI'))
        elif mode == NPCToons.SELL_MOVIE_COMPLETE:
            chatStr = TTLocalizer.STOREOWNER_THANKSFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_TROPHY:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TROPHY % (numFish, totalNumFish), CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_TROPHY_BUCKET:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TROPHY_BUCKET % (numFish, totalNumFish), CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_NOFISH:
            if hasattr(base.cr, 'newsManager'):
                d_genus, d_species = base.cr.newsManager.getDailyCatch()
                if d_genus != -1:
                    chatStr = TTLocalizer.STOREOWNER_NOFISH_DAILY_CATCH % TTLocalizer.FishSpeciesNames[d_genus][d_species]
                else:
                    chatStr = TTLocalizer.STOREOWNER_NOFISH
            else:
                chatStr = TTLocalizer.STOREOWNER_NOFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_NO_MONEY:
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetFisherman()
        return

    def __handleSaleDone(self, sell):
        self.ignore(self.fishGuiDoneEvent)
        self.sendUpdate('completeSale', [sell])
        self.fishGui.destroy()
        self.fishGui = None
        return

    def popupFishGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.fishGuiDoneEvent, self.__handleSaleDone)
        self.fishGui = FishSellGUI.FishSellGUI(self.fishGuiDoneEvent)
