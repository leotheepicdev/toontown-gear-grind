from panda3d.core import *
from direct.distributed.ClockDelta import *
import math
import random
from panda3d.core import Point3
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
from . import SuitTimings
from . import SuitDNA
from toontown.toonbase import TTLocalizer
from panda3d.toontown import SuitLegList
TIME_BUFFER_PER_WPT = 0.25
TIME_DIVISOR = 100
DISTRIBUTE_TASK_CREATION = 0

class SuitBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitBase')

    def __init__(self):
        self.dna = None
        self.level = 0
        self.maxHP = 10
        self.currHP = 10
        self.isSkelecog = 0
        return

    def delete(self):
        if hasattr(self, 'legList'):
            del self.legList

    def getStyleName(self):
        if hasattr(self, 'dna') and self.dna:
            return self.dna.name
        else:
            self.notify.error('called getStyleName() before dna was set!')
            return 'unknown'

    def getStyleDept(self):
        if hasattr(self, 'dna') and self.dna:
            return SuitDNA.getDeptFullname(self.dna.dept)
        else:
            self.notify.error('called getStyleDept() before dna was set!')
            return 'unknown'

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level
        if self.dna.name == 'null':
            self.maxHP = SuitBattleGlobals.NullLevel2HP[self.actualLevel]
            self.currHP = self.maxHP
            nameWLevel = TTLocalizer.SuitBaseNameWithoutDept % {'name': self.name,
             'level': self.getActualLevel()}
            self.setDisplayName(nameWLevel)
        elif self.dna.name != 'null' and self.dna.dept not in ['c', 'l', 's', 'm']:
            nameWLevel = TTLocalizer.SuitBaseNameWithoutDept % {'name': self.name,
             'level': self.getActualLevel()}
            self.setDisplayName(nameWLevel)
            attributes = SuitBattleGlobals.SuitAttributes[self.dna.name]
            self.maxHP = attributes['hp'][self.level]
            self.currHP = self.maxHP
        else:
            nameWLevel = TTLocalizer.SuitBaseNameWithLevel % {'name': self.name,
             'dept': self.getStyleDept(),
             'level': self.getActualLevel()}
            self.setDisplayName(nameWLevel)
            attributes = SuitBattleGlobals.SuitAttributes[self.dna.name]
            self.maxHP = attributes['hp'][self.level]
            self.currHP = self.maxHP

    def getSkelecog(self):
        return self.isSkelecog

    def setSkelecog(self, flag):
        self.isSkelecog = flag

    def setPath(self, path):
        self.path = path
        self.pathLength = self.path.getNumPoints()

    def getPath(self):
        return self.path

    def printPath(self):
        print('%d points in path' % self.pathLength)
        for currPathPt in range(self.pathLength):
            indexVal = self.path.getPointIndex(currPathPt)
            print('\t', self.sp.dnaStore.getSuitPointWithIndex(indexVal))

    def makeLegList(self):
        self.legList = SuitLegList(self.path, self.sp.dnaStore, self.sp.suitWalkSpeed, SuitTimings.fromSky, SuitTimings.toSky, SuitTimings.fromSuitBuilding, SuitTimings.toSuitBuilding, SuitTimings.toToonBuilding)
