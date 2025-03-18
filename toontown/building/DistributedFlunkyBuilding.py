from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import TextNode, DecalEffect
from toontown.toonbase import TTLocalizer, ToontownGlobals

class DistributedFlunkyBuilding(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.model = None
        self.elevatorDoId = 0
        self.posHpr = (0, 0, 0, 0, 0, 0)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.loadModel()
        
    def delete(self):
        DistributedObject.delete(self)
        if self.model:
            self.model.removeNode()
            self.model = None
        
    def loadModel(self):
        self.model = loader.loadModel('phase_4/models/modules/suit_landmark_corp')
        self.model.setPosHpr(*self.getPosHpr())
        self.model.reparentTo(render)
        
        buildingTitle = TTLocalizer.FlunkyCogBuildingName
        textNode = TextNode('sign')
        textNode.setTextColor(1.0, 1.0, 1.0, 1.0)
        textNode.setFont(ToontownGlobals.getSuitFont())
        textNode.setAlign(TextNode.ACenter)
        textNode.setWordwrap(17.0)
        textNode.setText(buildingTitle)
        textHeight = textNode.getHeight()
        zScale = (textHeight + 2) / 3.0
        signOrigin = self.model.find('**/sign_origin;+s')
        backgroundNP = loader.loadModel('phase_5/models/modules/suit_sign')
        backgroundNP.reparentTo(signOrigin)
        backgroundNP.setPosHprScale(0.0, 0.0, textHeight * 0.8 / zScale, 0.0, 0.0, 0.0, 8.0, 8.0, 8.0 * zScale)
        signTextNodePath = backgroundNP.attachNewNode(textNode.generate())
        signTextNodePath.setPosHprScale(0.0, -0.02, -0.21 + textHeight * 0.1 / zScale, 0.0, 0.0, 0.0,  0.1, 0.1, 0.1 / zScale)
        signTextNodePath.setColor(1.0, 1.0, 1.0, 1.0)
        frontNP = self.model.find('**/*_front/+GeomNode;+s')
        backgroundNP.wrtReparentTo(frontNP)
        frontNP.node().setEffect(DecalEffect.make())        
        
        
        elevator = base.cr.doId2do.get(self.elevatorDoId)
        if elevator:
            elevatorModel = elevator.elevatorModel
            elevatorModel.reparentTo(self.model.find("**/*_door_origin"))
            cab = elevatorModel.find('**/elevator')
            flunkySZ = loader.loadModel('phase_4/models/props/flunkySZ')
            flunkyIcon = flunkySZ.find('**/flunkySZ').copyTo(cab)
            flunkyIcon.setPos(0, 6.79, 6.8)
            flunkyIcon.setScale(3)
            flunkySZ.removeNode()
            
        
    def setElevatorDoId(self, elevatorDoId):
        self.elevatorDoId = elevatorDoId
        
    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)
        
    def getPosHpr(self):
        return self.posHpr