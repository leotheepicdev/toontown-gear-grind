from otp.ai.AIBaseGlobal import *
from otp.avatar import DistributedAvatarAI
from . import SuitBase, SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
import random

class DistributedSuitBaseAI(DistributedAvatarAI.DistributedAvatarAI, SuitBase.SuitBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitBaseAI')

    def __init__(self, air, suitPlanner):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        SuitBase.SuitBase.__init__(self)
        self.sp = suitPlanner
        self.maxHP = 10
        self.currHP = 10
        self.zoneId = 0
        self.dna = None
        self.virtual = 0
        self.skeleRevives = 0
        self.maxSkeleRevives = 0
        self.reviveFlag = 0
        self.buildingHeight = None
        self.attacks = {}
        self.actualLevel = 1
        self.giveMerits = True
        self.sued = False
        self.status2ToonIds = {}
        self.atk2DmgAdd = {}

    def generate(self):
        DistributedAvatarAI.DistributedAvatarAI.generate(self)

    def delete(self):
        self.sp = None
        del self.dna
        del self.attacks

        DistributedAvatarAI.DistributedAvatarAI.delete(self)
        SuitBase.SuitBase.delete(self)

    def requestRemoval(self):
        if self.sp != None:
            self.sp.removeSuit(self)
        else:
            self.requestDelete()
        return

    def setLevel(self, lvl=None):
        attributes = SuitBattleGlobals.SuitAttributes[self.dna.name]
        if lvl:
            self.setActualLevel(lvl)
        if lvl:
            self.level = lvl - attributes['level'] - 1
        else:
            self.level = SuitBattleGlobals.pickFromFreqList(attributes['freq'])
        self.notify.debug('Assigning level ' + str(lvl))
        if hasattr(self, 'doId'):
            self.d_setLevelDist(self.level)
        hp = attributes['hp'][self.level]
        self.maxHP = hp
        self.currHP = hp

    def getLevelDist(self):
        return self.getLevel()

    def d_setLevelDist(self, level):
        self.sendUpdate('setLevelDist', [level])
        
    def getActualLevel(self):
        return self.actualLevel
        
    def setActualLevel(self, level):
        self.actualLevel = level
        
    def setupNullCog(self, level):
        dna = SuitDNA.SuitDNA()
        dna.newSuitNull(level)
        self.dna = dna
        self.track = 'null'
        self.setActualLevel(level)
        self.maxHP = SuitBattleGlobals.NullLevel2HP[level]
        self.currHP = self.maxHP
        
        body = self.dna.body
        if body == 'a':
            attackList = SuitBattleGlobals.CogAAttacks.copy()
        elif body == 'b':
            attackList = SuitBattleGlobals.CogBAttacks.copy()
        elif body == 'c':
            attackList = SuitBattleGlobals.CogCAttacks.copy()
            
        attackNum = random.choice(SuitBattleGlobals.NullNumAttacks)
        for i in range(attackNum):
            dmg = random.randint(SuitBattleGlobals.NullLevels2Damage[level][0], SuitBattleGlobals.NullLevels2Damage[level][1])
            acc = random.randint(SuitBattleGlobals.NullLevels2Acc[level][0], SuitBattleGlobals.NullLevels2Acc[level][1])
            freq = random.choice(SuitBattleGlobals.NullNumAttacks2Freq[attackNum])
            attackChoice = random.choice(attackList)
            self.attacks[random.choice(attackList)] = {'dmg': dmg, 'acc': acc, 'freq': freq}
            attackList.remove(attackChoice)

    def setupSuitDNA(self, level, type, track, allowBuildingCogs=False):
        dna = SuitDNA.SuitDNA()
        if allowBuildingCogs:
            dna.newSuitBuilding(level, track, 0.9, street=True)
        else:
            dna.newSuitRandom(type, track)
        self.dna = dna
        self.track = track
        self.setLevel(level)

    def getDNAString(self):
        if self.dna:
            return self.dna.makeNetString()
        else:
            self.notify.debug('No dna has been created for suit %d!' % self.getDoId())
            return ''

    def b_setBrushOff(self, index):
        self.setBrushOff(index)
        self.d_setBrushOff(index)
        return None

    def d_setBrushOff(self, index):
        self.sendUpdate('setBrushOff', [index])

    def setBrushOff(self, index):
        pass

    def d_denyBattle(self, toonId):
        self.sendUpdateToAvatarId(toonId, 'denyBattle', [])

    def b_setSkeleRevives(self, num):
        if num == None:
            num = 0
        self.setSkeleRevives(num)
        self.d_setSkeleRevives(self.getSkeleRevives())
        return

    def d_setSkeleRevives(self, num):
        self.sendUpdate('setSkeleRevives', [num])

    def getSkeleRevives(self):
        return self.skeleRevives

    def setSkeleRevives(self, num):
        if num == None:
            num = 0
        self.skeleRevives = num
        if num > self.maxSkeleRevives:
            self.maxSkeleRevives = num
        return

    def getMaxSkeleRevives(self):
        return self.maxSkeleRevives

    def useSkeleRevive(self):
        self.skeleRevives -= 1
        self.currHP = self.maxHP
        self.reviveFlag = 1

    def reviveCheckAndClear(self):
        returnValue = 0
        if self.reviveFlag == 1:
            returnValue = 1
            self.reviveFlag = 0
        return returnValue

    def getHP(self):
        return self.currHP

    def setHP(self, hp):
        if hp > self.maxHP:
            self.currHP = self.maxHP
        else:
            self.currHP = hp
        return None

    def b_setHP(self, hp):
        self.setHP(hp)
        self.d_setHP(hp)

    def d_setHP(self, hp):
        self.sendUpdate('setHP', [hp])

    def releaseControl(self):
        return None

    def getDeathEvent(self):
        return 'cogDead-%s' % self.doId

    def resume(self):
        self.notify.debug('resume, hp=%s' % self.currHP)
        if self.currHP <= 0:
            messenger.send(self.getDeathEvent())
            self.requestRemoval()
        return None

    def prepareToJoinBattle(self):
        pass

    def b_setSkelecog(self, flag):
        self.setSkelecog(flag)
        self.d_setSkelecog(flag)

    def setSkelecog(self, flag):
        SuitBase.SuitBase.setSkelecog(self, flag)

    def d_setSkelecog(self, flag):
        self.sendUpdate('setSkelecog', [flag])

    def isForeman(self):
        return 0

    def isSupervisor(self):
        return 0
        
    def b_setVirtual(self, virtual):
        self.setVirtual(virtual)
        self.d_setVirtual(virtual)

    def setVirtual(self, virtual):
        self.virtual = virtual
        if virtual == SuitBattleGlobals.VIRTUAL_GREEN:
            self.maxHP *= SuitBattleGlobals.VIRTUAL_GREEN_HP_MULT
            self.currHP *= SuitBattleGlobals.VIRTUAL_GREEN_HP_MULT
            
    def d_setVirtual(self, virtual):
        self.sendUpdate('setVirtual', [virtual])

    def getVirtual(self):
        return self.virtual
        
    def setGiveMerits(self, giveMerits):
        self.giveMerits = giveMerits
        
    def getGiveMerits(self):
        return self.giveMerits
        
    def setSued(self, sued):
        self.sued = sued
    
    def getSued(self):
        return self.sued