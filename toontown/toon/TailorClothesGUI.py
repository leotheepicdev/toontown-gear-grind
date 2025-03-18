from toontown.makeatoon.ClothesGUI import *
from toontown.toonbase import ToontownGlobals
from . import ToonDNA

class TailorClothesGUI(ClothesGUI):
    notify = directNotify.newCategory('MakeClothesGUI')

    def __init__(self, doneEvent, swapEvent, tailorId):
        ClothesGUI.__init__(self, CLOTHES_TAILOR, doneEvent, swapEvent)
        self.tailorId = tailorId

    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        gender = self.dna.getGender()
        if self.swapEvent != None:
            self.topStyles = ToonDNA.getTopStyles(gender, tailorId=self.tailorId)
            self.tops = ToonDNA.getTops(gender, tailorId=self.tailorId)
            self.bottomStyles = ToonDNA.getBottomStyles(gender, tailorId=self.tailorId)
            self.bottoms = ToonDNA.getBottoms(gender, tailorId=self.tailorId)
            self.gender = gender
            self.topChoice = -1
            self.topStyleChoice = -1
            self.topColorChoice = -1
            self.bottomChoice = -1
            self.bottomStyleChoice = -1            
            self.bottomColorChoice = -1
        self.setupButtons()
        self.tickets = DirectLabel(parent=base.a2dBottomRight, relief=None, pos=(-0.55, 0, 0.05), scale=0.08, text=TTLocalizer.ClothingTicketAmount % base.localAvatar.getClothingTickets(), 
                                   text_pos=(0.2, -0.2), text_font=ToontownGlobals.getSignFont(), text_fg=(1, 0.5, 0, 1))

    def unload(self):
        ClothesGUI.unload(self)
        self.tickets.destroy()
        del self.tickets
