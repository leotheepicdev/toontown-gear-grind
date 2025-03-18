from otp.level.DistributedEntityAI import DistributedEntityAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedInteractiveEntityAI(DistributedEntityAI):
    notify = directNotify.newCategory('DistributedInteractiveEntityAI')

    def setAvatarInteract(self, todo0):
        pass

    def requestInteract(self):
        pass

    def rejectInteract(self):
        pass

    def requestExit(self):
        pass

    def avatarExit(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass
