from direct.distributed.DistributedObjectAI import DistributedObjectAI
from .MagicWordGlobals import *
from .MagicWordLocalizer import ResponseCode2String
from direct.showbase.PythonUtil import describeException
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from toontown.shtiker import CogPageGlobals
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.coghq import CogDisguiseGlobals
from toontown.toon import ToonDNA
from toontown.suit import SuitDNA
from toontown.quest import Quests
from lib.libotp.NametagGlobals import NAMETAG_COLOR_LIST
import random, limeade

class MagicWordManagerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def generate(self):
        DistributedObjectAI.generate(self)
        self.air.mwDispatcher.register(
          ['hp', 'sethp'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_DEV,
           'argTypes': [(int, True)],
           'callback': self.doSetHp
          }
          )
        self.air.mwDispatcher.register(
         ['system', 'smsg'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_ADMIN,
           'argTypes': [(str, True)],
           'callback': self.doSystem
          }
          )
        self.air.mwDispatcher.register(
         ['setgm', 'gm'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_COMMUNITY,
           'argTypes': [(int, False)],
           'defaults': {0: 0},
           'callback': self.doGM,
          }
          )
        self.air.mwDispatcher.register(
         ['pinkslips', 'fires'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_DEV,
           'argTypes': [(int, False)],
           'defaults': {0: 255},
           'callback': self.doPinkSlips,
          }
          )
        self.air.mwDispatcher.register(
         ['clearinv', 'noinv', 'clearinventory', 'noinventory', 'nostuff'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_DEV,
           'callback': self.doClearInventory,
          }
          )
        self.air.mwDispatcher.register(
         ['endholiday', 'stopholiday'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_ADMIN,
           'argTypes': [(int, True)],
           'callback': self.doStopHoliday,
          }
          )
        self.air.mwDispatcher.register(
         ['fo', 'cogdo', 'spawnfo', 'spawncogdo'],
          {
           'target': TARGET_SELF,
           'access': ACCESS_DEV,
           'argTypes': [(str, True)],
           'callback': self.doSpawnFO,
          }
          )

        words = {
          'ghost':
            {
              'target': TARGET_SELF,
              'access': ACCESS_CREATIVE,
              'callback': self.doGhost
            },
          'maxtoon':
            {
               'target': TARGET_SELF,
               'access': ACCESS_CREATIVE,
               'argTypes': [(str, False)],
               'defaults': {0: ''},
               'callback': self.doMaxToon
            },
           'regulartoon':
             {
               'target': TARGET_SELF,
               'access': ACCESS_CREATIVE,
               'callback': self.doRegularToon
             },
           'restock': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: 0},
               'callback': self.doRestock
            },
           'unites': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: 32767},
               'callback': self.doUnites
            },
           'summons': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: ToontownGlobals.MAX_SUMMONS},
               'callback': self.doSummons
            },
           'name':
            {
               'target': TARGET_SELF,
               'access': ACCESS_CREATIVE,
               'argTypes': [(str, True)],
               'callback': self.doName
            },
           'glovetickets': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: 255},
               'callback': self.doGloveTickets
            },
           'clothingtickets': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: 255},
               'callback': self.doClothingTickets
            },
           'tickets': {
               'target': TARGET_SELF,
               'access': ACCESS_DEV,
               'argTypes': [(int, False)],
               'defaults': {0: 99999},
               'callback': self.doRacingTickets
            },
            'nametagstyle': {
               'target': TARGET_SELF,
               'access': ACCESS_CREATIVE,
               'argTypes': [(str, True)],
               'callback': self.doNametagStyle
            },
            'nametagcolor': {
               'target': TARGET_SELF,
               'access': ACCESS_CREATIVE,
               'argTypes': [(int, True)],
               'callback': self.doNametagColor
            },
            'skipmovie': {
               'target': TARGET_SELF,
               'access': ACCESS_MOD,
               'callback': self.skipMovie
            },
            'startholiday': {
               'target': TARGET_SELF,
               'access': ACCESS_ADMIN,
               'argTypes': [(int, True)],
               'callback': self.doStartHoliday
            },
            'cogpage': {
              'target': TARGET_SELF,
              'access': ACCESS_DEV,
              'callback': self.doCogPageFull,
            },
            'togglekart': {
                'target': TARGET_SELF,
                'access': ACCESS_CREATIVE,
                'callback': self.toggleKart
            },
            'refresh': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'callback': self.refreshModules
            },
            'completequest': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'argTypes': [(int, True)],
                'callback': self.doCompleteQuest
            },
            'completequests': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'callback': self.doCompleteQuests
            },
            'questtier': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'argTypes': [(int, True)],
                'callback': self.doQuestTier
            },
            'stopinvasion': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'callback': self.doStopInvasion
            },
            'hat': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'argTypes': [(int, True), (int, True)],
                'callback': self.doHat,
            },
            'shoes': {
                'target': TARGET_SELF,
                'access': ACCESS_DEV,
                'argTypes': [(int, True), (int, True)],
                'callback': self.doShoes,
            },

        }
        self.air.mwDispatcher.merge(words)

    def doSetHp(self, av, target, extraArgs):
        hp = extraArgs[0]

        target.b_setHp(hp)
        return 'HP has been set to %s.' % hp # TODO: make this a localize code

    def doSystem(self, av, target, extraArgs):
        message = extraArgs[0]
        dclass = simbase.air.dclassesByName['ClientManager']
        datagram = dclass.aiFormatUpdate('systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_MANAGER, 10, OtpDoGlobals.OTP_ALL_CLIENTS, [message])
        simbase.air.send(datagram)

    def doGM(self, av, target, extraArgs):
        requestedGM = extraArgs[0]
        if requestedGM == 0:
            av.b_setGM(0)
            return 'Turned off GM icon!' # TODO: make this localized
        if av.getAccessLevel() == ACCESS_COMMUNITY:
            av.b_setGM(6)
        else:
            if requestedGM > 6 or requestedGM < 0:
                return 'Requested invalid GM icon! Range is (0-6)'
            av.b_setGM(requestedGM)
        return 'GM icon has been set to %s.' % requestedGM

    def doGhost(self, av, target, extraArgs):
        if av.ghostMode:
            av.b_setGhostMode(0)
        else:
            av.b_setGhostMode(1)
        return 'Toggled ghost mode!' # TODO: make this a localize code

    def doMaxToon(self, av, target, extraArgs):
        av.b_setTrackAccess([1, 1, 1, 1, 1, 1, 1])
        av.b_setMaxCarry(80)
        av.experience.maxOutExp()
        av.b_setExperience(av.experience.makeNetString())
        av.inventory.zeroInv()
        av.inventory.maxOutInv(filterUberGags = 0, filterPaidGags = 0)
        av.b_setInventory(av.inventory.makeNetString())
        emotes = list(av.getEmoteAccess())
        for emoteId in list(OTPLocalizer.EmoteFuncDict.values()):
           if emoteId >= len(emotes):
              continue
           emotes[emoteId] = 1
        av.b_setEmoteAccess(emotes)

        av.b_setCogParts(
            [
              CogDisguiseGlobals.PartsPerSuitBitmasks[0],
              CogDisguiseGlobals.PartsPerSuitBitmasks[1],
              CogDisguiseGlobals.PartsPerSuitBitmasks[2],
              CogDisguiseGlobals.PartsPerSuitBitmasks[3]
            ]
        )

        av.b_setCogLevels([49] * 4)
        av.b_setCogTypes([7, 7, 7, 7])

        deptCount = len(SuitDNA.suitDepts)
        av.b_setCogCount(list(CogPageGlobals.COG_QUOTAS[1]) * deptCount)
        cogStatus = [CogPageGlobals.COG_COMPLETE2] * SuitDNA.suitsPerDept
        av.b_setCogStatus(cogStatus * deptCount)
        av.b_setCogRadar([1, 1, 1, 1])
        av.b_setBuildingRadar([1, 1, 1, 1])

        av.b_setSummons(ToontownGlobals.MAX_SUMMONS)

        hoods = list(ToontownGlobals.HoodsForTeleportAll)
        av.b_setHoodsVisited(hoods)
        av.b_setTeleportAccess(hoods)

        av.b_setMoney(av.getMaxMoney())
        av.b_setMaxMoney(250)
        av.b_setMaxBankMoney(20000)
        av.b_setBankMoney(20000)

        av.b_setQuestCarryLimit(4)

        av.b_setQuests([])
        av.b_setRewardHistory(Quests.ELDER_TIER, [])

        if simbase.wantPets:
            av.b_setPetTrickPhrases(list(range(7)))

        av.b_setTickets(99999)
        av.b_setPinkSlips(255)

        av.restockAllNPCFriends()
        av.restockAllResistanceMessages(32767)

        av.b_setMaxHp(ToontownGlobals.MaxHpLimit)
        av.toonUp(av.getMaxHp() - av.hp)
        return 'Maxed your Toon!' # TODO: Make this a magic word localizer code

    def doRegularToon(self, av, target, extraArgs):
        pickTrack = ([1, 1, 1, 1, 1, 1, 0], # Dropless
                     [1, 1, 1, 0, 1, 1, 1], # Soundless
                     [0, 1, 1, 1, 1, 1, 1], # Toon-less
                     [1, 1, 0, 1, 1, 1, 1], # Lure-less
                     [1, 0, 1, 1, 1, 1, 1]) # Trapless
        av.b_setTrackAccess(random.choice(pickTrack))
        av.b_setMaxCarry(ToontownGlobals.MaxCarryLimit)
        av.b_setQuestCarryLimit(ToontownGlobals.MaxQuestCarryLimit)
        av.experience.makeExpRegular()
        av.d_setExperience(av.experience.makeNetString())
        laughminus = int(random.random() * 20.0) + 10.0
        av.b_setMaxHp(ToontownGlobals.MaxHpLimit-laughminus)
        av.b_setHp(ToontownGlobals.MaxHpLimit-laughminus)
        return 'You are now a regular Toon!' # TODO: make this a magic word localizer code.

    def doRestock(self, av, target, extraArgs):
        noUber = extraArgs[0]
        av.doRestock(noUber)
        return 'Restocked inventory with %s noUber arg!' % noUber # TODO: improve this response msg

    def doClearInventory(self, av, target, extraArgs):
        av.inventory.zeroInv()
        av.d_setInventory(av.inventory.makeNetString())
        return 'Cleared inventory!'

    def doUnites(self, av, target, extraArgs):
        uniteNum = extraArgs[0]
        if uniteNum < 0 or uniteNum > 32767:
            return 'Invalid unite number! Range: (0-32767)'
        av.restockAllResistanceMessages(uniteNum)
        return 'Restocked unites.'

    def doSummons(self, av, target, extraArgs):
        summons = extraArgs[0]
        if summons < 0 or summons > ToontownGlobals.MAX_SUMMONS:
            return 'Invalid summons number! Range: (0-1000)'
        av.b_setSummons(summons)
        return 'Set summons to %s' % summons

    def doPinkSlips(self, av, target, extraArgs):
        slips = extraArgs[0]
        if slips < 0 or slips > 255:
            return 'Invalid pink slips number! Range: (0-255)'
        av.b_setPinkSlips(slips)
        return 'Set glove tickets to %s' % slips

    def doName(self, av, target, extraArgs):
        name = extraArgs[0]
        av.b_setName(name)

    def doGloveTickets(self, av, target, extraArgs):
        tickets = extraArgs[0]
        if tickets < 0 or tickets > 255:
            return 'Invalid clothing tickets number! Range: (0-255)'
        av.b_setGloveTickets(tickets)
        return 'Set glove tickets to %s' % tickets

    def doClothingTickets(self, av, target, extraArgs):
        tickets = extraArgs[0]
        if tickets < 0 or tickets > 255:
            return 'Invalid clothing tickets number! Range: (0-255)'
        av.b_setClothingTickets(tickets)
        return 'Set clothing tickets to %s' % tickets

    def doRacingTickets(self, av, target, extraArgs):
        tickets = extraArgs[0]
        av.b_setTickets(tickets)
        return 'Set racing tickets to %s' % tickets

    def doNametagStyle(self, av, target, extraArgs):
        style = extraArgs[0]

        nametagList = list(TTLocalizer.NametagFontNames)
        for index, item in enumerate(nametagList):
            nametagList[index] = item.lower()

        style == style.lower()

        if style in nametagList:
            index = nametagList.index(style)
        elif style == 'basic':
            index = 100
        else:
            return 'Invalid nametag style entered.'

        av.b_setNametagStyle(index)
        return 'Successfully set nametag style: {0}!'.format(style)

    def doNametagColor(self, av, target, extraArgs):
        color = extraArgs[0]

        if color not in NAMETAG_COLOR_LIST:
            return 'Invalid nametag color specified. Range: (%s-%s)' % (NAMETAG_COLOR_LIST[0], NAMETAG_COLOR_LIST[-1])

        av.b_setNametagColor(color)
        return 'Successfully set nametag color: {0}!'.format(color)

    def toggleKart(self, av, target, extraArgs):
        if not av.hasKart():
            return 'You do not have a kart!'

        av.toggleKart()

        return 'Toggled kart.'
        
    def doCompleteQuest(self, av, target, extraArgs):
        index = extraArgs[0]
        if self.air.questManager.completeQuestMagically(av, index):
            return 'Successfully completed quest!'
        return 'Invalid index.'
        
    def doCompleteQuests(self, av, target, extraArgs):
        self.air.questManager.completeAllQuestsMagically(av)
        return 'Completed all quests!'
        
    def doQuestTier(self, av, target, extraArgs):
        tier = extraArgs[0]
        av.b_setQuests([])
        av.b_setRewardHistory(tier, [])
        return 'Set quest tier to %s' % tier

    def doMagicWordAI(self, mwString, targetId):
        wordName, extraArgs = (mwString.split(' ', 1) + [''])[:2]
        wordName = wordName.lower()

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        word = self.air.mwDispatcher.getWord(wordName)
        if not word:
            # Try to see if its close to another existing Magic Word.
            for word in self.air.mwDispatcher.words:
                if wordName in word:
                    return self.sendMagicWordResponseString(avId, ResponseCode2String[8].format(word))
                else:
                    return self.sendMagicWordResponseCode(avId, 5)
        target = self.air.doId2do.get(targetId)
        if not target:
            return
        avAccess = av.getAccessLevel()
        if avAccess < MIN_MAGIC_WORD_ACCESS:
            return
        minAccess = self.air.mwDispatcher.getAccess(wordName)
        if avAccess < minAccess:
            return self.sendMagicWordResponseCode(avId, 6)

        valid, responseCode, parsedArgs = self.air.mwDispatcher.checkIfWordIsValid(wordName, av, target, extraArgs)
        if not valid:
            return self.sendMagicWordResponseCode(avId, responseCode)

        callback = self.air.mwDispatcher.getCallback(wordName)

        try:
            callbackResponse = callback(av, target, parsedArgs)
            if callbackResponse:
                if type(callbackResponse) == str:
                    self.sendMagicWordResponseString(avId, callbackResponse)
                else:
                    self.sendMagicWordResponseCode(avId, callbackResponse)
        except:
            info = describeException()
            self.sendMagicWordResponseString(avId, info)
            
    def skipMovie(self, av, target, extraArgs):
        battleId = av.getBattleId()
        if not battleId:
            return 'You are not in a battle!'
        battle = self.air.doId2do.get(battleId)
        battle._DistributedBattleBaseAI__movieDone()
        return 'Skipped battle movie.'

    def doStartHoliday(self, av, target, extraArgs):
        holidayId = extraArgs[0]
        if not hasattr(self.air, 'holidayManager'):
            return "Holiday manager isn't generated in this AI. Holiday not started."
        if self.air.holidayManager.isHolidayRunning(holidayId):
            return 'Holiday {} is already running!'.format(holidayId)

        self.air.holidayManager.startHoliday(holidayId)
        return 'Holiday {} has started!'.format(holidayId)
        
    def doStopHoliday(self, av, target, extraArgs):
        holidayId = extraArgs[0]
        if not hasattr(self.air, 'holidayManager'):
            return "Holiday manager isn't generated in this AI. Holiday not ended."
        if not self.air.holidayManager.isHolidayRunning(holidayId):
            return 'Holiday {} is not running!'.format(holidayId)

        self.air.holidayManager.endHoliday(holidayId)
        return 'Holiday {} has stopped!'.format(holidayId)
        
    def doCogPageFull(self, av, target, extraArgs):
        av.b_setCogStatus([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        av.b_setCogCount([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        return 'Cog page is now filled.'
        
    def doSpawnFO(self, av, target, extraArgs):
        track = extraArgs[0]
        allowedTracks = ['l', 's', 'm']
        if track not in allowedTracks:
            return "Invalid tracks. Allowed tracks are {0}".format(allowedTracks)
        bldg = av.findClosestDoor()
        if not bldg:
            return "Unable to find a toon building."
        bldg.cogdoTakeOver(track)
        return 'Successfully spawned a Field Office with track {0}!'.format(track)

    def refreshModules(self, av, target, extraArgs):
        limeade.refresh()

        return 'Refreshed AI modules.'
        
    def doStopInvasion(self, av, target, extraArgs):
        if self.air.suitInvasionManager.getInvading():
            self.air.suitInvasionManager.stopInvasion()
            return 'Stopped invasion.'
        return 'No invasion found.'
        
    def doHat(self, av, target, extraArgs):
        hatId, hatTex = extraArgs
        if not 0 <= hatId < len(ToonDNA.HatModels):
            return 'Invalid hat index.'
        if not 0 <= hatTex < len(ToonDNA.HatTextures):
            return 'Invalid hat texture.'
        avdna = av.dna
        avdna.hat = (hatId, hatTex, 0)
        av.b_setDNAString(avdna.makeNetString())
        
    def doShoes(self, av, target, extraArgs):
        shoeId, shoeTex = extraArgs
        if not 0 <= shoeId < len(ToonDNA.ShoesModels):
            return 'Invalid shoe index.'
        if not 0 <= shoeTex < len(ToonDNA.ShoesTextures):
            return 'Invalid shoe texture.'
        avdna = av.dna
        avdna.shoes = (shoeId, shoeTex, 0)
        av.b_setDNAString(avdna.makeNetString())

    def sendMagicWordResponseString(self, avId, responseStr):
        self.sendUpdateToAvatarId(avId, 'magicWordResponseString', [responseStr])

    def sendMagicWordResponseCode(self, avId, responseCode):
        self.sendUpdateToAvatarId(avId, 'magicWordResponseCode', [responseCode])