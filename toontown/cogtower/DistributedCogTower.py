from direct.distributed.DistributedObject import DistributedObject

class DistributedCogTower(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.generate(self)
