from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class ToontownDistrictStatsAI(DistributedObjectAI):
    notify = directNotify.newCategory('ToontownDistrictStatsAI')

    districtId = 0
    avatarCount = 0
    newAvatarCount = 0

    def settoontownDistrictId(self, districtId):
        self.districtId = districtId

    def gettoontownDistrictId(self):
        return self.districtId

    def d_settoontownDistrictId(self, districtId):
        self.sendUpdate('settoontownDistrictId', [districtId])

    def b_settoontownDistrictId(self, districtId):
        self.d_settoontownDistrictId(districtId)
        self.settoontownDistrictId(districtId)

    def setAvatarCount(self, avCount):
        self.avatarCount = avCount

    def getAvatarCount(self):
        return self.avatarCount

    def d_setAvatarCount(self, avCount):
        self.sendUpdate('setAvatarCount', [avCount])

    def b_setAvatarCount(self, avCount):
        self.d_setAvatarCount(avCount)
        self.setAvatarCount(avCount)

    def setNewAvatarCount(self, newAvCount):
        self.newAvatarCount = newAvCount

    def getNewAvatarCount(self):
        return self.newAvatarCount

    def d_setNewAvatarCount(self, newAvCount):
        self.sendUpdate('setNewAvatarCount', [newAvCount])

    def b_setNewAvatarCount(self, newAvCount):
        self.setNewAvatarCount(newAvCount)
        self.d_setNewAvatarCount(newAvCount)