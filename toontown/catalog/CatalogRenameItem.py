from direct.gui.DirectGui import DirectLabel
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpgui.OTPDialog import YesNo, Acknowledge
from . import CatalogItem

class CatalogRenameItem(CatalogItem.CatalogItem):

    def getPurchaseLimit(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.RenameTypeName

    def getName(self):
        return TTLocalizer.RenameTypeName
        
    def getDisplayName(self):
        return TTLocalizer.RenameTypeDesc

    def getPicture(self, av):
        frame = self.makeFrame()
        fontIndex = av.getNametagStyle()
        if fontIndex == 100:
            font = ToontownGlobals.getToonFont()
        else:
            font = ToontownGlobals.getNametagFont(av.getNametagStyle())
        label = DirectLabel(parent=frame, relief=None, pos=(0, 0, 0.24), scale=0.5, text=av.getName(), text_fg=(1.0, 1.0, 1.0, 1.0), text_shadow=(0.0, 0.0, 0.0, 1.0), text_font=font, text_wordwrap=9)
        self.hasPicture = True
        return (frame, None)
        
    def output(self, store = -1):
        return 'CatalogRenameItem()'

    def reachedPurchaseLimit(self, avatar):
        if avatar.onOrder.count(self) != 0:
            return 1
        if avatar.onGiftOrder.count(self) != 0:
            return 1
        if avatar.mailboxContents.count(self) != 0:
            return 1
        if self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        if avatar.getWishNameState() != '':
            return 2
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
        message = TTLocalizer.MessageConfirmRename
        dialogClass = ToontownGlobals.getDialogClass()
        self.dialog = dialogClass(text=message, dialogName='acceptItem', command=self.handleRenameChoice, style=YesNo)
        self.dialog.show()

    def handleRenameChoice(self, status):
        self.dialog.cleanup()
        if status == 1:
            message = TTLocalizer.MessageRenameConfirmed
            dialogClass = ToontownGlobals.getDialogClass()
            self.dialog = dialogClass(text=message, dialogName='renameAccepted', command=self.handleTutorialDone, style=Acknowledge)
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
        avatar.b_WishNameState('OPEN')
        return ToontownGlobals.P_ItemAvailable