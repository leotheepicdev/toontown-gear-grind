from panda3d.core import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toonbase.ToontownGlobals import *
from .SuitBattleGlobals import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui import OnscreenText

class PlayByPlayText(OnscreenText.OnscreenText):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayByPlayText')

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, pos=(0.0, 0.75), scale=TTLocalizer.PBPTonscreenText, fg=(1, 0, 0, 1), font=getSignFont(), wordwrap=13)

    def getShowInterval(self, text, duration):
        return Sequence(Func(self.hide), Wait(duration * 0.3), Func(self.setText, text), Func(self.setColorScale, (1, 1, 1, 0)), Func(self.show), 
                        LerpColorScaleInterval(self, .1, (1, 1, 1, 1)), Wait(duration * 0.7), LerpColorScaleInterval(self, .1, (1, 1, 1, 0)), Func(self.hide))

    def getToonsDiedInterval(self, textList, duration):
        track = Sequence(Func(self.hide), Wait(duration * 0.3))
        waitGap = 0.6 / len(textList) * duration
        for text in textList:
            newList = [Func(self.setText, text),
             Func(self.show),
             Wait(waitGap),
             Func(self.hide)]
            track += newList

        track.append(Wait(duration * 0.1))
        return track

class PlayByPlayTextRounds(OnscreenText.OnscreenText):

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, scale=TTLocalizer.PBPTRonscreenText, fg=(1, 0.5, 0, 1), font=getSignFont(), wordwrap=13)
        
    def changePos(self, pos):
        self['pos'] = pos

    def getShowInterval(self, text, pos, duration):
        return Sequence(Func(self.hide), Wait(duration * 0.3), Func(self.setText, text), Func(self.changePos, pos), Func(self.setColorScale, (1, 1, 1, 0)), Func(self.show), 
                        LerpColorScaleInterval(self, .1, (1, 1, 1, 1)), Wait(duration * 0.7), LerpColorScaleInterval(self, .1, (1, 1, 1, 0)), Func(self.hide))
                        
class PlayByPlayTextDesc(OnscreenText.OnscreenText):

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, scale=TTLocalizer.PBPTRonscreenText, fg=(1, 0.5, 0, 1), font=getSignFont(), wordwrap=13)
        
    def changePos(self, pos):
        self['pos'] = pos

    def getShowInterval(self, text, pos, duration):
        return Sequence(Func(self.hide), Wait(duration * 0.3), Func(self.setText, text), Func(self.changePos, pos), Func(self.setColorScale, (1, 1, 1, 0)), Func(self.show), 
                        LerpColorScaleInterval(self, .1, (1, 1, 1, 1)), Wait(duration * 0.7), LerpColorScaleInterval(self, .1, (1, 1, 1, 0)), Func(self.hide))