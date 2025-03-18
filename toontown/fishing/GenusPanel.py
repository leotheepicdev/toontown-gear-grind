from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from . import FishBase
from . import FishGlobals
from . import FishPhoto

class GenusPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GenusPanel')

    def __init__(self, genus = None, itemIndex = 0, *extraArgs):
        fishingGui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        albumGui = fishingGui.find('**/photo_frame1').copyTo(hidden)
        albumGui.find('**/picture_frame').reparentTo(albumGui, -1)
        albumGui.find('**/arrows').removeNode()
        optiondefs = (('relief', None, None),
         ('state', DGG.NORMAL, None),
         ('image', albumGui, None),
         ('image_scale', (0.025, 0.025, 0.025), None),
         ('image_pos', (0, 1, 0), None),
         ('text', TTLocalizer.UnknownFish, None),
         ('text_scale', 0.065, None),
         ('text_fg', (0.2, 0.1, 0.0, 1), None),
         ('text_pos', (-0.5, -0.34), None),
         ('text_font', ToontownGlobals.getInterfaceFont(), None),
         ('text_wordwrap', 13.5, None),
         ('text_align', TextNode.ALeft, None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self)
        self.initialiseoptions(GenusPanel)
        self.fishPanel = None
        self.genus = None
        self.setGenus(int(genus))
        self.setScale(1.2)
        albumGui.removeNode()
        return

    def destroy(self):
        if self.fishPanel:
            self.fishPanel.destroy()
            del self.fishPanel
        DirectFrame.destroy(self)

    def load(self):
        pass

    def setGenus(self, genus):
        if self.genus == genus:
            return
        self.genus = genus
        if self.genus != None:
            if self.fishPanel:
                self.fishPanel.destroy()
            f = FishBase.FishBase(self.genus, 0, 0)
            self.fishPanel = FishPhoto.FishPhoto(fish=f, parent=self)
            self.fishPanel.setPos(-0.23, 1, -0.01)
            self.fishPanel.setSwimBounds(-0.2461, 0.2367, -0.207, 0.2664)
            self.fishPanel.setSwimColor(0.47, 1.0, 0.99, 1.0)
            speciesList = FishGlobals.getSpecies(self.genus)
            self.speciesLabels = []
            self.recordLabels = []
            offset = 0.085
            startPos = len(speciesList) / 2 * offset

            if not len(speciesList) % 2:
                startPos -= offset / 2
            for species in range(len(speciesList)):
                labelPos = startPos - species * offset
                recordPos = labelPos - 0.035
            
                label = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, pos=(0.06, 0, labelPos), text=TTLocalizer.UnknownFish, text_fg=(0.2, 0.1, 0.0, 1), text_scale=TTLocalizer.GPgenus, text_align=TextNode.ALeft, text_font=ToontownGlobals.getInterfaceFont())
                self.speciesLabels.append(label)
                recordLabel = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, pos=(0.06, 0, recordPos), text='', text_fg=(0.2, 0.1, 0.0, 1), text_scale=TTLocalizer.GPrecord, text_align=TextNode.ALeft, text_font=ToontownGlobals.getInterfaceFont())
                self.recordLabels.append(recordLabel)

    def show(self):
        self.update()
        DirectFrame.show(self)

    def hide(self):
        if self.fishPanel is not None:
            self.fishPanel.hide()
        DirectFrame.hide(self)
        return

    def update(self):
        if base.localAvatar.fishCollection.hasGenus(self.genus) and self.fishPanel is not None:
            self.fishPanel.show(showBackground=1)
            self['text'] = TTLocalizer.FishGenusNames[self.genus]
        for species in range(len(FishGlobals.getSpecies(self.genus))):
            genus, species, weight = base.localAvatar.fishCollection.hasFishGenusPanel(self.genus, species)
            if genus == None and species == None and weight == None:
                continue
            self.speciesLabels[species]['text'] = TTLocalizer.FishSpeciesNames[self.genus][species]
            
            conv = TTLocalizer.FishPageWeightConversion
            large = weight / conv
            if large == 1:
                largeStr = TTLocalizer.FishPageWeightLargeS % large
            else:
                largeStr = TTLocalizer.FishPageWeightLargeP % large
            small = weight % conv
            if small == 1:
                smallStr = TTLocalizer.FishPageWeightSmallS % small
            else:
                smallStr = TTLocalizer.FishPageWeightSmallP % small         
            
            self.recordLabels[species]['text'] = TTLocalizer.FishPageRecordStr + largeStr + smallStr
