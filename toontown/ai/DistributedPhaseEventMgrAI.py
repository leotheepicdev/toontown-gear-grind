from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedPhaseEventMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedPhaseEventMgrAI')

    def __init__(self, air, isRunning, numPhases, curPhase, holidayDates):
        DistributedObjectAI.__init__(self, air)

        self.isRunning = isRunning
        self.numPhases = numPhases
        self.curPhase = curPhase
        self.holidayDates = holidayDates

    def b_setNumPhases(self, numPhases):
        self.d_setNumPhases(numPhases)
        self.setNumPhases(numPhases)

    def d_setNumPhases(self, numPhases):
        self.sendUpdate('setNumPhases', [numPhases])

    def setNumPhases(self, numPhases):
        self.numPhases = numPhases

    def getNumPhases(self):
        return self.numPhases

    def b_setDates(self, holidayDates):
        self.d_setDates(holidayDates)
        self.setDates(holidayDates)

    def d_setDates(self, holidayDates):
        self.sendUpdate('setDates', [holidayDates])

    def setDates(self, holidayDates):
        self.holidayDates = holidayDates

    def getDates(self):
        return self.holidayDates

    def b_setCurPhase(self, curPhrase):
        self.d_setCurPhase(curPhrase)
        self.setCurPhase(curPhrase)

    def d_setCurPhase(self, curPhrase):
        self.sendUpdate('setCurPhase', [curPhrase])

    def setCurPhase(self, curPhrase):
        self.curPhase = curPhrase

    def getCurPhase(self):
        return self.curPhase

    def b_setIsRunning(self, isRunning):
        self.d_setIsRunning(isRunning)
        self.setIsRunning(isRunning)

    def d_setIsRunning(self, isRunning):
        self.sendUpdate('setIsRunning', [isRunning])

    def setIsRunning(self, isRunning):
        self.isRunning = isRunning

    def getIsRunning(self):
        return self.isRunning