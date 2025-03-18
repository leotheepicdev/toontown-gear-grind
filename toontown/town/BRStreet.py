from direct.task.Task import Task
import random
from . import Street
from toontown.battle import BattleParticles

class BRStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

    def enter(self, requestStatus):
        taskMgr.doMethodLater(1, self.__windTask, 'BR-wind')
        Street.Street.enter(self, requestStatus)

    def exit(self):
        Street.Street.exit(self)
        taskMgr.remove('BR-wind')

    def __windTask(self, task):
        base.playSfx(random.choice(self.loader.windSound))
        time = random.random() * 8.0 + 1
        taskMgr.doMethodLater(time, self.__windTask, 'BR-wind')
        return Task.done
