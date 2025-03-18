from . import Street
import random
from direct.task import Task

class DGStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

        
    def enter(self, requestStatus):
        self.nextBirdTime = 0
        taskMgr.add(self.__birds, 'DG-birds')
        Street.Street.enter(self, requestStatus)

    def exit(self):
        Street.Street.exit(self)
        taskMgr.remove('DG-birds')

    def __birds(self, task):
        if task.time < self.nextBirdTime:
            return Task.cont
        randNum = random.random()
        bird = int(randNum * 100) % 6 + 1
        if bird == 1:
            base.playSfx(self.loader.bird1Sound)
        elif bird == 2:
            base.playSfx(self.loader.bird2Sound)
        elif bird == 3:
            base.playSfx(self.loader.bird3Sound)
        elif bird == 4:
            base.playSfx(self.loader.bird4Sound)
        elif bird == 5:
            base.playSfx(self.loader.bird5Sound)
        elif bird == 6:
            base.playSfx(self.loader.beeSound)
        self.nextBirdTime = task.time + randNum * 20.0
        return Task.cont
