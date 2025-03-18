from toontown.toon.DistributedNPCFisherman import *

class DistributedNPCLonelyLouis(DistributedNPCFisherman):

    def __init__(self, cr):
        DistributedNPCFisherman.__init__(self, cr)
        
    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

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
            self.setChatAbsolute(TTLocalizer.LONELY_LOUIS_TOOKTOOLONG, CFSpeech | CFTimeout)
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
            chatStr = TTLocalizer.LONELY_LOUIS_THANKSFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_TROPHY:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.LONELY_LOUIS_TROPHY % (numFish, totalNumFish), CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_TROPHY_BUCKET:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.LONELY_LOUIS_TROPHY_BUCKET % (numFish, totalNumFish), CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_NOFISH:
            chatStr = TTLocalizer.LONELY_LOUIS_NOFISH
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetFisherman()
        elif mode == NPCToons.SELL_MOVIE_NO_MONEY:
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetFisherman()
