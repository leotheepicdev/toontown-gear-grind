from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.otpbase.OTPLocalizer import EmoteFuncDict

class DistributedResistanceEmoteMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedResistanceEmoteMgrAI')

    def addResistanceEmote(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if not av.emoteAccess[EmoteFuncDict['Resistance Salute']]:
            av.emoteAccess[EmoteFuncDict['Resistance Salute']] = 1
            av.b_setEmoteAccess(av.emoteAccess)