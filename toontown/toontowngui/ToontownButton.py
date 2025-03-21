"""This module contains the ToontownButton class.
"""

__all__ = ['ToontownButton']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from toontown.toontowngui.ToontownFrame import ToontownFrame

class ToontownButton(ToontownFrame):
    """
    ToontownButton(parent) - Create a DirectGuiWidget which responds
    to mouse clicks and execute a callback function if defined
    """
    def __init__(self, parent = None, **kw):
        # Inherits from ToontownFrame
        # A Toontown Frame can have:
        # - A background texture (pass in path to image, or Texture Card)
        # - A midground geometry item (pass in geometry)
        # - A foreground text Node (pass in text string or Onscreen Text)
        # For a direct button:
        # Each button has 4 states (ready, press, rollover, disabled)
        # The same image/geom/text can be used for all four states or each
        # state can have a different text/geom/image
        # State transitions happen automatically based upon mouse interaction
        # Responds to click event and calls command if None
        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',          PGButton,   None),
            ('numStates',       4,          None),
            ('state',           DGG.NORMAL, None),
            ('relief',          DGG.RAISED, None),
            ('invertedFrames',  (1,),       None),
            # Command to be called on button click
            ('command',         None,       None),
            ('extraArgs',       [],         None),
            # Which mouse buttons can be used to click the button
            ('commandButtons',  (DGG.LMB,),     self.setCommandButtons),
            # Whether the button continuously runs the command if pressed
            # The default repeat threshold is 0.01
            # The default delay multiplier is 0.5
            ('repeat',   False,      None),
            ('repeatThreshold', 0.01,       None),
            ('repeatDelay',     1.0,        None),
            ('repeatDecay',     0.5,        None),
            # Sounds to be used for button events
            ('rolloverSound',   DGG.getDefaultRolloverSound(), self.setRolloverSound),
            ('clickSound',      DGG.getDefaultClickSound(),    self.setClickSound),
            # Can only be specified at time of widget contruction
            # Do the text/graphics appear to move when the button is clicked
            ('pressEffect',     1,         DGG.INITOPT),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        ToontownFrame.__init__(self, parent, inherit=True)

        # If specifed, add scaling to the pressed state to make it
        # look like the button is moving when you press it.  We have
        # to set up the node first, before we call initialise options;
        # but we can't actually apply the scale until we have the
        # bounding volume (which happens during initialise options).
        pressEffectNP = None
        if self['pressEffect']:
            pressEffectNP = self.stateNodePath[1].attachNewNode('pressEffect', 1)
            self.stateNodePath[1] = pressEffectNP

        # Call option initialization functions
        self.initialiseoptions(ToontownButton)
        self.handleEnter()

        # Now apply the scale.
        if pressEffectNP:
            bounds = self.getBounds()
            centerX = (bounds[0] + bounds[1]) / 2
            centerY = (bounds[2] + bounds[3]) / 2

            # Make a matrix that scales about the point
            mat = Mat4.translateMat(-centerX, 0, -centerY) * \
                  Mat4.scaleMat(0.98) * \
                  Mat4.translateMat(centerX, 0, centerY)
            pressEffectNP.setMat(mat)

    def setCommandButtons(self):
        # Attach command function to specified buttons
        # Left mouse button
        if DGG.LMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.one())
            self.bind(DGG.B1CLICK, self.commandFunc)
            if self['repeat']:
                self.bind(DGG.B1PRESS, self.__repeat, extraArgs=[True])
                self.bind(DGG.B1RELEASE, self.__repeat, extraArgs=[False])
        else:
            if self['repeat']:
                self.unbind(DGG.B1PRESS)
                self.unbind(DGG.B1RELEASE)
            self.unbind(DGG.B1CLICK)
            self.guiItem.removeClickButton(MouseButton.one())
        # Middle mouse button
        if DGG.MMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.two())
            self.bind(DGG.B2CLICK, self.commandFunc)
            if self['repeat']:
                self.bind(DGG.B2PRESS, self.__repeat, extraArgs=[True])
                self.bind(DGG.B2RELEASE, self.__repeat, extraArgs=[False])
        else:
            if self['repeat']:
                self.unbind(DGG.B2PRESS)
                self.unbind(DGG.B2RELEASE)
            self.unbind(DGG.B2CLICK)
            self.guiItem.removeClickButton(MouseButton.two())
        # Right mouse button
        if DGG.RMB in self['commandButtons']:
            self.guiItem.addClickButton(MouseButton.three())
            self.bind(DGG.B3CLICK, self.commandFunc)
            if self['repeat']:
                self.bind(DGG.B3PRESS, self.__repeat, extraArgs=[True])
                self.bind(DGG.B3RELEASE, self.__repeat, extraArgs=[False])
        else:
            if self['repeat']:
                self.unbind(DGG.B3PRESS)
                self.unbind(DGG.B3RELEASE)
            self.unbind(DGG.B3CLICK)
            self.guiItem.removeClickButton(MouseButton.three())

    def commandFunc(self, event):
        if self['command']:
            # Pass any extra args to command
            self['command'](*self['extraArgs'])

    def __repeat(self, state, event):
        if state and not taskMgr.hasTaskNamed(self.uniqueName('__repeatFunc')):
            task = self.addTask(self.__repeatFunc, self.uniqueName('__repeatFunc'), extraArgs=[event], appendTask=True)
            task.delayTime = self['repeatDelay']
            task.prevTime = 0.0
        elif not state:
            self.removeTask(self.uniqueName('__repeatFunc'))

    def __repeatFunc(self, event, task):
        if task.time - task.prevTime < task.delayTime:
            return task.cont
        else:
            self.commandFunc(event)
            task.delayTime = max(self['repeatThreshold'], task.delayTime * self['repeatDecay'])
            task.prevTime = task.time
            return task.cont

    def setClickSound(self):
        clickSound = self['clickSound']
        # Clear out sounds
        self.guiItem.clearSound(DGG.B1PRESS + self.guiId)
        self.guiItem.clearSound(DGG.B2PRESS + self.guiId)
        self.guiItem.clearSound(DGG.B3PRESS + self.guiId)
        if clickSound:
            if DGG.LMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B1PRESS + self.guiId, clickSound)
            if DGG.MMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B2PRESS + self.guiId, clickSound)
            if DGG.RMB in self['commandButtons']:
                self.guiItem.setSound(DGG.B3PRESS + self.guiId, clickSound)

    def setRolloverSound(self):
        rolloverSound = self['rolloverSound']
        if rolloverSound:
            self.guiItem.setSound(DGG.ENTER + self.guiId, rolloverSound)
        else:
            self.guiItem.clearSound(DGG.ENTER + self.guiId)
                
