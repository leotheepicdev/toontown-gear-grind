from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.otpbase import OTPGlobals

class DistributedDistrictAI(DistributedObjectAI):
    notify = directNotify.newCategory("DistributedDistrictAI")
    name = 'District'
    available = 0
    districtPopLimits = OTPGlobals.DefaultDistrictPopLimits

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setAvailable(self, available):
        self.available = available

    def d_setAvailable(self, available):
        self.sendUpdate('setAvailable', [available])

    def b_setAvailable(self, available):
        self.setAvailable(available)
        self.d_setAvailable(available)

    def getAvailable(self):
        return self.available
        
    def setDistrictPopLimits(self, districtPopLimits):
        self.districtPopLimits = districtPopLimits
        
    def d_setDistrictPopLimits(self, districtPopLimits):
        self.sendUpdate('setDistrictPopLimits', [districtPopLimits])
        
    def b_setDistrictPopLimits(self, districtPopLimits):
        self.setDistrictPopLimits(districtPopLimits)
        self.d_setDistrictPopLimits(districtPopLimits)
        
    def getDistrictPopLimits(self):
        return self.districtPopLimits

