from direct.distributed.DistributedObject import DistributedObject

class DistributedHotTub(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.pos = (0, 0, 0)

    def generate(self):
        print("can't have my toontown without my hot tubs!")
        DistributedObject.generate(self)
        self.loadModel()
        
    def delete(self):
        DistributedObject.delete(self)
        
    def setPos(self, x, y, z):
        self.pos = (x, y, z)
        
    def loadModel(self):
        pass
        
    def unloadModel(self):
        pass
        
    def __collisionTouched(self):
        pass