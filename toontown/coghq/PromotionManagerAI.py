from otp.ai.AIBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
import random
from toontown.hood import ZoneUtil
from toontown.suit import SuitDNA
from . import CogDisguiseGlobals
from toontown.toonbase.ToontownBattleGlobals import getInvasionMultiplier
from functools import reduce
MeritMultiplier = 0.5

class PromotionManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('PromotionManagerAI')

    def __init__(self, air):
        self.air = air

    def getPercentChance(self):
        return 100.0

    def recoverMerits(self, av, cogList, zoneId, multiplier = 1, extraMerits = None, respectInvasions=True):
        avId = av.getDoId()
        meritsRecovered = [0, 0, 0, 0]
        if extraMerits is None:
            extraMerits = [0, 0, 0, 0]
        if respectInvasions:
            if self.air.suitInvasionManager.getInvading() and not ZoneUtil.isWelcomeValley(zoneId):
                multiplier *= getInvasionMultiplier()
        for i in range(len(extraMerits)):
            if CogDisguiseGlobals.isSuitComplete(av.getCogParts(), i):
                meritsRecovered[i] += extraMerits[i]
        for cogDict in cogList:
            if cogDict['track'] not in SuitDNA.suitDepts:
                continue
            if avId in cogDict['activeToons']:
                deptIndex = SuitDNA.suitDepts.index(cogDict['track'])
                if CogDisguiseGlobals.isSuitComplete(av.getCogParts(), deptIndex):
                    self.notify.debug('recoverMerits: checking against cogDict: %s' % cogDict)
                    rand = random.random() * 100
                    giveMerits = cogDict.get('giveMerits', 1)
                    if rand <= self.getPercentChance() and giveMerits:
                        merits = cogDict['level'] * MeritMultiplier
                        merits = int(round(merits))
                        if cogDict['hasRevives']:
                            merits *= 2
                        if cogDict['sued']:
                            merits *= 4
                        merits = merits * multiplier
                        merits = int(round(merits))
                        meritsRecovered[deptIndex] += merits
        if meritsRecovered != [0, 0, 0, 0]:
            actualCounted = [0, 0, 0, 0]
            merits = av.getCogMerits()
            for i in range(len(meritsRecovered)):
                max = CogDisguiseGlobals.getTotalMerits(av, i)
                if max:
                    if merits[i] + meritsRecovered[i] <= max:
                        actualCounted[i] = meritsRecovered[i]
                        merits[i] += meritsRecovered[i]
                    else:
                        actualCounted[i] = max - merits[i]
                        merits[i] = max
                    av.b_setCogMerits(merits)
        return meritsRecovered
