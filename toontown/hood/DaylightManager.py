from direct.distributed.DistributedObject import DistributedObject

class DaylightManager(DistributedObject):
    neverDisable = 1
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        base.cr.daylightManager = self
        
    def d_requestTime(self):
        self.sendUpdate('requestTime')
        
    def receiveTime(self, elaspedTime, serverTime):
        try:
            hood = base.cr.playGame.hood
            hood.adjustDaylight(elaspedTime, serverTime)
        except:
            pass