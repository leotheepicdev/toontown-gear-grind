from panda3d.core import FrameRateMeter
from toontown.toonbase import ToontownGlobals
import random

class TTFrameRateMeter(FrameRateMeter):
    TEXT_COLORS2FPS = [(1, 1, 1, 1), #White
                   (1, 0, 0, 1), #Red
                   (1, 0.5, 0, 1), #Orange
                   (0, 0, 1, 1), #Blue
                   (0, 1, 0, 1)] #Green
    DELAY_TIME = 1.5

    def __init__(self, name):
        FrameRateMeter.__init__(self, name)
        self.lastTextColor = None
        self.setUpdateInterval(self.DELAY_TIME)
        self.setTextColor(self.TEXT_COLORS2FPS[0])
        self.setFont(ToontownGlobals.getSignFont())

    def update(self, task):
        FrameRateMeter.update(self)
        textColorChoice = random.choice(self.TEXT_COLORS2FPS)
        if textColorChoice != self.lastTextColor:
            self.setTextColor(textColorChoice)
            self.lastTextColor = textColorChoice
        del textColorChoice
        return task.again

    def setupWindow(self, win):
        FrameRateMeter.setupWindow(self, win)
        taskMgr.doMethodLater(self.DELAY_TIME, self.update, 'updateFpsTask')

    def clearWindow(self):
        taskMgr.remove('updateFpsTask')
        FrameRateMeter.clearWindow(self)