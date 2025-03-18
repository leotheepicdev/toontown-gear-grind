from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from . import FishBase
from . import FishGlobals
from . import FishPhoto

class DailyCatchPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('DailyCatchPanel')

    def __init__(self):
        fishingGui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        albumGui = fishingGui.find('**/photo_frame1').copyTo(hidden)
        albumGui.find('**/picture_frame').setPos(-9.3, 0, 0)
        albumGui.find('**/picture_frame').reparentTo(albumGui, -1)
        albumGui.find('**/arrows').removeNode()
        optiondefs = (('relief', None, None),
         ('state', DGG.NORMAL, None),
         ('image', albumGui, None),
         ('image_scale', (0.025, 0.025, 0.025), None),
         ('image_pos', (0.23, 1, 0.12), None),
         ('text', TTLocalizer.UnknownDailyCatch, None),
         ('text_scale', 0.045, None),
         ('text_fg', (0.2, 0.1, 0.0, 1), None),
         ('text_pos', (0, -0.35), None),
         ('text_font', ToontownGlobals.getInterfaceFont(), None),
         ('text_wordwrap', 13.5, None),
         ('text_align', TextNode.ACenter, None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self)
        self.initialiseoptions(DailyCatchPanel)
        self.fishPanel = None
        self.genus = None
        self.jellybeanBoost = None
        self.setScale(1.3)
        albumGui.removeNode()

    def destroy(self):
        DirectFrame.destroy(self)
        self.destroyFishPanel()
        if self.jellybeanBoost:
            self.jellybeanBoost.destroy()
            self.jellybeanBoost = None

    def load(self):
        self.jellybeanBoost = DirectLabel(parent=self,
            relief = None,
            text = TTLocalizer.WorthDoubleBeans,
            text_fg = (1, 0, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_pos = (0, -0.215),
            text_scale = 0.045)
        
    def destroyFishPanel(self):
        if self.fishPanel:
            self.fishPanel.destroy()
            self.fishPanel = None

    def setGenus(self, genus):
        if self.genus == genus:
            return
        self.genus = genus
        if self.genus != None:
            f = FishBase.FishBase(self.genus, 0, 0)
            self.destroyFishPanel()
            self.fishPanel = FishPhoto.FishPhoto(fish=f, parent=self)
            self.fishPanel.setPos(0, 1, 0.12)
            self.fishPanel.setSwimBounds(-0.2461, 0.2367, -0.207, 0.2664)
            self.fishPanel.setSwimColor(0.47, 1.0, 0.99, 1.0)
            self.fishPanel.show()

    def show(self):
        self.update()
        DirectFrame.show(self)
        if self.fishPanel:
            self.fishPanel.show()
        if self.jellybeanBoost:
            self.jellybeanBoost.show()

    def hide(self):
        DirectFrame.hide(self)
        if self.fishPanel:
            self.fishPanel.hide()
        if self.jellybeanBoost:
            self.jellybeanBoost.hide()

    def update(self):
        genus, species = base.cr.newsManager.getDailyCatch()
    
        if genus == -1:
            self['text'] = TTLocalizer.UnknownDailyCatch
            self.destroyFishPanel()
        else:
            self['text'] = TTLocalizer.KnownDailyCatch % TTLocalizer.FishSpeciesNames[genus][species]
            self.setGenus(genus)
