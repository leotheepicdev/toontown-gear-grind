from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.ai.DistributedBlackCatMgrAI import DistributedBlackCatMgrAI, BlackCatDayHolidayAI
from toontown.building import DoorTypes, FADoorCodes
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI
from toontown.building.HQBuildingAI import HQBuildingAI
from toontown.quest import Quests
from toontown.suit.DistributedTutorialSuitAI import DistributedTutorialSuitAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer, ToontownBattleGlobals

class TutorialInstance:

    def __init__(self, air):
        self.air = air

        # Generate our tutorial zones.
        self.streetZone = self.air.allocateZone()
        self.shopZone = self.air.allocateZone()
        self.hqZone = self.air.allocateZone()

        # Generate our shop.
        self.tutorialTom = NPCToons.createNPC(self.air, 20000, NPCToons.NPCToonDict.get(20000), self.shopZone, 0)
        self.tutorialTom.setTutorial(1)
        self.interior = DistributedTutorialInteriorAI(self.air, self.shopZone, self.tutorialTom.doId)
        self.interior.generateWithRequired(self.shopZone)
        self.exteriorShopDoor = DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD, doorIndex=0)
        self.exteriorShopDoor.generateWithRequired(self.streetZone)
        self.interiorShopDoor = DistributedDoorAI(self.air, 0, DoorTypes.INT_STANDARD, doorIndex=0)
        self.interiorShopDoor.setDoorLock(FADoorCodes.TALK_TO_TOM)
        self.interiorShopDoor.generateWithRequired(self.shopZone)
        self.exteriorShopDoor.setOtherDoor(self.interiorShopDoor)
        self.interiorShopDoor.setOtherDoor(self.exteriorShopDoor)

        # Generate our HQ.
        self.hqHarry = NPCToons.createNPC(self.air, 20002, NPCToons.NPCToonDict.get(20002), self.hqZone, 0)
        self.hqHarry.setTutorial(1)
        self.hqBuilding = HQBuildingAI(self.air, self.streetZone, self.hqZone, 1)

        # Leave our suit variable here.
        self.suit = None

        # Leave our flippy variable here.
        self.flippy = None

    def cleanup(self):
        if self.tutorialTom:
            self.tutorialTom.requestDelete()
        del self.tutorialTom
        self.interior.requestDelete()
        del self.interior
        self.exteriorShopDoor.requestDelete()
        del self.exteriorShopDoor
        self.interiorShopDoor.requestDelete()
        del self.interiorShopDoor
        if self.suit:
            self.suit.requestDelete()
        del self.suit
        if self.hqHarry:
            self.hqHarry.requestDelete()
        del self.hqHarry
        self.hqBuilding.cleanup()
        del self.hqBuilding
        if self.flippy:
            self.flippy.requestDelete()
        del self.flippy
        self.air.deallocateZone(self.streetZone)
        self.air.deallocateZone(self.shopZone)
        self.air.deallocateZone(self.hqZone)

    def getZones(self):
        return self.streetZone, self.streetZone, self.shopZone, self.hqZone

    def preparePlayerForBattle(self):
        self.interiorShopDoor.setDoorLock(FADoorCodes.UNLOCKED)

        # Generate our suit
        self.suit = DistributedTutorialSuitAI(self.air)
        self.suit.createSuit('f', 1)
        self.suit.generateWithRequired(self.streetZone)

        # Lock our doors
        self.exteriorShopDoor.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_TOM)
        self.hqBuilding.door0.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_HQ)

    def preparePlayerForHQ(self):
        if self.suit:
            self.suit.requestDelete()
        self.suit = None
        self.tutorialTom.requestDelete()
        self.tutorialTom = None
        self.exteriorShopDoor.setDoorLock(FADoorCodes.TALK_TO_HQ_TOM)
        self.hqBuilding.door0.setDoorLock(FADoorCodes.UNLOCKED)
        self.hqBuilding.insideDoor0.setDoorLock(FADoorCodes.TALK_TO_HQ)
        self.hqBuilding.insideDoor1.setDoorLock(FADoorCodes.TALK_TO_HQ)

    def preparePlayerForTunnel(self):
        self.flippy = NPCToons.createNPC(self.air, 20001, NPCToons.NPCToonDict.get(20001), self.streetZone, 0)
        self.hqBuilding.insideDoor1.setDoorLock(FADoorCodes.UNLOCKED)
        self.hqBuilding.door1.setDoorLock(FADoorCodes.GO_TO_PLAYGROUND)
        self.hqBuilding.insideDoor0.setDoorLock(FADoorCodes.WRONG_DOOR_HQ)

class TutorialManagerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.playerDict = {}

    def cleanup(self, avId):
        if avId in self.playerDict:
            self.playerDict[avId].cleanup()
            del self.playerDict[avId]

    def requestTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return
        if avId in self.playerDict:
            self.air.writeServerEvent('suspicious', avId, 'Attempted to request tutorial, but we are already in one.')
            return
        self.playerDict[avId] = TutorialInstance(self.air)
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.cleanup, extraArgs=[avId])
        branchZone, streetZone, shopZone, hqZone = self.playerDict[avId].getZones()
        self.sendUpdateToAvatarId(avId, 'enterTutorial', [branchZone, streetZone, shopZone, hqZone])

    def requestSkipTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.playerDict:
            return
        av = self.air.doId2do.get(avId)
        if av:
            if av.getTutorialAck() == 1:
                self.air.writeServerEvent('suspicious', avId, 'Attempted to skip tutorial, but we already went through it.')
                return
            av.b_setTutorialAck(1)
            av.b_setQuests([[110, 1, 1000, 100, 1]])
            av.b_setQuestHistory([101])
            av.b_setRewardHistory(1, [])
            self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [1])
        else:
            self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [0])

    def allDone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            av.b_setTutorialAck(1)
        self.cleanup(avId)
        self.ignore(self.air.getAvatarExitEvent(avId))

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if av.getTutorialAck():
            self.cleanup(avId)
            self.air.moderationManager.serverKick(avId, 'Attempted to request tutorial, but already went through it.')
            return

        # Modify the stats of our Toon so that we are able to pass the tutorial.
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])
        av.b_setHp(15)
        av.b_setMaxHp(15)

        av.inventory.zeroInv()
        if av.inventory.numItem(ToontownBattleGlobals.THROW_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.THROW_TRACK, 0)

        if av.inventory.numItem(ToontownBattleGlobals.SQUIRT_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.SQUIRT_TRACK, 0)

        av.d_setInventory(av.inventory.makeNetString())
        av.experience.zeroOutExp()
        av.d_setExperience(av.experience.makeNetString())