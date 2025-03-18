from panda3d.core import *

def loadCardModel(name='card', frame=(-1, 1, -1, 1), transparency=False):
    card = CardMaker(name)
    card.setFrame(*frame)
    card = NodePath(card.generate())
    if transparency:
        card.setTransparency(True)
    return card

def loadTextureModel(texture, name='card', frame=(-1, 1, -1, 1), transparency=False):
    card = loadCardModel(name, frame, transparency)
    card.setTexture(texture, 1)
    return card