from .DistributedNPCToonBase import DistributedNPCToonBase
from direct.distributed.DistributedObject import DistributedObject
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task
from direct.distributed import ClockDelta
from panda3d.core import Point3
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.parties import PartyGlobals
from lib.libotp._constants import CFSpeech, CFTimeout
from panda3d.core import Quat

class DistributedNPCPartyPerson(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.av = None
        self.button = None
        self.askGui = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupAskGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def delete(self):
        if self.askGui:
            self.ignore(self.planPartyQuestionGuiDoneEvent)
            self.askGui.cleanup()
            del self.askGui
        DistributedNPCToonBase.delete(self)

    def generate(self):
        DistributedNPCToonBase.generate(self)

    def announceGenerate(self):
        DistributedNPCToonBase.announceGenerate(self)
        self.planPartyQuestionGuiDoneEvent = 'planPartyQuestionDone'
        self.askGui = TTDialog.TTGlobalDialog(dialogName=self.uniqueName('askGui'), doneEvent=self.planPartyQuestionGuiDoneEvent, message=TTLocalizer.PartyDoYouWantToPlan, style=TTDialog.YesNo, okButtonText=OTPLocalizer.DialogYes, cancelButtonText=OTPLocalizer.DialogNo)
        self.askGui.hide()

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        if self.posIndex % 2 == 0:
            side = 'left'
        else:
            side = 'right'
        npcOrigin = self.cr.playGame.hood.loader.geom.find('**/party_person_%s;+s' % side)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning('announceGenerate: Could not find party_person_%s' % side)
        return

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def setupAvatars(self, av):
        self.ignoreAvatars()
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def resetPartyPerson(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupAskGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.askGui:
            self.askGui.hide()
        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PARTY_MOVIE_CLEAR:
            return
        if mode == NPCToons.PARTY_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignore(self.planPartyQuestionGuiDoneEvent)
                if self.askGui:
                    self.askGui.hide()
                    self.ignore(self.planPartyQuestionGuiDoneEvent)
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        elif mode == NPCToons.PARTY_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                quat = Quat()
                quat.setHpr((-150, -2, 0))
                camera.posQuatInterval(1, Point3(-5, 9, base.localAvatar.getHeight() - 0.5), quat, other=self, blendType='easeOut').start()
                taskMgr.doMethodLater(1.0, self.popupAskGUI, self.uniqueName('popupAskGUI'))
            else:
                self.setChatAbsolute(TTLocalizer.PartyDoYouWantToPlan, CFSpeech | CFTimeout)
        elif mode == NPCToons.PARTY_MOVIE_COMPLETE:
            chatStr = TTLocalizer.PartyPlannerOnYourWay
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
            if self.isLocalToon:
                base.localAvatar.aboutToPlanParty = True
                base.cr.partyManager.setPartyPlannerStyle(self.style)
                base.cr.partyManager.setPartyPlannerName(self.name)
                base.localAvatar.creatingNewPartyWithMagicWord = False
                loaderId = 'safeZoneLoader'
                whereId = 'party'
                hoodId, zoneId = extraArgs
                avId = -1
                place = base.cr.playGame.getPlace()
                requestStatus = {'loader': loaderId,
                 'where': whereId,
                 'how': 'teleportIn',
                 'hoodId': hoodId,
                 'zoneId': zoneId,
                 'shardId': None,
                 'avId': avId}
                place.requestLeave(requestStatus)
        elif mode == NPCToons.PARTY_MOVIE_MAYBENEXTTIME:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.setChatAbsolute(TTLocalizer.PartyPlannerMaybeNextTime, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        elif mode == NPCToons.PARTY_MOVIE_ALREADYHOSTING:
            chatStr = TTLocalizer.PartyPlannerHostingTooMany
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        elif mode == NPCToons.PARTY_MOVIE_COMINGSOON:
            chatStr = TTLocalizer.PartyPlannerNpcComingSoon
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        elif mode == NPCToons.PARTY_MOVIE_MINCOST:
            chatStr = TTLocalizer.PartyPlannerNpcMinCost % PartyGlobals.MinimumPartyCost
            self.setChatAbsolute(chatStr, CFSpeech | CFTimeout)
            self.resetPartyPerson()
        return

    def __handleAskDone(self):
        self.ignore(self.planPartyQuestionGuiDoneEvent)
        doneStatus = self.askGui.doneStatus
        if doneStatus == 'ok':
            wantsToPlan = 1
        else:
            wantsToPlan = 0
        self.sendUpdate('answer', [wantsToPlan])
        self.askGui.hide()

    def popupAskGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.planPartyQuestionGuiDoneEvent, self.__handleAskDone)
        self.askGui.show()