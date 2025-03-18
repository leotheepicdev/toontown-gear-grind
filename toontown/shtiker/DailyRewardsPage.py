from panda3d.core import *
from . import ShtikerPage
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class DailyRewardsPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.waitingForServerBox = None
        self.responseBox = None

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.DailyRewardsPageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        self.presents = loader.loadModel('phase_5.5/models/estate/tt_m_ara_int_presents')
        self.presents.reparentTo(self)
        self.presents.hide()
        self.presents.setPosHpr(-0.5, 0, -0.1, 0, 10, 0)
        self.presents.setScale(0.18)
        self.presents.setDepthTest(1)
        self.presents.setDepthWrite(1)
        self.claimDesc = DirectLabel(parent=self, relief=None, text=TTLocalizer.DailyRewardsClaimDescAvailable, text_scale=0.06, textMayChange=1, pos=(0.433, 0, 0.2))
        claimButtonGui = loader.loadModel('phase_3/models/gui/quit_button')
        self.claimButton = DirectButton(parent=self, relief=None, image=(claimButtonGui.find('**/QuitBtn_UP'),
         claimButtonGui.find('**/QuitBtn_DN'),
         claimButtonGui.find('**/QuitBtn_RLVR'),
         claimButtonGui.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=1.15, state=DGG.NORMAL, text=TTLocalizer.DailyRewardsClaimButton, 
         text_scale=TTLocalizer.OPCodesSubmitTextScale, text_align=TextNode.ACenter, text_pos=TTLocalizer.OPCodesSubmitTextPos, text3_fg=(0.5, 0.5, 0.5, 0.75),
         textMayChange=0, pos=(0.45, 0.0, -0.15))

    def unload(self):
        self.title.destroy()
        del self.title
        self.presents.removeNode()
        del self.presents
        self.claimDesc.destroy()
        del self.claimDesc
        self.claimButton.destroy()
        del self.claimButton
        if self.waitingForServerBox:
            self.waitingForServerBox.cleanup()
            self.waitingForServerBox = None
        if self.responseBox:
            self.responseBox.cleanup()
            self.responseBox = None
        ShtikerPage.ShtikerPage.unload(self)

    def updatePage(self):
        self.presents.show()

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.presents.hide()
        ShtikerPage.ShtikerPage.exit(self)
        
    def handleClaimButtonPressed(self):
        messenger.send('wakeup')
        
    def handleClaimButtonResponse(self, response):
        pass
