from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpgui.OTPDialog import YesNo
from . import CatalogItem

class CatalogSkipItem(CatalogItem.CatalogItem):

    def getPurchaseLimit(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.CatalogSkipTypeName

    def getName(self):
        return TTLocalizer.CatalogSkipTypeName
        
    def getDisplayName(self):
        return TTLocalizer.CatalogSkipTypeDesc

    def getPicture(self, avatar):
        gui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        cow = gui.find('**/clarabelleCow')
        cow.setScale(1.5)
        frame = self.makeFrame()
        cow.reparentTo(frame)
        gui.removeNode()
        return (frame, None)
        
    def output(self, store = -1):
        return 'CatalogSkipItem()'

    def reachedPurchaseLimit(self, avatar):
        if avatar.onOrder.count(self) != 0:
            return 1
        if avatar.onGiftOrder.count(self) != 0:
            return 1
        if avatar.mailboxContents.count(self) != 0:
            return 1
        if self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        return 0
        
    def getBasePrice(self):
        return 2500

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
        message = TTLocalizer.MessageConfirmCatalogSkip
        dialogClass = ToontownGlobals.getDialogClass()
        self.dialog = dialogClass(text=message, dialogName='acceptItem', command=self.handleCatalogSkipChoice, style=YesNo)
        self.dialog.show()

    def handleCatalogSkipChoice(self, status):
        self.dialog.cleanup()
        del self.dialog
        if status == 1:
            self.mailbox.acceptItem(self, self.index, self.callback)
            del self.mailbox
            del self.callback
        else:
            self.callback(ToontownGlobals.P_UserCancelled, None, self.index)

    def recordPurchase(self, avatar, optional):
        simbase.air.catalogManager.deliverCatalogFor(avatar)
        return ToontownGlobals.P_ItemAvailable
