from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task

from toontown.fishing import FishGlobals
from toontown.fishing.FishBase import FishBase
from toontown.toonbase import ToontownGlobals
import time, random

class DistributedFishingSpotAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedFishingSpotAI')
    WAGER_CHANCE = 0.03

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avId = None
        self.pondDoId = None
        self.posHpr = [None, None, None, None, None, None]
        self.cast = False
        self.lastFish = [None, None, None, None]
        self.lastHit = 0
        self.lastCast = [0, 0]
        self.wager = [0, 0]

    def generate(self):
        DistributedObjectAI.generate(self)

        pond = self.air.doId2do.get(self.pondDoId)
        pond.addSpot(self)

    def setPondDoId(self, pondDoId):
        self.pondDoId = pondDoId

    def getPondDoId(self):
        return self.pondDoId

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = [x, y, z, h, p, r]

    def getPosHpr(self):
        return self.posHpr

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != None:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId = avId, issue = 'Toon requested to enter a pier twice!')
            self.sendUpdateToAvatarId(avId, 'rejectEnter', [])
            return
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if av.getFishingSpotId():
            self.air.moderationManager.serverKick(avId, 'Requested to enter fishing spot, but already on one!')
            return        

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.removeFromPier)
        self.b_setOccupied(avId)
        av.setFishingSpotId(self.doId)
        self.d_setMovie(FishGlobals.EnterMovie, 0, 0, 0, 0, 0, 0)
        taskMgr.remove('cancelAnimation%d' % self.doId)
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancelAnimation%d' % self.doId, [self])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])
        taskMgr.remove('bingo-status-%d' % self.doId)
        taskMgr.doMethodLater(2, self.sendBingoStatus, 'bingo-status-%d' % self.doId)
        self.lastFish = [None, None, None]
        self.cast = False

    def sendBingoStatus(self, _ = None):
        # Send bingo status to avatar
        pond = self.air.doId2do.get(self.pondDoId)

        if not pond:
            return

        if pond.bingoMgr:
            pond.bingoMgr.sendStatesToAvatar(self.avId)

    def rejectEnter(self):
        pass

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon requested to exit a pier they\'re not on!')
            return
        self.ignore(self.air.getAvatarExitEvent(avId))
        self.removeFromPierWithAnim()

    def setOccupied(self, avId):
        self.avId = avId

    def d_setOccupied(self, avId):
        self.sendUpdate('setOccupied', [avId])

    def b_setOccupied(self, avId):
        self.setOccupied(avId)
        self.d_setOccupied(avId)

    def doCast(self, p, h):
        if [p, h] == self.lastCast:
            self.removeFromPierWithAnim()
            return
        self.lastCast = [p, h]
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to cast from a pier they\'re not on!')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to cast while not on district!')
            return
        money = av.getMoney()
        cost = FishGlobals.getCastCost(av.getFishingRod())
        if money < cost:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to cast without enough jellybeans!')
            return
        if len(av.fishTank) >= av.getMaxFishTank():
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to cast with too many fish!')
            return
        av.takeMoney(cost, False)
        self.d_setMovie(FishGlobals.CastMovie, 0, 0, 0, 0, p, h)
        taskMgr.remove('cancelAnimation%d' % self.doId)
        taskMgr.doMethodLater(2, DistributedFishingSpotAI.cancelAnimation, 'cancelAnimation%d' % self.doId, [self])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])
        self.cast = True

    def sellFish(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId != avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to sell fish at a pier they\'re not using!')
            return
        if self.air.doId2do[pondDoId].getArea() != ToontownGlobals.MyEstate:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to sell fish at a pier not in their estate!')
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to sell fish while not on district!')
            return
        result = self.air.fishManager.creditFishTank(av)
        totalFish = len(av.fishCollection)
        self.sendUpdateToAvatarId(avId, 'sellFishComplete', [result, totalFish])
        taskMgr.remove('timeOut%d' % self.doId)
        taskMgr.doMethodLater(45, DistributedFishingSpotAI.removeFromPierWithAnim, 'timeOut%d' % self.doId, [self])
        
    def wagerFish(self, fish):
    
        def parseOffer(value, offer):
            offerint = int(offer[1:])
            if offer.startswith('-'):
                return value - offerint
            elif offer.startswith('+'):
                return value + offerint
            elif offer.startswith('*'):
                return value * offerint
    
        rarity = fish.getRarity()
        value = fish.getValue()
        if rarity <= 3:
            if not value == 1:
                offerScale = ['-1', '-1', '-1', '+0', '+0', '+1', '+2']
                chosenOffer = random.choice(offerScale)
                return parseOffer(value, chosenOffer)
            return value
        elif rarity > 3 and rarity <= 6:
            if not value == 3:
                offerScale = ['-3', '-3', '-2', '-2', '-1', '+2', '+2', '+3', '+3', '+3', '*3']
                chosenOffer = random.choice(offerScale)
                return parseOffer(value, chosenOffer)
            return value
        return value
                

    def sellFishComplete(self, todo0, todo1):
        pass

    def setMovie(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def d_setMovie(self, mode, code, genus, species, weight, p, h):
        self.sendUpdate('setMovie', [mode, code, genus, species, weight, p, h])

    def removeFromPier(self):
        taskMgr.remove('timeOut%d' % self.doId)
        av = self.air.doId2do.get(self.avId)
        if av:
            av.exitFromFishingSpot()
        self.cancelAnimation()
        self.d_setOccupied(0)
        self.avId = None
        self.lastHit = 0
        self.lastFish = [0, 0]
        self.wager = [0, 0]

    def removeFromPierWithAnim(self):
        taskMgr.remove('cancelAnimation%d' % self.doId)
        self.d_setMovie(FishGlobals.ExitMovie, 0, 0, 0, 0, 0, 0)
        taskMgr.doMethodLater(1, DistributedFishingSpotAI.removeFromPier, 'remove%d' % self.doId, [self])

    def considerReward(self, target):
        if time.time() - self.lastHit <= 1:
            av = self.air.doId2do.get(self.avId)
            if av:
                self.air.moderationManager.serverKick(avId, 'Toon is finishing too fast!')
            return
        if not self.cast:
            self.air.writeServerEvent('suspicious', avId=self.avId, issue='Toon tried to fish without casting!')
            return

        av = self.air.doId2do.get(self.avId)
        area = self.air.doId2do.get(self.pondDoId).getArea()

        catch = self.air.fishManager.generateCatch(av, area)

        self.lastFish = catch
        
        if catch[0] == FishGlobals.FishItem and random.random() <= self.WAGER_CHANCE:
            fish = FishBase(catch[1], catch[2], catch[3])
            wager = self.wagerFish(fish)
            self.wager = [wager, catch]
            self.sendUpdateToAvatarId(self.avId, 'makeWager', [wager, fish.getValue(), fish.getWeight()]) 
        else:
            self.d_setMovie(FishGlobals.PullInMovie, catch[0], catch[1], catch[2], catch[3], 0, 0)
            self.cast = False
            
    def wagerResponse(self, response):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='FishingSpotAI.wagerResponse: requested wager for another avId.')
            return
        if self.wager == [0, 0]:
            self.air.writeServerEvent('suspicious', avId=avId, issue='FishingSpotAI.wagerResponse: wager has not been set.')
            return           
    
        if response == 0:
            catch = self.wager[1]
            self.d_setMovie(FishGlobals.PullInMovie, catch[0], catch[1], catch[2], catch[3], 0, 0)
            self.cast = False
            self.wager = [0, 0]
        else:
            self.cast = False
            av = self.air.doId2do[self.avId]
            av.addMoney(self.wager[0])
            av.fishTank.removeFishAtIndex(len(av.fishTank.fishList) -1)
            netlist = av.fishTank.getNetLists()
            av.fishTank.makeFromNetLists(netlist[0], netlist[1], netlist[2])
            av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
            av.d_setFishTank(netlist[0], netlist[1], netlist[2])

    def cancelAnimation(self):
        self.d_setMovie(FishGlobals.NoMovie, 0, 0, 0, 0, 0, 0)