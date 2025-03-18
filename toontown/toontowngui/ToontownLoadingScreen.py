from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *
import random

class ToontownLoadingScreen:

    def __init__(self):
        self.expectedCount = 0
        self.count = 0
        self.gui = OnscreenImage(parent=hidden, image='phase_3/maps/loading_bg.png')
        self.gui.setBin('gui-popup', 0)
        self.slogan = DirectLabel(guiId='ToontownLoadingSlogan', parent=hidden, relief=None, pos=(0, 0, -0.85), text='',
                                  text_font=ToontownGlobals.getMinnieFont(), textMayChange=1, text_scale=0.06, text_fg=(0.95, 0.95, 0.95, 1), text_shadow=(0, 0, 0, 0.2), text_align=TextNode.ACenter)
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=hidden, relief=None, pos=(0, 0, -0.35), text='',
                                 text_font=ToontownGlobals.getMinnieFont(), textMayChange=1, text_scale=0.08, text_fg=(0.98, 0.227, 0.01, 1), text_shadow=(0, 0, 0, 0.2), text_align=TextNode.ACenter)

        self.textBar = OnscreenImage(parent=hidden, image='phase_3/maps/loading_bar.png', scale=(render2d.getScale()[0], 0.25, 0.25), pos=(0, 0, -0.65))
        self.textBar.setTransparency(TransparencyAttrib.MAlpha)
        self.textBar.setBin('gui-popup', 1)
        
        
        self.didYouKnowTitle = DirectLabel(guiId='ToontownLoadingScreenTipTitle', parent=hidden, relief=None, pos=(0, 0, -0.575), text=TTLocalizer.DidYouKnowTitle,
                                 text_font=ToontownGlobals.getMinnieFont(), text_scale=0.08, text_fg=(0.95, 0.95, 0.95, 1), text_shadow=(0, 0, 0, 0.2), text_align=TextNode.ACenter)
        self.didYouKnow = DirectLabel(guiId='ToontownLoadingScreenTip', parent=hidden, relief=None, pos=(0, 0, -0.675), text='',
                                 text_font=ToontownGlobals.getInterfaceFont(), textMayChange=1, text_wordwrap=18, text_scale=0.06, text_fg=(0.95, 0.95, 0.95, 1), text_shadow=(0, 0, 0, 0.2), text_align=TextNode.ACenter)

        self.logo = OnscreenImage(parent=hidden, image='phase_3/maps/toontown-logo.png', scale=(0.703125, 1, 0.3515625), pos=(0, 0, -0.4))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)

    def destroy(self):
        self.slogan.destroy()
        self.title.destroy()
        self.didYouKnowTitle.destroy()
        self.didYouKnow.destroy()
        self.gui.removeNode()
        self.textBar.removeNode()
        self.logo.removeNode()

    def begin(self, range, label, gui, tipCategory):
        self.slogan['text'] = random.choice(TTLocalizer.LoadingScreenSlogans)
        self.title['text'] = label
        if tipCategory in [TTLocalizer.TIP_MINIGAME, TTLocalizer.TIP_KARTING, TTLocalizer.TIP_GOLF]:
            self.didYouKnow['text'] = random.choice(TTLocalizer.DidYouKnowDict[tipCategory])
        else:
            self.didYouKnow['text'] = random.choice(TTLocalizer.DidYouKnowDict[tipCategory] + TTLocalizer.TIP_ALL)
        self.__count = 0
        self.expectedCount = range
        if gui:
            self.slogan.reparentTo(base.a2dpTopCenter, NO_FADE_SORT_INDEX)
            if label != '':
                self.title.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.didYouKnowTitle.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.didYouKnow.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.gui.reparentTo(render2d, NO_FADE_SORT_INDEX)
            self.textBar.reparentTo(render2d, NO_FADE_SORT_INDEX)
            self.logo.reparentTo(base.a2dpTopCenter, NO_FADE_SORT_INDEX)
        else:
            self.slogan.reparentTo(base.a2dpTopCenter, NO_FADE_SORT_INDEX)
            self.title.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.didYouKnowTitle.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.didYouKnow.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.gui.reparentTo(hidden)
            self.textBar.reparentTo(hidden)
            self.logo.reparentTo(hidden)

    def end(self):
        self.slogan.reparentTo(hidden)
        self.title.reparentTo(hidden)
        self.didYouKnowTitle.reparentTo(hidden)
        self.didYouKnow.reparentTo(hidden)
        self.gui.reparentTo(hidden)
        self.textBar.reparentTo(hidden)
        self.logo.reparentTo(hidden)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.count = self.count + 1
        base.graphicsEngine.renderFrame()
