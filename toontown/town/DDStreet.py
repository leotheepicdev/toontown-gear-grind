from . import Street
from direct.task.Task import Task
import random

class DDStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)
        
    def enter(self, requestStatus):
        self.nextSeagullTime = 0
        taskMgr.add(self.__seagulls, 'dd-seagulls')
        self.loader.hood.setWhiteFog()
        Street.Street.enter(self, requestStatus)

    def exit(self):
        taskMgr.remove('dd-seagulls')      
        self.loader.hood.setNoFog()
        Street.Street.exit(self)


    def __seagulls(self, task):
        if task.time < self.nextSeagullTime:
            return Task.cont
        base.playSfx(self.loader.seagullSound)
        self.nextSeagullTime = task.time + random.random() * 4.0 + 8.0
        return Task.cont
