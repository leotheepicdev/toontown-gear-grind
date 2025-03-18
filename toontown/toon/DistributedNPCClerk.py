from panda3d.core import Vec3
from lib.libotp._constants import CFSpeech, CFTimeout
from toontown.minigame import ClerkPurchase
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import NPCToons
from .DistributedNPCToonBase import DistributedNPCToonBase
import time

class DistributedNPCClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchaseGui = None

    def disable(self):
        self.resetClerk()
        DistributedNPCToonBase.disable(self)

    def resetClerk(self):
        self.ignoreAll()
        self.clearChat()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))

        if self.purchaseGui:
            if self.purchaseGui.timer:
                self.purchaseGui.timer.stop()
                self.purchaseGui.timer.destroy()
            self.purchaseGui.exit()
            self.purchaseGui.unload()
            self.purchaseGui = None
            
    def setMovie(self, mode):
        if mode == 0:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
        elif mode == 1:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING, CFSpeech | CFTimeout)
            return
        elif mode == 2:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)

        self.initToonState()
    
    def freeAvatar(self):
        base.localAvatar.posCamera(0, 0)
        base.cr.playGame.getPlace().fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        if not base.localAvatar.getMoney():
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NEEDJELLYBEANS, CFSpeech | CFTimeout)
            return
        
        self.setMovie(1)
        base.cr.playGame.getPlace().fsm.request('purchase')
        camera.wrtReparentTo(render)
        camera.posQuatInterval(1, Vec3(-5, 9, self.getHeight() - 0.5), Vec3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera')).start()
        taskMgr.doMethodLater(1.0, self.popupPurchaseGUI, self.uniqueName('popupPurchaseGUI'))
   
    def popupPurchaseGUI(self, task):
        self.clearChat()
        self.acceptOnce('purchaseClerkDone', self.__handlePurchaseDone)
        self.purchaseGui = ClerkPurchase.ClerkPurchase(base.localAvatar, NPCToons.CLERK_COUNTDOWN_TIME, 'purchaseClerkDone')
        self.purchaseGui.load()
        self.purchaseGui.enter()

    def __handlePurchaseDone(self, mode):
        self.sendUpdate('setInventory', [base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney()])
        self.resetClerk()
        self.freeAvatar()
        self.detectAvatars()
        self.setMovie(mode)