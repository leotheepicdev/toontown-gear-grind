from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.interval.IntervalGlobal import *
from .DaylightGlobals import *
import random, time

class DaylightManagerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.seq = None
        self.timeOfDay = DAY
        self.chosenTime = random.choice(TIMES_LIST)
    
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.startServerDaylight()
        
    def delete(self):
        DistributedObjectAI.delete(self)
        self.seq.finish()

    def requestTime(self):
        avId = self.air.getAvatarIdFromSender()
        
        timeElasped = self.seq.getT()
        serverTime = time.time()
        
        self.sendUpdateToAvatarId(avId, 'receiveTime', [timeElasped, serverTime])
        
    def restartSequence(self):
        self.seq.finish()
        self.seq.start()

    def startServerDaylight(self):
        self.seq = Sequence(
                       Parallel(Func(self.setTimeOfDay, DAY), Wait(DAY_TIME)),
                       Parallel(Func(self.setTimeOfDay, DUSK), Wait(DUSK_TIME)),
                       Parallel(Func(self.setTimeOfDay, NIGHT), Wait(NIGHT_TIME)),
                       Parallel(Func(self.setTimeOfDay, DAWN), Wait(DAWN_TIME)),
                       Func(self.restartSequence)
                  )
        self.seq.start(self.chosenTime)

    def setTimeOfDay(self, timeOfDay):
        self.timeOfDay = timeOfDay
        
    def isDay(self):
        return self.timeOfDay == DAY
        
    def isDawn(self):
        return self.timeOfDay == DAWN
        
    def isDusk(self):
        return self.timeOfDay == DUSK
        
    def isNight(self):
        return self.timeOfDay == NIGHT