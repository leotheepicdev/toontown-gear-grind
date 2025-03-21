from panda3d.core import ModelPool, Texture, TexturePool
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from toontown.town import TownBattle
from toontown.building import Elevator
from direct.task.Task import Task
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals

class FlunkyBuildingInterior(Place.Place):
    notify = DirectNotifyGlobal.directNotify.newCategory('FlunkyBuildingInterior')

    def __init__(self, loader, parentFSM, doneEvent):
        Place.Place.__init__(self, loader, doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('FlunkyBuildingInterior', [State.State('entrance', self.enterEntrance, self.exitEntrance, ['battle', 'walk']),
         State.State('Elevator', self.enterElevator, self.exitElevator, ['battle', 'walk']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'died']),
         State.State('walk', self.enterWalk, self.exitWalk, ['stickerBook',
          'stopped',
          'sit',
          'died',
          'teleportOut',
          'Elevator']),
         State.State('sit', self.enterSit, self.exitSit, ['walk']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'stopped',
          'sit',
          'died',
          'DFA',
          'trialerFA',
          'teleportOut',
          'Elevator']),
         State.State('trialerFA', self.enterTrialerFA, self.exitTrialerFA, ['trialerFAReject', 'DFA']),
         State.State('trialerFAReject', self.enterTrialerFAReject, self.exitTrialerFAReject, ['walk']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walk']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'elevatorOut']),
         State.State('died', self.enterDied, self.exitDied, []),
         State.State('elevatorOut', self.enterElevatorOut, self.exitElevatorOut, [])], 'entrance', 'elevatorOut')
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = 'elevatorDoneSI'
        self.currentFloor = 0

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        self._telemLimiter = TLGatherAllAvs('FlunkyBuildingInterior', RotationLimitToH)
        self.zoneId = requestStatus['zoneId']
        self.accept('DSIDoneEvent', self.handleDSIDoneEvent)

    def exit(self):
        self.ignoreAll()
        self._telemLimiter.destroy()
        del self._telemLimiter

    def load(self):
        Place.Place.load(self)
        self.parentFSM.getStateNamed('flunkyBuildingInterior').addChild(self.fsm)
        self.townBattle = TownBattle.TownBattle('town-battle-done')
        self.townBattle.load()

    def unload(self):
        Place.Place.unload(self)
        self.parentFSM.getStateNamed('flunkyBuildingInterior').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        self.townBattle.unload()
        self.townBattle.cleanup()
        del self.townBattle

    def setState(self, state, battleEvent = None):
        if battleEvent:
            self.fsm.request(state, [battleEvent])
        else:
            self.fsm.request(state)

    def getZoneId(self):
        return self.zoneId

    def enterZone(self, zoneId):
        pass

    def handleDSIDoneEvent(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def enterEntrance(self):
        pass

    def exitEntrance(self):
        pass

    def enterElevator(self, distElevator):
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('Elevator'), self.elevatorDoneEvent, distElevator)
        self.elevator.load()
        self.elevator.enter()
        base.localAvatar.cantLeaveGame = 1

    def exitElevator(self):
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('Elevator', [distElevator])

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'flunkyBuildingInterior':
            pass
        elif where == 'suitInterior': # HACK
            pass
        else:
            self.notify.error('Unknown mode: %s in handleElevatorDone' % where)

    def enterBattle(self, event):
        self.enterFLM(battle=True)
        mult = ToontownBattleGlobals.getCreditMultiplier(self.currentFloor)
        self.townBattle.enter(event, self.fsm.getStateNamed('battle'), bldg=1, creditMultiplier=mult)
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.cantLeaveGame = 1

    def exitBattle(self):
        self.exitFLM(battle=True)
        self.townBattle.exit()
        base.localAvatar.cantLeaveGame = 0

    def enterWalk(self, teleportIn = 0):
        Place.Place.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterStickerBook(self, page = None):
        Place.Place.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterSit(self):
        Place.Place.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterStopped(self, disableEmotes=0):
        Place.Place.enterStopped(self, disableEmotes)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterTeleportIn(self, requestStatus):
        base.localAvatar.setPosHpr(2.5, 11.5, ToontownGlobals.FloorOffset, 45.0, 0.0, 0.0)
        Place.Place.enterTeleportIn(self, requestStatus)

    def enterTeleportOut(self, requestStatus):
        Place.Place.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        if hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            messenger.send('localToonLeft')
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def exitTeleportOut(self):
        Place.Place.exitTeleportOut(self)

    def goHomeFailed(self, task):
        self.notifyUserGoHomeFailed()
        self.ignore('setLocalEstateZone')
        self.doneStatus['avId'] = -1
        self.doneStatus['zoneId'] = self.getZoneId()
        self.fsm.request('teleportIn', [self.doneStatus])
        return Task.done

    def enterElevatorOut(self):
        pass

    def __elevatorOutDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def exitElevatorOut(self):
        pass
