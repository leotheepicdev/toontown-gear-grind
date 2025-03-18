from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
from toontown.suit import SuitDNA
from toontown.hood import ZoneUtil
from toontown.suit import SuitInvasionGlobals
import random

class SuitInvasionManagerAI:
    notify = directNotify.newCategory('SuitInvasionManagerAI')
    SPECIAL_CHANCE = 0.1
    # TODO: Mega invasions that happen on certain holidays
    # TODO: allow for V2.0s and other flags
    # TODO: make these variables toggleable

    def __init__(self, air):
        self.air = air

        self.invadingCogs = ([], 0) 
        self.numCogs = 0
        self.numCogsRemaining = 0
        self.invType = SuitInvasionGlobals.INV_NORMAL
        if simbase.air.isInvasionOnly:
            self.invading = True
        else:
            self.invading = False

    def startRandomInvasionTick(self):
        # Every 30 to 90 minutes, an invasion can be generated.
        taskMgr.doMethodLater(random.randint(1800, 5400), self.generateRandomInvasion, 'random-invasion')
        
    def generateRandomInvasion(self, task=None):
        if not simbase.air.isInvasionOnly:
            if self.invading:
                return task.again
            if random.random() >= 0.8:
                # Sometimes, we don't want to invade.
                return task.again
                
        if random.random() <= self.SPECIAL_CHANCE:
            self.invType = random.randint(1, 9)
            cogList = SuitInvasionGlobals.INV_2_COGS[self.invType]
        else:
            self.invType = SuitInvasionGlobals.INV_NORMAL
            cogList = [random.choice(SuitDNA.suitHeadTypes)]            
                
        numCogs = random.randint(1000, 6000)
        specialCog = 0
        self.startInvasion(cogList, numCogs, specialCog)
        if task:
            return task.done

    def setInvadingCogs(self, cogList, specialCog):
        self.invadingCogs = (cogList, specialCog)

    def getInvadingCog(self):
        invadingCogs, special = self.invadingCogs[0], self.invadingCogs[1]
        if invadingCogs:
            invadingCog = random.choice(invadingCogs)
        else:
            invadingCog = None
        return (invadingCog, special)

    def getInvading(self):
        return self.invading

    def _spGetOut(self):
        for suitPlanner in list(self.air.suitPlanners.values()):
            if ZoneUtil.isWelcomeValley(suitPlanner.zoneId):
                continue
            suitPlanner.flySuits()
            
    def decrementNumCogs(self):
        self.numCogsRemaining -= 1
        if self.numCogsRemaining <= 0:
            self.stopInvasion()

    def stopInvasion(self, task = None):
        if not self.getInvading():
            return

        self.air.newsManager.d_setInvasionStatus(ToontownGlobals.SuitInvasionEnd, self.invadingCogs[0], self.numCogs, self.invadingCogs[1], self.invType)
        if task:
            task.remove()
        else:
            taskMgr.remove('invasion-timeout')

        self.numCogs = 0
        self.numCogsRemaining = 0
        self.invType = SuitInvasionGlobals.INV_NORMAL
        if simbase.air.isInvasionOnly:
            self.generateRandomInvasion()
        else:
            self.setInvadingCogs([], 0)
            self.invading = False
            self._spGetOut()
        if simbase.air.wantRandomInvasions:
            self.startRandomInvasionTick()        

    def startInvasion(self, cogList, numCogs, specialCog):
        if not simbase.air.isInvasionOnly and self.getInvading():
            return False
        if taskMgr.hasTaskNamed('random-invasion'):
            taskMgr.remove('random-invasion')
        self.numCogs = numCogs
        self.numCogsRemaining = numCogs
        self.setInvadingCogs(cogList, specialCog)
        self.invading = True
        self.air.newsManager.d_setInvasionStatus(ToontownGlobals.SuitInvasionBegin, cogList, numCogs, specialCog, self.invType)
        self._spGetOut()
        timePerSuit = config.GetFloat('invasion-time-per-suit', 1.2)
        taskMgr.doMethodLater(self.numCogs * timePerSuit, self.stopInvasion, 'invasion-timeout')
        return True
