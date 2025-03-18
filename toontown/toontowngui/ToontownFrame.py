"""A ToontownFrame is a basic ToontownGUI component that acts as the base
class for various other components, and can also serve as a basic
container to hold other ToontownGUI components.

A ToontownFrame can have:

* A background texture (pass in path to image, or Texture Card)
* A midground geometry item (pass in geometry)
* A foreground text Node (pass in text string or OnscreenText)

Each of these has 1 or more states.  The same object can be used for
all states or each state can have a different text/geom/image (for
radio button and check button indicators, for example).

See the :ref:`toontownframe` page in the programming manual for a more in-depth
explanation and an example of how to use this class.
"""

__all__ = ['ToontownFrame']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGuiBase import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenGeom import OnscreenGeom
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *


class ToontownFrame(DirectGuiWidget):
    DefDynGroups = ('text', 'geom', 'image')

    def __init__(self, parent=None, inherit=False, **kw):
        # Inherits from DirectGuiWidget
        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',          PGItem,     None),
            ('numStates',       1,          None),
            ('state',           self.inactiveInitState, None),
            # Frame can have:
            # A background texture
            ('image',           None,       self.setImage),
            # A midground geometry item
            ('geom',            None,       self.setGeom),
            # A foreground text node
            ('text',            None,       self.setText),
            # Change default value of text mayChange flag from 0
            # (OnscreenText.py) to 1
            ('textMayChange',  1,          None),
            ('enteranim', None, None),
            ('anim', None, None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs,
                           dynamicGroups=ToontownFrame.DefDynGroups)

        # Initialize superclasses
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(ToontownFrame)
        self.enterAnim = None
        self.b_anim = None
        if not inherit:
            self.handleEnter()

    def __reinitComponent(self, name, component_class, states, **kwargs):
        """Recreates the given component using the given keyword args."""
        assert name in ("geom", "image", "text")

        # constants should be local to or default arguments of constructors
        for c in range(self['numStates']):
            component_name = name + str(c)

            try:
                state = states[c]
            except IndexError:
                state = states[-1]

            if self.hascomponent(component_name):
                if state is None:
                    self.destroycomponent(component_name)
                else:
                    self[component_name + "_" + name] = state
            else:
                if state is None:
                    return

                kwargs[name] = state
                self.createcomponent(
                    component_name,
                    (),
                    name,
                    component_class,
                    (),
                    parent=self.stateNodePath[c],
                    **kwargs
                )
                
    def destroy(self):
        if self.enterAnim:
            self.enterAnim.pause()
            self.enterAnim.finish()
            self.enterAnim = None
        if self.b_anim:
            self.b_anim.pause()
            self.b_anim.finish()
            self.b_anim = None
        DirectGuiWidget.destroy(self)

    def clearText(self):
        self['text'] = None
        self.setText()

    def setText(self, text=None):
        if text is not None:
            self["text"] = text

        text = self["text"]
        if text is None or isinstance(text, str):
            text_list = (text,) * self['numStates']
        else:
            text_list = text

        self.__reinitComponent("text", OnscreenText, text_list,
            scale=1,
            mayChange=self['textMayChange'],
            sort=DGG.TEXT_SORT_INDEX)

    def clearGeom(self):
        self['geom'] = None
        self.setGeom()

    def setGeom(self, geom=None):
        if geom is not None:
            self["geom"] = geom

        geom = self["geom"]
        if geom is None or \
           isinstance(geom, NodePath) or \
           isinstance(geom, str):
            geom_list = (geom,) * self['numStates']
        else:
            geom_list = geom

        self.__reinitComponent("geom", OnscreenGeom, geom_list,
            scale=1,
            sort=DGG.GEOM_SORT_INDEX)

    def clearImage(self):
        self['image'] = None
        self.setImage()

    def setImage(self, image=None):
        if image is not None:
            self["image"] = image

        image = self["image"]
        if image is None or \
           isinstance(image, NodePath) or \
           isinstance(image, Texture) or \
           isinstance(image, str) or \
           isinstance(image, Filename) or \
           (len(image) == 2 and \
            isinstance(image[0], str) and \
            isinstance(image[1], str)):
            image_list = (image,) * self['numStates']
        else:
            image_list = image

        self.__reinitComponent("image", OnscreenImage, image_list,
            scale=1,
            sort=DGG.IMAGE_SORT_INDEX)

    def handleEnter(self):
        enteranim = self['enteranim']
        if enteranim != None:
            if enteranim == 'fadeinscale':
                r, g, b, a = self.getColorScale()
                x, y, z = self.getScale()
                self.setColorScale(r, g, b, 0)
                self.setScale(0.001, 0.001, 0.001)
                self.enterAnim = Sequence(
                    Parallel(
                      LerpColorScaleInterval(self, 0.3, (r, g, b, a)),
                      LerpScaleInterval(self, 0.3, (x, y, z)),
                    ),
                    Func(self.setAnim),
                )
                self.enterAnim.start()
            else:
                self.setAnim()
        else:
            self.setAnim()

    def setAnim(self):
        anim = self['anim']
        if anim != None:
            if anim == 'stretch':
                x, y, z = self.getScale()
                x_stretch = x + 0.03
                z_stretch = y + 0.03
                self.b_anim = Sequence(
                    LerpScaleInterval(self, duration=0.5, scale=(x_stretch, y, z), startScale=(x, y, z_stretch), blendType='easeInOut'),
                    LerpScaleInterval(self, duration=0.5, scale=(x, y, z_stretch), startScale=(x_stretch, y, z), blendType='easeInOut')
                )
            elif anim == 'stretchslow':
                x, y, z = self.getScale()
                x_stretch = x + 0.03
                z_stretch = y + 0.03
                self.b_anim = Sequence(
                    LerpScaleInterval(self, duration=1.5, scale=(x_stretch, y, z), startScale=(x, y, z_stretch), blendType='easeInOut'),
                    LerpScaleInterval(self, duration=1.5, scale=(x, y, z_stretch), startScale=(x_stretch, y, z), blendType='easeInOut')
                )
            elif anim == 'popinoutfast': # for 2d gui
                x, y, z = self.getScale()
                self.b_anim = Sequence(
                    LerpScaleInterval(self, duration=0.15, scale=(x - 0.01, y - 0.01, z - 0.01), startScale=(x, y, z), blendType='easeIn'),
                    LerpScaleInterval(self, duration=0.15, scale=(x, y, z), startScale=(x - 0.01, y - 0.01, z - 0.01), blendType='easeOut'),
                    Wait(1)
                )
            else:
                return
            self.b_anim.loop()