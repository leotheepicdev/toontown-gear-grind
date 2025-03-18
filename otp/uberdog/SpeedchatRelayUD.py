from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class SpeedchatRelayUD(DistributedObjectUD):
    notify = directNotify.newCategory('SpeedchatRelayUD')

    def forwardSpeedchat(self, todo0, todo1, todo2, todo3, todo4):
        pass
