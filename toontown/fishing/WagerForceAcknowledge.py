from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonDNA
from toontown.toon import ToonHead
from direct.gui.DirectGui import *

class WagerForceAcknowledge:

    def __init__(self, message, doneEvent):
        fadeModel = loader.loadModel('phase_3/models/misc/fade')
        if fadeModel:
            self.fade = DirectFrame(
                parent=aspect2dp,
                relief=None,
                image=fadeModel,
                image_color=(0, 0, 0, 0.4),
                image_scale=3.0,
                state=DGG.NORMAL)
            self.fade.reparentTo(render2d, FADE_SORT_INDEX)
            fadeModel.removeNode()
        else:
            print('Problem loading fadeModel.')
            self.fade = None
        self.dialog = TTDialog.TTGlobalDialog(
            message=message,
            doneEvent=doneEvent,
            style=TTDialog.YesNo,
            suppressKeys=True)
        self.dialog['text_pos'] = (-.26, 0.1)
        scale = self.dialog.component('image0').getScale()
        scale.setX(scale[0] * 1.3)
        self.dialog.component('image0').setScale(scale)
        
        
        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonRandom()
        self.head = ToonHead.ToonHead()
        self.head.setupHead(self.dna, forGui=1)
        self.head.reparentTo(self.dialog)
        self.head.setScale(0.17)
        self.head.setHpr(180, 0, 0)
        self.head.setPos(-0.48, 0, -0.035)
        
    def getDoneStatus(self):
        return self.dialog.doneStatus
        
    def show(self):
        self.dialog.show()

    def cleanup(self):
        if self.fade:
            self.fade.destroy()
        if self.head:
            self.head.delete()
            self.head = None
        self.dna = None
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
