from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class SettingsMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('SettingsMgrAI')

    def requestAllChangedSettings(self):
        pass

    def settingChange(self, todo0, todo1):
        pass
