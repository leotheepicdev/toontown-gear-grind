"""Contains the ToontownLabel class.
"""

__all__ = ['ToontownLabel']

from panda3d.core import *
from toontown.toontowngui.ToontownFrame import *

class ToontownLabel(ToontownFrame):
    """
    ToontownLabel(parent) - Create a DirectGuiWidget which has multiple
    states.  User explicitly chooses a state to display
    """
    def __init__(self, parent = None, **kw):
        # Inherits from ToontownFrame
        # A Toontown Frame can have:
        # - A background texture (pass in path to image, or Texture Card)
        # - A midground geometry item (pass in geometry)
        # - A foreground text Node (pass in text string or Onscreen Text)
        # For a direct label:
        # Each label has 1 or more states
        # The same image/geom/text can be used for all states or each
        # state can have a different text/geom/image
        # State transitions happen under user control

        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',          PGItem,    None),
            ('numStates',       1,         None),
            ('state',           self.inactiveInitState, None),
            ('activeState',     0,         self.setActiveState),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        ToontownFrame.__init__(self, parent, inherit=True)

        # Call option initialization functions
        self.initialiseoptions(ToontownLabel)
        self.handleEnter()

    def setActiveState(self):
        """ setActiveState - change label to specifed state """
        self.guiItem.setState(self['activeState'])
