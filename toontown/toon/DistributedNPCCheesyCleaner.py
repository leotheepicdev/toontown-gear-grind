from .DistributedNPCToonBase import *
from . import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from lib.libotp._constants import CFSpeech, CFTimeout

class DistributedNPCCheesyCleaner(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.dialog = None

    def disable(self):
        self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('stopped')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetCheesyCleaner(self):
        self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None          
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            base.localAvatar.resetHeight()
            self.freeAvatar()

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return
        if mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetCheesyCleaner()
        elif mode == NPCToons.PURCHASE_MOVIE_NO_MONEY:
            self.setChatAbsolute(TTLocalizer.CHEESY_CLEANER_NO_EFFECT, CFSpeech | CFTimeout)
            self.resetCheesyCleaner()
        elif mode == NPCToons.PURCHASE_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            self.setChatAbsolute(TTLocalizer.CHEESY_CLEANER_GREETING, CFSpeech | CFTimeout)
            if self.isLocalToon:
                self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=TTLocalizer.CheesyEffectCleanerConfirmation, command=self.sendResponse)
                self.dialog.show()
        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.CHEESY_CLEANER_SUCCESS, CFSpeech | CFTimeout)
            self.resetCheesyCleaner()
        elif mode == NPCToons.PURCHASE_MOVIE_AVATAR_REJECT:
            self.setChatAbsolute(TTLocalizer.CHEESY_CLEANER_AV_SAID_NO, CFSpeech | CFTimeout)
            self.resetCheesyCleaner()
            
    def sendResponse(self, response):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        self.sendUpdate('receiveResponse', [response])