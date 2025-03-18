from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class SettingsMgrUD(DistributedObjectUD):
    notify = directNotify.newCategory('SettingsMgrUD')

    def requestAllChangedSettings(self):
        pass

    def settingChange(self, todo0, todo1):
        pass
