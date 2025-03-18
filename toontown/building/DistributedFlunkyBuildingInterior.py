from panda3d.core import TextNode, Point3, Vec3, VBase3
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import ClassicFSM, State
from toontown.building.ElevatorConstants import *
from toontown.building import ElevatorUtils
from toontown.toon import NPCToons
from toontown.suit.Suit import Suit
from toontown.suit.SuitDNA import SuitDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals, ToontownBattleGlobals
from lib.libotp._constants import CFSpeech

class DistributedFlunkyBuildingInterior(DistributedObject):
    id = 0

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.toons = []
        self.activeIntervals = {}
        self.openSfx = loader.loadSfx('phase_5/audio/sfx/elevator_door_open.ogg')
        self.closeSfx = loader.loadSfx('phase_5/audio/sfx/elevator_door_close.ogg')
        self.currentFloor = 0
        self.elevatorOutOpen = 0
        self.suits = []
        self.activeSuits = []
        self.reserveSuits = []
        self.elevatorName = self.__uniqueName('elevator')
        self.floorModel = None
        self.tom = None
        self.flunky = None
        self.BottomFloor_SuitPositions = [Point3(0, 15, 0),
         Point3(10, 20, 0),
         Point3(-8, 20, 0),
         Point3(-10, 0, 0)]
        self.BottomFloor_SuitHs = [170,
         170,
         190,
         190]
        self.BossOffice_SuitPositions = [Point3(13, 20, 0),
         Point3(0, 15, 0),
         Point3(8, 6, 0),
         Point3(-8, 6, 0),
         Point3(-14, 6, 0)]
        self.BossOffice_SuitHs = [0,
         12,
         12,
         12,
         12,
         38]
        self.introMusic = loader.loadMusic('phase_9/audio/bgm/CHQ_FACT_bg.ogg')
        self.epilogueMusic = loader.loadMusic('phase_9/audio/bgm/CogHQ_finale.ogg')
        self.flunkyEntranceMusic = loader.loadMusic('phase_9/audio/bgm/encntr_suit_winning.ogg')
        self.waitMusic = loader.loadMusic('phase_7/audio/bgm/encntr_toon_winning_indoor.ogg')
        self.elevatorMusic = loader.loadMusic('phase_7/audio/bgm/tt_elevator.ogg')
        self.fsm = ClassicFSM.ClassicFSM('DistributedFlunkyBuildingInterior', [State.State('WaitForAllToonsInside', self.enterWaitForAllToonsInside, self.exitWaitForAllToonsInside, ['Elevator']),
         State.State('Elevator', self.enterElevator, self.exitElevator, ['Introduction', 'IntroductionBoss', 'Battle']),
         State.State('Introduction', self.enterIntroduction, self.exitIntroduction, ['Battle']),
         State.State('IntroductionBoss', self.enterIntroductionBoss, self.exitIntroductionBoss, ['Battle']),
         State.State('Battle', self.enterBattle, self.exitBattle, ['Resting', 'Reward', 'Epilogue', 'ReservesJoining']),
         State.State('ReservesJoining', self.enterReservesJoining, self.exitReservesJoining, ['Battle']),
         State.State('Resting', self.enterResting, self.exitResting, ['Elevator']),
         State.State('Epilogue', self.enterEpilogue, self.exitElevator, ['Reward']),
         State.State('Reward', self.enterReward, self.exitReward, ['Off']),
         State.State('Off', self.enterOff, self.exitOff, ['Elevator', 'WaitForAllToonsInside', 'Battle'])], 'Off', 'Off')
        self.fsm.enterInitialState()
		
    def __addToon(self, toon):
        self.accept(toon.uniqueName('disable'), self.__handleUnexpectedExit, extraArgs=[toon])

    def __handleUnexpectedExit(self, toon):
        self.notify.warning('handleUnexpectedExit() - toon: %d' % toon.doId)
        self.__removeToon(toon, unexpected=1)

    def __removeToon(self, toon, unexpected = 0):
        if self.toons.count(toon) == 1:
            self.toons.remove(toon)
        self.ignore(toon.uniqueName('disable'))

    def __finishInterval(self, name):
        if name in self.activeIntervals:
            interval = self.activeIntervals[name]
            if interval.isPlaying():
                interval.finish()

    def __cleanupIntervals(self):
        for interval in self.activeIntervals.values():
            interval.finish()

        self.activeIntervals = {}
		
    def __uniqueName(self, name):
        DistributedFlunkyBuildingInterior.id += 1
        return name + '%d' % DistributedFlunkyBuildingInterior.id
		
    def generate(self):
        DistributedObject.generate(self)
        self.announceGenerateName = self.uniqueName('generate')
        self.accept(self.announceGenerateName, self.handleAnnounceGenerate)
        self.elevatorModelIn = loader.loadModel('phase_4/models/modules/elevator')
        self.leftDoorIn = self.elevatorModelIn.find('**/left-door')
        self.rightDoorIn = self.elevatorModelIn.find('**/right-door')
        self.elevatorModelOut = loader.loadModel('phase_4/models/modules/elevator')
        self.leftDoorOut = self.elevatorModelOut.find('**/left-door')
        self.rightDoorOut = self.elevatorModelOut.find('**/right-door')
        
    def setElevatorLights(self, elevatorModel):
        cfloor = self.currentFloor - 1
        npc = elevatorModel.findAllMatches('**/floor_light_?;+s')
        for i in range(npc.getNumPaths()):
            np = npc.getPath(i)
            floor = int(np.getName()[-1:]) - 1
            if floor == cfloor:
                np.setColor(LIGHT_ON_COLOR)
            else:
                if floor < self.numFloors:
                    np.setColor(LIGHT_OFF_COLOR)
                else:
                    np.hide()
		
    def __closeInElevator(self):
        self.leftDoorIn.setPos(3.5, 0, 0)
        self.rightDoorIn.setPos(-3.5, 0, 0)
		
    def handleAnnounceGenerate(self, obj):
        self.ignore(self.announceGenerateName)
        self.sendUpdate('setAvatarJoined', [])
		
    def disable(self):
        self.fsm.requestFinalState()
        self.__cleanupIntervals()
        self.ignoreAll()
        self.__cleanup()
        DistributedObject.disable(self)

    def delete(self):
        del self.introMusic
        del self.waitMusic
        del self.elevatorMusic
        del self.epilogueMusic
        del self.flunkyEntranceMusic
        del self.openSfx
        del self.closeSfx
        del self.fsm
        base.localAvatar.inventory.setBattleCreditMultiplier(1)
        DistributedObject.delete(self)
		
    def __cleanup(self):
        self.toons = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        if self.elevatorModelIn != None:
            self.elevatorModelIn.removeNode()
        if self.elevatorModelOut != None:
            self.elevatorModelOut.removeNode()
        if self.floorModel != None:
            self.floorModel.removeNode()
        self.leftDoorIn = None
        self.rightDoorIn = None
        self.leftDoorOut = None
        self.rightDoorOut = None
        
    def setNumFloors(self, numFloors):
        self.numFloors = numFloors
		
    def setToons(self, toonIds, hack):
        self.toonIds = toonIds
        oldtoons = self.toons
        self.toons = []
        for toonId in toonIds:
            if toonId != 0:
                if toonId in self.cr.doId2do:
                    toon = self.cr.doId2do[toonId]
                    toon.stopSmooth()
                    self.toons.append(toon)
                    if oldtoons.count(toon) == 0:
                        self.__addToon(toon)
                else:
                    self.notify.warning('setToons() - no toon: %d' % toonId)
        for toon in oldtoons:
            if self.toons.count(toon) == 0:
                self.__removeToon(toon)

    def setSuits(self, suitIds, reserveIds, values):
        oldsuits = self.suits
        self.suits = []
        self.joiningReserves = []
        for suitId in suitIds:
            if suitId in self.cr.doId2do:
                suit = self.cr.doId2do[suitId]
                self.suits.append(suit)
                if self.currentFloor == 0:
                    suit.makeWaiter()
                suit.fsm.request('Battle')
                suit.buildingSuit = 1
                suit.reparentTo(render)
                if oldsuits.count(suit) == 0:
                    self.joiningReserves.append(suit)
            else:
                self.notify.warning('setSuits() - no suit: %d' % suitId)

        self.reserveSuits = []
        for index in range(len(reserveIds)):
            suitId = reserveIds[index]
            if suitId in self.cr.doId2do:
                suit = self.cr.doId2do[suitId]
                if self.currentFloor == 0:
                    suit.makeWaiter()
                self.reserveSuits.append((suit, values[index]))
            else:
                self.notify.warning('setSuits() - no suit: %d' % suitId)

        if len(self.joiningReserves) > 0:
            self.fsm.request('ReservesJoining')
			
    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def d_elevatorDone(self):
        self.sendUpdate('elevatorDone', [])
        
    def d_introductionDone(self):
        self.sendUpdate('introductionDone', [])
        
    def d_introductionBossDone(self):
        self.sendUpdate('introductionBossDone', [])

    def d_reserveJoinDone(self):
        self.sendUpdate('reserveJoinDone', [])
        
    def d_epilogueDone(self):
        self.sendUpdate('epilogueDone', [])

    def enterOff(self, ts = 0):
        pass

    def exitOff(self):
        pass

    def enterWaitForAllToonsInside(self, ts = 0):
        pass

    def exitWaitForAllToonsInside(self):
        pass
		
    def __playElevator(self, ts, name, callback):
        SuitHs = []
        SuitPositions = []
        if self.floorModel:
            self.floorModel.removeNode()
        if self.currentFloor == 1:
            self.floorModel = loader.loadModel('phase_7/models/modules/suit_interior')
            SuitHs = self.BottomFloor_SuitHs
            SuitPositions = self.BottomFloor_SuitPositions
        else:
            self.floorModel = loader.loadModel('phase_7/models/modules/boss_suit_office')
            SuitHs = self.BossOffice_SuitHs
            SuitPositions = self.BossOffice_SuitPositions
        self.floorModel.reparentTo(render)
        elevIn = self.floorModel.find('**/elevator-in')
        elevOut = self.floorModel.find('**/elevator-out')
        for index in range(len(self.suits)):
            self.suits[index].setPos(SuitPositions[index])
            if len(self.suits) > 2:
                self.suits[index].setH(SuitHs[index])
            else:
                self.suits[index].setH(170)
            self.suits[index].loop('neutral')
        for toon in self.toons:
            toon.reparentTo(self.elevatorModelIn)
            index = self.toonIds.index(toon.doId)
            toon.setPos(ElevatorPoints[index][0], ElevatorPoints[index][1], ElevatorPoints[index][2])
            toon.setHpr(180, 0, 0)
            toon.loop('neutral')
        self.elevatorModelIn.reparentTo(elevIn)
        self.leftDoorIn.setPos(3.5, 0, 0)
        self.rightDoorIn.setPos(-3.5, 0, 0)
        self.elevatorModelOut.reparentTo(elevOut)
        self.leftDoorOut.setPos(3.5, 0, 0)
        self.rightDoorOut.setPos(-3.5, 0, 0)
        camera.reparentTo(self.elevatorModelIn)
        camera.setH(180)
        camera.setPos(0, 14, 4)
        base.playMusic(self.elevatorMusic, looping=1, volume=0.8)
        track = Sequence(ElevatorUtils.getRideElevatorInterval(ELEVATOR_NORMAL), ElevatorUtils.getOpenInterval(self, self.leftDoorIn, self.rightDoorIn, self.openSfx, None, type=ELEVATOR_COG_TOWER), Func(camera.wrtReparentTo, render))
        for toon in self.toons:
            track.append(Func(toon.wrtReparentTo, render))
        track.append(Func(callback))
        track.start(ts)
        self.activeIntervals[name] = track
		
    def enterElevator(self, ts = 0):
        self.currentFloor += 1
        self.setElevatorLights(self.elevatorModelIn)
        self.setElevatorLights(self.elevatorModelOut)
        self.__playElevator(ts, self.elevatorName, self.__handleElevatorDone)
        mult = ToontownBattleGlobals.getCreditMultiplier(self.currentFloor)
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)

    def __handleElevatorDone(self):
        self.d_elevatorDone()

    def exitElevator(self):
        self.elevatorMusic.stop()
        self.__finishInterval(self.elevatorName)

    def __playCloseElevatorOut(self, name):
        track = Sequence(Wait(SUIT_LEAVE_ELEVATOR_TIME), Parallel(SoundInterval(self.closeSfx), LerpPosInterval(self.leftDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL), startPos=Point3(0, 0, 0), blendType='easeOut'), LerpPosInterval(self.rightDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL), startPos=Point3(0, 0, 0), blendType='easeOut')))
        track.start()
        self.activeIntervals[name] = track
        
    def enterIntroduction(self, ts = 0):
        base.playMusic(self.introMusic, looping=1, volume=0.7)
        suit0 = self.suits[0]
        suit1 = self.suits[1]
        suit2 = self.suits[2]
        suit3 = self.suits[3]
        
        
        track = Sequence(
          camera.posInterval(1, Point3(0, -30, 3), blendType='easeInOut'),
          Wait(1),
          Func(suit0.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroOne[0], CFSpeech),
          Wait(4),
          Func(suit0.clearChat),
          Parallel(
            ActorInterval(suit1, 'victory', startTime=0.5, endTime=1.9),
            Func(suit1.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroOne[1], CFSpeech),
          ),
          Func(suit1.loop, 'neutral'),
          Wait(4),
          Func(suit1.clearChat),
          Func(suit2.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroOne[2], CFSpeech),
          Wait(5),
          Func(suit2.clearChat),
          Func(suit3.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroOne[3], CFSpeech),
          Wait(4),
          Func(suit3.clearChat),
          Wait(1),
          Func(self.d_introductionDone)
        )
        track.start(ts)
        self.activeIntervals['introduction'] = track
  
    def exitIntroduction(self):
        self.__finishInterval('introduction')
        self.introMusic.stop()
        
    def enterIntroductionBoss(self, ts = 0):
        base.playMusic(self.introMusic, looping=1, volume=0.7)
        suit0 = self.suits[0]
        flunky = self.suits[1]
        suit2 = self.suits[2]
        suit3 = self.suits[3]
        suit4 = self.suits[4]
        
        
        track = Sequence(
          camera.posInterval(1, Point3(0, -30, 3), blendType='easeInOut'),
          Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[0], CFSpeech),
          Wait(2),
          Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[1], CFSpeech),
          Wait(4),
          Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[2], CFSpeech),
          Wait(1),
          Parallel(
            Sequence(Wait(0.5), Func(flunky.clearChat)),
            suit0.actorInterval('effort', startFrame=50),
            flunky.actorInterval('effort', startFrame=50),
            suit2.actorInterval('effort', startFrame=50),
            suit3.actorInterval('effort', startFrame=50),
            suit4.actorInterval('effort', startFrame=50),
          ),
          Parallel(
            Func(suit0.loop, 'neutral'),
            Func(flunky.loop, 'neutral'),
            Func(suit2.loop, 'neutral'),
            Func(suit3.loop, 'neutral'),
            Func(suit4.loop, 'neutral'),
          ),
          Wait(1),
          Func(suit3.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[3], CFSpeech),
          Wait(3),
          Func(suit3.clearChat),
          Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[4], CFSpeech),
          Wait(2),
          Func(flunky.clearChat),
          Parallel(
            Func(suit0.loop, 'walk'),
            Func(flunky.loop, 'walk'),
            Func(suit2.loop, 'walk'),
            Func(suit3.loop, 'walk'),
            Func(suit4.loop, 'walk'),
          ),
          Parallel(
            LerpHprInterval(suit0, 0.5, Point3(180, 0, 0), blendType='easeInOut'),
            LerpHprInterval(flunky, 0.5, Point3(180, 0, 0), blendType='easeInOut'),
            LerpHprInterval(suit2, 0.5, Point3(180, 0, 0), blendType='easeInOut'),
            LerpHprInterval(suit3, 0.5, Point3(180, 0, 0), blendType='easeInOut'),
            LerpHprInterval(suit4, 0.5, Point3(180, 0, 0), blendType='easeInOut'),
          ),        
          Parallel(
            Func(suit0.loop, 'neutral'),
            Func(flunky.loop, 'neutral'),
            Func(suit2.loop, 'neutral'),
            Func(suit3.loop, 'neutral'),
            Func(suit4.loop, 'neutral'),
          ),
          Wait(2),
          Parallel(
            camera.posInterval(1.6, Point3(0, -8, 3), blendType='easeInOut'),
            Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[5], CFSpeech)
          ),
          Wait(3),
          Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[6], CFSpeech),
          Wait(4),
          Parallel(
            ActorInterval(flunky, 'victory', startTime=0.5, endTime=1.9),
            Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[7], CFSpeech),
          ),
          Func(flunky.loop, 'neutral'),
          Wait(3),
          Parallel(
            camera.posInterval(1, Point3(0, 3, 5), blendType='easeInOut'), 
            Func(flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingIntroBoss[8], CFSpeech),
          ),
          Wait(2),
          Func(self.d_introductionBossDone)
        )
        track.start(ts)
        self.activeIntervals['introduction'] = track
  
    def exitIntroductionBoss(self):
        self.__finishInterval('introduction')
        self.introMusic.stop()
        
    def __makeTom(self):
        if self.tom:
            return
        self.tom = NPCToons.createLocalNPC(20000)
        self.tom.addActive()
        self.tom.reparentTo(self.elevatorModelOut)
        self.tom.loop('neutral')
        self.tom.setPos(0, 3, 0.1)
        self.tom.setHpr(180, 0, 0)
        self.tom.setActiveShadow(0)

    def __cleanupTom(self):
        if self.tom:
            self.tom.removeActive()
            self.tom.delete()
            self.tom = None
            
    def __makeFlunky(self):
        self.flunky = Suit()
        dna = SuitDNA()
        dna.newSuit('f')
        self.flunky.setDNA(dna)
        self.flunky.setDisplayLevel(6)
        self.flunky.reparentTo(self.elevatorModelOut)
        self.flunky.hide()
        self.flunky.loop('neutral')
        self.flunky.setPos(0, 3, 0.1)
        self.flunky.setHpr(180, 0, 0)
        
    def __cleanupFlunky(self):
        if self.flunky:
           self.flunky.clearChat()
           self.flunky.removeActive()
           self.flunky.delete()
           self.flunky = None
        
    def enterEpilogue(self, ts = 0):
        base.playMusic(self.epilogueMusic, looping=1, volume=0.7)    
    
        self.__makeTom()
        self.__makeFlunky()
        place = self.cr.playGame.getPlace()
        if place and hasattr(place, 'fsm'):
            try:
                place.setState('stopped', [0])
            except:
                pass
        camera.setH(180)
        camera.reparentTo(self.elevatorModelOut)
        track = Sequence(
          Func(camera.setPos, 0, -20, 5),
          Func(camera.headsUp, self.elevatorModelOut),
          Parallel(SoundInterval(self.openSfx), LerpPosInterval(self.leftDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL), blendType='easeOut'), LerpPosInterval(self.rightDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL), blendType='easeOut')),
          Func(self.tom.loop, 'walk'),
          Parallel(
              camera.posInterval(2, Point3(0, -30, 5), blendType='easeInOut'),
              Sequence(Wait(2), camera.posHprInterval(2, pos=(0, -60, 10), hpr=VBase3(0, -20, 0), blendType='easeInOut')),
              Sequence(LerpPosInterval(self.tom, 4, Point3(0, -35, 0.1)), Func(self.tom.loop, 'neutral')),
              Sequence(Wait(1), Parallel(SoundInterval(self.closeSfx), LerpPosInterval(self.leftDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL), startPos=Point3(0, 0, 0), blendType='easeOut'), LerpPosInterval(self.rightDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL), startPos=Point3(0, 0, 0), blendType='easeOut')))
          ),
          Func(self.tom.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[0], CFSpeech),
          ActorInterval(self.tom, 'jump'),
          Func(self.tom.loop, 'neutral'),
          Wait(1),
          Func(self.tom.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[1], CFSpeech),
          Wait(3),
          Func(self.tom.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[2], CFSpeech),
          Wait(3),
          Func(self.tom.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[3], CFSpeech),
          Wait(3),
          Func(self.tom.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[4], CFSpeech),
          Wait(0.3),
          Func(self.flunky.show),
          Func(self.flunky.addActive),
          Parallel(
            Sequence(Func(self.epilogueMusic.stop), Func(base.playMusic, self.flunkyEntranceMusic, looping=1, volume=0.7)),
            SoundInterval(self.openSfx), 
            LerpPosInterval(self.leftDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL), blendType='easeOut'), 
            LerpPosInterval(self.rightDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL), blendType='easeOut'),
            Sequence(Wait(1), Func(self.tom.clearChat), Func(self.tom.loop, 'walk'), LerpHprInterval(self.tom, 2, Point3(0, 0, 0)), Func(self.tom.loop, 'neutral'))
          ),
          Func(self.flunky.loop, 'walk'),
          LerpPosInterval(self.flunky, 4, Vec3(0, -25, 0.1)),
          Func(self.flunky.loop, 'neutral'),
          Wait(1),
          Func(self.flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[5], CFSpeech),      
          Func(self.tom.play, 'lose'),
          Wait(2),
          self.tom.scaleInterval(1.5, VBase3(0.01, 0.01, 0.01), blendType='easeInOut'),
          Func(self.__cleanupTom),
          Func(self.flunky.clearChat),
          camera.posHprInterval(2, pos=(0, -40, 5), hpr=(0, 0, 0)),
          Func(self.flunky.setChatAbsolute, TTLocalizer.FlunkyBuildingEpilogue[6], CFSpeech),
          Wait(2),
          Func(self.d_epilogueDone)
        )
        track.start(ts)
        self.activeIntervals['epilogue'] = track
  
    def exitEpilogue(self):
        self.__finishInterval('epilogue')

    def enterBattle(self, ts = 0):
        if self.elevatorOutOpen == 1:
            self.__playCloseElevatorOut(self.uniqueName('close-out-elevator'))
            camera.setPos(0, -15, 6)
            camera.headsUp(self.elevatorModelOut)

    def exitBattle(self):
        if self.elevatorOutOpen == 1:
            self.__finishInterval(self.uniqueName('close-out-elevator'))
            self.elevatorOutOpen = 0 

    def __playReservesJoining(self, ts, name, callback):
        index = 0
        for suit in self.joiningReserves:
            suit.reparentTo(render)
            suit.setPos(self.elevatorModelOut, Point3(ElevatorPoints[index][0], ElevatorPoints[index][1], ElevatorPoints[index][2]))
            index += 1
            suit.setH(180)
            suit.loop('neutral')

        track = Sequence(Func(camera.wrtReparentTo, self.elevatorModelOut), Func(camera.setPos, Point3(0, -8, 2)), Func(camera.setHpr, Vec3(0, 10, 0)), Parallel(SoundInterval(self.openSfx), LerpPosInterval(self.leftDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getLeftClosePoint(ELEVATOR_NORMAL), blendType='easeOut'), LerpPosInterval(self.rightDoorOut, ElevatorData[ELEVATOR_NORMAL]['closeTime'], Point3(0, 0, 0), startPos=ElevatorUtils.getRightClosePoint(ELEVATOR_NORMAL), blendType='easeOut')), Wait(SUIT_HOLD_ELEVATOR_TIME), Func(camera.wrtReparentTo, render), Func(callback))
        track.start(ts)
        self.activeIntervals[name] = track

    def enterReservesJoining(self, ts = 0):
        self.__playReservesJoining(ts, self.uniqueName('reserves-joining'), self.__handleReserveJoinDone)

    def __handleReserveJoinDone(self):
        self.joiningReserves = []
        self.elevatorOutOpen = 1
        self.d_reserveJoinDone()

    def exitReservesJoining(self):
        self.__finishInterval(self.uniqueName('reserves-joining'))

    def enterResting(self, ts = 0):
        base.playMusic(self.waitMusic, looping=1, volume=0.7)
        base.localAvatar.questMap.stop()
        self.__closeInElevator()

    def exitResting(self):
        self.waitMusic.stop()

    def enterReward(self, ts = 0): 
        base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        request = {'loader': 'safeZoneLoader',
         'where': 'playground',
         'how': 'teleportIn',
         'hoodId': ToontownGlobals.ToontownCentral,
         'zoneId': ToontownGlobals.ToontownCentral,
         'shardId': None,
         'avId': base.localAvatar.doId}
        messenger.send('DSIDoneEvent', [request])
        self.__cleanupFlunky()

    def exitReward(self):
        pass
        
    def getZoneId(self):
        return self.zoneId
        
    def getSuitBldgType(self):
        return 0