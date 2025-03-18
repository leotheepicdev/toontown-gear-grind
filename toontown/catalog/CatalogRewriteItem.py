from panda3d.core import Texture
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpgui.OTPDialog import YesNo, Acknowledge
from . import CatalogItem

class CatalogRewriteItem(CatalogItem.CatalogItem):

    def getPurchaseLimit(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.RewriteTypeName

    def getName(self):
        return TTLocalizer.RewriteTypeName
        
    def getDisplayName(self):
        return TTLocalizer.RewriteTypeDesc

    def getPicture(self, avatar):
        frame = self.makeFrame()
        model = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        sample = model.find('**/big_book')
        sample.setScale(2)
        sample.setTransparency(True)
        sample.setTexture(self.loadTexture(), 1)
        sample.setColorScale(base.localAvatar.style.getHeadColor())
        sample.reparentTo(frame)
        self.hasPicture = True
        return (frame, None)

    def loadTexture(self):
        texture = loader.loadTexture('phase_6/maps/Kartmenu_paintbucket.jpg', 'phase_6/maps/Kartmenu_paintbucket_a.rgb')
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture
        
    def output(self, store = -1):
        return 'CatalogRewriteItem()'
        
    def reachedPurchaseLimit(self, avatar):
        if avatar.onOrder.count(self) != 0:
            return 1
        if avatar.onGiftOrder.count(self) != 0:
            return 1
        if avatar.mailboxContents.count(self) != 0:
            return 1
        if self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        if avatar.getAllowedRewrite():
            return 1
        return 0
        
    def getBasePrice(self):
        return 10000

    def getDeliveryTime(self):
        return 1

    def isGift(self):
        return False

    def getDaysToGo(self, avatar):
        return 0

    def loyaltyRequirement(self):
        return 0

    def acceptItem(self, mailbox, index, callback):
        self.mailbox = mailbox
        self.index = index
        self.callback = callback
        message = TTLocalizer.MessageConfirmRewrite
        dialogClass = ToontownGlobals.getDialogClass()
        self.dialog = dialogClass(text=message, dialogName='acceptItem', command=self.handleRewriteChoice, style=YesNo)
        self.dialog.show()

    def handleRewriteChoice(self, status):
        self.dialog.cleanup()
        if status == 1:
            message = TTLocalizer.MessageRewriteConfirmed
            dialogClass = ToontownGlobals.getDialogClass()
            self.dialog = dialogClass(text=message, dialogName='rewriteAccepted', command=self.handleTutorialDone, style=Acknowledge)
            self.dialog.show()
        else:
            self.callback(ToontownGlobals.P_UserCancelled, None, self.index)

    def handleTutorialDone(self, status):
        self.dialog.cleanup()
        del self.dialog
        self.mailbox.acceptItem(self, self.index, self.callback)
        del self.mailbox
        del self.callback

    def recordPurchase(self, avatar, optional):
        avatar.b_setAllowedRewrite(1)
        return ToontownGlobals.P_ItemAvailable