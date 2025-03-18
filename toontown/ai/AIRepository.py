from panda3d.core import UniqueIdAllocator, CSDefault

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed import MsgTypes

from otp.distributed import OtpDoGlobals
from otp.ai.AIZoneData import AIZoneDataStore
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.ai.BanManagerAI import BanManagerAI
from otp.ai.ModerationManagerAI import ModerationManagerAI
from otp.chat.ChatRelayAI import ChatRelayAI
from otp.friends.FriendManagerAI import FriendManagerAI

from toontown.building.CogBuildingManagerAI import CogBuildingManagerAI

from toontown.distributed.InternalRepository import InternalRepository
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from toontown.ai.HolidayManagerAI import HolidayManagerAI
from toontown.catalog.CatalogManagerAI import CatalogManagerAI
from toontown.ai.WelcomeValleyManagerAI import WelcomeValleyManagerAI
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import NPCToons

from toontown.hood.TTHoodDataAI import TTHoodDataAI
from toontown.hood.DDHoodDataAI import DDHoodDataAI
from toontown.hood.OZHoodDataAI import OZHoodDataAI
from toontown.hood.GZHoodDataAI import GZHoodDataAI
from toontown.hood.DGHoodDataAI import DGHoodDataAI
from toontown.hood.WWHoodDataAI import WWHoodDataAI
from toontown.hood.MMHoodDataAI import MMHoodDataAI
from toontown.hood.BRHoodDataAI import BRHoodDataAI
from toontown.hood.DLHoodDataAI import DLHoodDataAI
from toontown.hood.CSHoodDataAI import CSHoodDataAI
from toontown.hood.CashbotHQDataAI import CashbotHQDataAI
from toontown.hood.LawbotHQDataAI import LawbotHQDataAI
from toontown.hood.BossbotHQDataAI import BossbotHQDataAI
from toontown.hood.GSHoodDataAI import GSHoodDataAI
from toontown.hood.OZHoodDataAI import OZHoodDataAI
from toontown.hood.GZHoodDataAI import GZHoodDataAI
from toontown.hood.RRHHoodDataAI import RRHHoodDataAI

from toontown.hood.DaylightManagerAI import DaylightManagerAI

from toontown.hood import ZoneUtil
from toontown.building import CogBuildingGlobalsAI
from toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from toontown.pets.PetManagerAI import PetManagerAI
from toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI
from toontown.ai.NewsManagerAI import NewsManagerAI
from toontown.estate.EstateManagerAI import EstateManagerAI

from toontown.safezone.SafeZoneManagerAI import SafeZoneManagerAI
from toontown.safezone.DistributedPartyGateAI import DistributedPartyGateAI

from toontown.uberdog.DistributedInGameNewsMgrAI import DistributedInGameNewsMgrAI
from toontown.fishing.FishManagerAI import FishManagerAI
from toontown.fishing.FishBingoManagerAI import FishBingoManagerAI

from toontown.coghq.FactoryManagerAI import FactoryManagerAI
from toontown.coghq.MintManagerAI import MintManagerAI
from toontown.coghq.LawOfficeManagerAI import LawOfficeManagerAI
from toontown.coghq.CountryClubManagerAI import CountryClubManagerAI
from toontown.coghq.PromotionManagerAI import PromotionManagerAI
from toontown.coghq.CogSuitManagerAI import CogSuitManagerAI

from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing import RaceGlobals
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI, DistributedViewingBlockAI
from toontown.racing.DistributedLeaderBoardAI import DistributedLeaderBoardAI
from toontown.racing.RaceManagerAI import RaceManagerAI

from toontown.mwparser.MagicWordManagerAI import MagicWordManagerAI
from toontown.mwparser.MagicWordDispatcher import MagicWordDispatcher

from toontown.parties.ToontownTimeManager import ToontownTimeManager

from toontown.quest.QuestManagerAI import QuestManagerAI

from toontown.tutorial.TutorialManagerAI import TutorialManagerAI

from panda3d.toontown import DNAStorage, loadDNAFileAI, DNAGroup, DNAVisGroup

from toontown.ai.CogPageManagerAI import CogPageManagerAI

from toontown.coderedemption.TTCodeRedemptionMgrAI import TTCodeRedemptionMgrAI

from toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI

from toontown.ai.DistributedResistanceEmoteMgrAI import DistributedResistanceEmoteMgrAI
from toontown.ai.DistributedPolarPlaceEffectMgrAI import DistributedPolarPlaceEffectMgrAI

import os, time, random

class AIRepository(InternalRepository):
    notify = directNotify.newCategory('AIRepository')

    GameGlobalsId = OtpDoGlobals.OTP_DO_ID_TOONTOWN

    def __init__(self, baseChannel, stateServerChannel, districtName, wantRandomInvasions, isInvasionOnly):
        InternalRepository.__init__(self, baseChannel, stateServerChannel, dcSuffix = 'AI')

        self.districtName = districtName
        self.wantRandomInvasions = wantRandomInvasions
        self.isInvasionOnly = isInvasionOnly

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin, ToontownGlobals.DynamicZonesEnd)

        self.zoneDataStore = AIZoneDataStore()

        # Dictionaries:
        self.hoods = []
        self.zoneTable = {}
        self.cogHeadquarters = []
        self.dnaStoreMap = {}
        self.dnaDataMap = {}
        self.suitPlanners = {}
        self.buildingManagers = {}
        self.zoneId2owner = {}

        # What we want to have on the server:
        self.wantCogdominiums = config.GetBool('want-cogdominiums', True)
        self.wantUndergroundBldgs = config.GetBool('want-underground-bldgs', False)
        self.useAllMinigames = config.GetBool('use-all-minigames', False)
        self.wantCodeRedemption = config.GetBool('want-coderedemption', True)

        self.notify.setInfo(True)

        self.mwDispatcher = MagicWordDispatcher()

        # Let them know the AI is starting up:
        self.notify.info('District {0} is now starting up.'.format(districtName))

    def handleConnected(self):
        InternalRepository.handleConnected(self)

        self.districtId = self.allocateChannel()

        self.distributedDistrict = ToontownDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.generateWithRequiredAndId(self.districtId, self.getGameDoId(), OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)
        self.setAI(self.districtId, self.ourChannel)

        self.districtStats = ToontownDistrictStatsAI(self)
        self.districtStats.settoontownDistrictId(self.districtId)
        self.districtStats.generateWithRequiredAndId(self.allocateChannel(), self.getGameDoId(), OtpDoGlobals.OTP_ZONE_ID_DISTRICTS)

        self.notify.info('Generating managers...')
        self.generateManagers()

        self.notify.info('Creating zones...')
        self.createZones()

        if self.wantRandomInvasions:
            self.suitInvasionManager.startRandomInvasionTick()
        if self.isInvasionOnly:
            self.suitInvasionManager.generateRandomInvasion()

        self.fishManager.generateDailyCatch()
        self.bldgMgr.assignInitialCogBuildings()

        self.distributedDistrict.b_setAvailable(1)
        self.notify.info('District (AI) {0} is now ready.'.format(self.districtName))

    def createHood(self, hoodCtr, zoneId):
        # Bossbot HQ doesn't use DNA, so we skip over that.
        if zoneId != ToontownGlobals.BossbotHQ:
            self.dnaStoreMap[zoneId] = DNAStorage()
            self.dnaDataMap[zoneId] = self.loadDNAFileAI(self.dnaStoreMap[zoneId], self.genDNAFileName(zoneId))
            if zoneId in ToontownGlobals.HoodHierarchy:
                for streetId in ToontownGlobals.HoodHierarchy[zoneId]:
                    self.dnaStoreMap[streetId] = DNAStorage()
                    self.dnaDataMap[streetId] = self.loadDNAFileAI(self.dnaStoreMap[streetId], self.genDNAFileName(streetId))

        hood = hoodCtr(self, zoneId)
        hood.startup()
        self.hoods.append(hood)

    def createZones(self):
        # First, generate our zone2NpcDict...
        NPCToons.generateZone2NpcDict()

        # If enabled, create our main playgrounds:
        if config.GetBool('want-main-playgrounds', True):
            self.createMainPlaygrounds()

        # If enabled, create our Cog HQs:
        if config.GetBool('want-cog-headquarters', True):
            self.createCogHeadquarters()

        # If enabled, create our other playgrounds:
        if config.GetBool('want-other-playgrounds', True):
            self.createMiscPlaygrounds()

    def createMainPlaygrounds(self):
        # Toontown Central
        self.zoneTable[ToontownGlobals.ToontownCentral] = (
            (ToontownGlobals.ToontownCentral, 1, 0), (ToontownGlobals.SillyStreet, 1, 1),
            (ToontownGlobals.LoopyLane, 1, 1),
            (ToontownGlobals.PunchlinePlace, 1, 1)
        )
        self.createHood(TTHoodDataAI, ToontownGlobals.ToontownCentral)

        # Donald's Dock
        self.zoneTable[ToontownGlobals.DonaldsDock] = (
            (ToontownGlobals.DonaldsDock, 1, 0), (ToontownGlobals.BarnacleBoulevard, 1, 1),
            (ToontownGlobals.SeaweedStreet, 1, 1), (ToontownGlobals.LighthouseLane, 1, 1)
        )
        self.createHood(DDHoodDataAI, ToontownGlobals.DonaldsDock)

        # Daisy Gardens
        self.zoneTable[ToontownGlobals.DaisyGardens] = (
            (ToontownGlobals.DaisyGardens, 1, 0), (ToontownGlobals.ElmStreet, 1, 1),
            (ToontownGlobals.MapleStreet, 1, 1), (ToontownGlobals.OakStreet, 1, 1)
        )
        self.createHood(DGHoodDataAI, ToontownGlobals.DaisyGardens)

        # Minnie's Melodyland
        self.zoneTable[ToontownGlobals.MinniesMelodyland] = (
            (ToontownGlobals.MinniesMelodyland, 1, 0), (ToontownGlobals.AltoAvenue, 1, 1),
            (ToontownGlobals.BaritoneBoulevard, 1, 1), (ToontownGlobals.TenorTerrace, 1, 1)
        )
        self.createHood(MMHoodDataAI, ToontownGlobals.MinniesMelodyland)

        # The Brrrgh
        self.zoneTable[ToontownGlobals.TheBrrrgh] = (
            (ToontownGlobals.TheBrrrgh, 1, 0), (ToontownGlobals.WalrusWay, 1, 1),
            (ToontownGlobals.SleetStreet, 1, 1), (ToontownGlobals.PolarPlace, 1, 1)
        )
        self.createHood(BRHoodDataAI, ToontownGlobals.TheBrrrgh)

        # Donald's Dreamland
        self.zoneTable[ToontownGlobals.DonaldsDreamland] = (
            (ToontownGlobals.DonaldsDreamland, 1, 0), (ToontownGlobals.LullabyLane, 1, 1),
            (ToontownGlobals.PajamaPlace, 1, 1)
        )
        self.createHood(DLHoodDataAI, ToontownGlobals.DonaldsDreamland)

        # Wacky West
        self.zoneTable[ToontownGlobals.WackyWest] = (
            (ToontownGlobals.WackyWest, 1, 0),
        )
        self.createHood(WWHoodDataAI, ToontownGlobals.WackyWest)

    def createCogHeadquarters(self):
        # Sellbot HQ
        self.zoneTable[ToontownGlobals.SellbotHQ] = (
            (ToontownGlobals.SellbotHQ, 0, 1), (ToontownGlobals.SellbotFactoryExt, 0, 1)
        )
        self.createHood(CSHoodDataAI, ToontownGlobals.SellbotHQ)

        # Cashbot HQ
        self.zoneTable[ToontownGlobals.CashbotHQ] = (
            (ToontownGlobals.CashbotHQ, 0, 1),
        )
        self.createHood(CashbotHQDataAI, ToontownGlobals.CashbotHQ)

        # Lawbot HQ
        self.zoneTable[ToontownGlobals.LawbotHQ] = (
            (ToontownGlobals.LawbotHQ, 0, 1),
        )
        self.createHood(LawbotHQDataAI, ToontownGlobals.LawbotHQ)

        # Bossbot HQ
        self.zoneTable[ToontownGlobals.BossbotHQ] = (
            (ToontownGlobals.BossbotHQ, 0, 0),
        )
        self.createHood(BossbotHQDataAI, ToontownGlobals.BossbotHQ)

    def createMiscPlaygrounds(self):
        # Goofy Speedway
        self.zoneTable[ToontownGlobals.GoofySpeedway] = (
            (ToontownGlobals.GoofySpeedway, 1, 0),
        )
        self.createHood(GSHoodDataAI, ToontownGlobals.GoofySpeedway)

        # Chip 'n Dale's Acorn Acres
        self.zoneTable[ToontownGlobals.OutdoorZone] = (
            (ToontownGlobals.OutdoorZone, 1, 0),
        )
        self.createHood(OZHoodDataAI, ToontownGlobals.OutdoorZone)

        # Chip 'n Dale's MiniGolf
        self.zoneTable[ToontownGlobals.GolfZone] = (
            (ToontownGlobals.GolfZone, 1, 0),
        )
        self.createHood(GZHoodDataAI, ToontownGlobals.GolfZone)

        # Resistance Ranger Hideout
        self.zoneTable[ToontownGlobals.ResistanceRangerHideout] = (
            (ToontownGlobals.ResistanceRangerHideout, 1, 0),
        )
        self.createHood(RRHHoodDataAI, ToontownGlobals.ResistanceRangerHideout)

        # Welcome Valley hoods (Toontown Central & Goofy Speedway)
        self.notify.info('Creating ' + TTLocalizer.WelcomeValley[2] + ' hoods...')

        # Welcome Valley, Toontown Central
        self.createHood(TTHoodDataAI, ToontownGlobals.WelcomeValleyBegin)

        # Welcome Valley, Goofy Speedway
        self.createHood(GSHoodDataAI, ToontownGlobals.WelcomeValleyGoofySpeedway)

    def loadDNAFileAI(self, dnaStore, dnaFileName):
        return loadDNAFileAI(dnaStore, dnaFileName, CSDefault)

    def genDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phase = ToontownGlobals.phaseMap[hoodId]
        else:
            phase = ToontownGlobals.streetPhaseMap[hoodId]

        if 'outdoor_zone' in hood or 'golf_zone' in hood:
            phase = '6'

        return 'phase_{0}/dna/{1}_{2}.dna'.format(phase, hood, zoneId)

    def lookupDNAFileName(self, dnaFileName):
        for _ in range(3, 13):
            if os.path.exists('resources/phase_{0}/dna/{1}'.format(_, dnaFileName)):
                return 'phase_{0}/dna/{1}'.format(_, dnaFileName)

    def findFishingPonds(self, dnaData, zoneId, area):
        fishingPonds = []
        fishingPondGroups = []
        if isinstance(dnaData, DNAGroup) and 'fishing_pond' in dnaData.getName():
            fishingPondGroups.append(dnaData)
            pond = self.fishManager.generatePond(area, zoneId)
            fishingPonds.append(pond)
        else:
            if isinstance(dnaData, DNAVisGroup):
                zoneId = ZoneUtil.getTrueZoneId(int(dnaData.getName().split(':')[0]), zoneId)
        for i in range(dnaData.getNumChildren()):
            foundFishingPonds, foundFishingPondGroups = self.findFishingPonds(dnaData.at(i), zoneId, area)
            fishingPonds.extend(foundFishingPonds)
            fishingPondGroups.extend(foundFishingPondGroups)

        return (fishingPonds, fishingPondGroups)

    def findFishingSpots(self, dnaData, fishingPond):
        fishingSpots = []
        if isinstance(dnaData, DNAGroup) and dnaData.getName()[:13] == 'fishing_spot_':
            spot = self.fishManager.generateSpots(dnaData, fishingPond)
            fishingSpots.append(spot)
        for i in range(dnaData.getNumChildren()):
            foundFishingSpots = self.findFishingSpots(dnaData.at(i), fishingPond)
            fishingSpots.extend(foundFishingSpots)

        return fishingSpots

    def findRacingPads(self, dnaData, zoneId, area, type = 'racing_pad', overrideDNAZone = False):
        racingPads, racingPadGroups = [], []
        if type in dnaData.getName():
            if type == 'racing_pad':
                nameSplit = dnaData.getName().split('_')
                racePad = DistributedRacePadAI(self)
                racePad.setArea(area)
                racePad.index = int(nameSplit[2])
                racePad.genre = nameSplit[3]
                trackInfo = RaceGlobals.getNextRaceInfo(-1, racePad.genre, racePad.index)
                racePad.setTrackInfo([trackInfo[0], trackInfo[1]])
                racePad.laps = trackInfo[2]
                racePad.generateWithRequired(zoneId)
                racingPads.append(racePad)
                racingPadGroups.append(dnaData)
            elif type == 'viewing_pad':
                viewPad = DistributedViewPadAI(self)
                viewPad.setArea(area)
                viewPad.generateWithRequired(zoneId)
                racingPads.append(viewPad)
                racingPadGroups.append(dnaData)
        for i in range(dnaData.getNumChildren()):
            foundRacingPads, foundRacingPadGroups = self.findRacingPads(dnaData.at(i), zoneId, area, type, overrideDNAZone)
            racingPads.extend(foundRacingPads)
            racingPadGroups.extend(foundRacingPadGroups)

        return (racingPads, racingPadGroups)

    def findStartingBlocks(self, dnaData, pad):
        startingBlocks = []
        for i in range(dnaData.getNumChildren()):
            groupName = dnaData.getName()
            blockName = dnaData.at(i).getName()
            if 'starting_block' in blockName:
                cls = DistributedStartingBlockAI if 'racing_pad' in groupName else DistributedViewingBlockAI
                x, y, z = dnaData.at(i).getPos()
                h, p, r = dnaData.at(i).getHpr()
                padLocationId = int(dnaData.at(i).getName()[(-1)])
                startingBlock = cls(self, pad, x, y, z, h, p, r, padLocationId)
                startingBlock.generateWithRequired(pad.zoneId)
                startingBlocks.append(startingBlock)

        return startingBlocks

    def findLeaderBoards(self, dnaData, zoneId):
        leaderboards = []
        if 'leaderBoard' in dnaData.getName():
            x, y, z = dnaData.getPos()
            h, p, r = dnaData.getHpr()
            leaderboard = DistributedLeaderBoardAI(self, dnaData.getName(), x, y, z, h, p, r)
            leaderboard.generateWithRequired(zoneId)
            leaderboards.append(leaderboard)
        for i in range(dnaData.getNumChildren()):
            foundLeaderBoards = self.findLeaderBoards(dnaData.at(i), zoneId)
            leaderboards.extend(foundLeaderBoards)

        return leaderboards

    def findPartyHats(self, dnaData, zoneId):
        partyHats = []
        if 'prop_party_gate' in dnaData.getName():
            partyHat = DistributedPartyGateAI(self)
            partyHat.generateWithRequired(zoneId)
            partyHats.append(partyHat)

        for i in range(dnaData.getNumChildren()):
            foundPartyHats = self.findPartyHats(dnaData.at(i), zoneId)
            partyHats.extend(foundPartyHats)

        return partyHats

    def generateManagers(self):
        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.chatRelay = ChatRelayAI(self)
        self.chatRelay.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.holidayManager = HolidayManagerAI(self)
        self.catalogManager = CatalogManagerAI(self)
        self.welcomeValleyManager = WelcomeValleyManagerAI(self)
        self.welcomeValleyManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.bldgMgr = CogBuildingManagerAI(self)

        self.trophyMgr = DistributedTrophyMgrAI(self)
        self.trophyMgr.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_OLD_QUIET_ZONE)

        self.petMgr = PetManagerAI(self)
        self.suitInvasionManager = SuitInvasionManagerAI(self)

        self.newsManager = NewsManagerAI(self)
        self.newsManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)
        self.estateMgr = EstateManagerAI(self)
        self.estateMgr.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)
        self.safeZoneManager = SafeZoneManagerAI(self)
        self.safeZoneManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.inGameNewsMgr = DistributedInGameNewsMgrAI(self)
        self.inGameNewsMgr.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.fishManager = FishManagerAI(self)

        self.factoryMgr = FactoryManagerAI(self)
        self.mintMgr = MintManagerAI(self)
        self.lawMgr = LawOfficeManagerAI(self)
        self.countryClubMgr = CountryClubManagerAI(self)
        self.raceMgr = RaceManagerAI(self)

        self.magicWordMgr = MagicWordManagerAI(self)
        self.magicWordMgr.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.toontownTimeManager = ToontownTimeManager(serverTimeUponLogin = int(time.time()), globalClockRealTimeUponLogin = globalClock.getRealTime())

        self.banManager = BanManagerAI() # TODO: remove me
        self.moderationManager = ModerationManagerAI(self)

        self.questManager = QuestManagerAI(self)

        self.tutorialManager = TutorialManagerAI(self)
        self.tutorialManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.promotionMgr = PromotionManagerAI(self)

        self.cogPageManager = CogPageManagerAI(self)

        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.deliveryManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')

        self.codeRedemptionMgr = TTCodeRedemptionMgrAI(self)
        self.codeRedemptionMgr.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.centralLogger = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')

        self.partyManager = DistributedPartyManagerAI(self)
        self.partyManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

        self.cogSuitMgr = CogSuitManagerAI(self)

        self.fishBingoManager = FishBingoManagerAI(self)

        self.resistanceEmoteMgr = DistributedResistanceEmoteMgrAI(self)
        self.resistanceEmoteMgr.generateWithRequired(9720)

        self.polarPlaceEffectMgr = DistributedPolarPlaceEffectMgrAI(self)
        self.polarPlaceEffectMgr.generateWithRequired(3821)

        self.daylightManager = DaylightManagerAI(self)
        self.daylightManager.generateWithRequired(OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT)

    def doLiveUpdates(self):
        if config.GetBool('want-do-live-updates', False):
            return True

        return False

    def incrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() + 1)

    def decrementPopulation(self):
        self.districtStats.b_setAvatarCount(self.districtStats.getAvatarCount() - 1)

    def updateDistrictPopLimits(self, districtPopLimits):
        self.distributedDistrict.b_setDistrictPopLimits(districtPopLimits)

    def sendQueryToonMaxHp(self, doId, checkResult):
        self.notify.info('sendQueryToonMaxHp ({0}, {1})'.format(doId, checkResult))

    def _isValidPlayerLocation(self, parentId, zoneId):
        if not parentId or zoneId > ToontownGlobals.DynamicZonesEnd or zoneId == 0:
            return False

        return True

    def getZoneDataStore(self):
        return self.zoneDataStore

    def getAvatarExitEvent(self, doId):
        return 'distObjDelete-{0}'.format(doId)

    def sendSetZone(self, obj, zoneId):
        obj.b_setLocation(obj.parentId, zoneId)

    def allocateZone(self, owner = None):
        zoneId = self.zoneAllocator.allocate()

        if owner:
            self.zoneId2owner[zoneId] = owner

        return zoneId

    def deallocateZone(self, zone):
        if self.zoneId2owner.get(zone):
            del self.zoneId2owner[zone]

        self.zoneAllocator.free(zone)

    def getAvatarDisconnectReason(self, avId):
        return self.timeManager.avId2disconnectcode.get(avId, ToontownGlobals.DisconnectUnknown)

    def trueUniqueName(self, idString):
        return self.uniqueName(idString)