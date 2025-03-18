from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownBattleGlobals
from toontown.suit import SuitDNA
import time
BattleExperienceAINotify = DirectNotifyGlobal.directNotify.newCategory('BattleExprienceAI')

def getSkillGained(toonSkillPtsGained, toonId, track):
    exp = 0
    expList = toonSkillPtsGained.get(toonId, None)
    if expList != None:
        exp = expList[track]
    return int(exp + 0.5)


def getBattleExperience(numToons, activeToons, toonExp, toonSkillPtsGained, toonOrigQuests, toonItems, toonOrigMerits, toonMerits, toonParts, suitsKilled, helpfulToonsList=None, mvp=0, avId2SuitsKilled={}):
    if helpfulToonsList == None:
        BattleExperienceAINotify.warning('=============\nERROR ERROR helpfulToons=None in assignRewards , tell Red')
        
    toonsList = []
    for k in range(numToons):
        toon = None
        if k < len(activeToons):
            toonId = activeToons[k]
            toon = simbase.air.doId2do.get(toonId)
        if toon == None:
            toonsList.append( 
              (
              -1, 
              [0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0],
              [],
              [],
              [],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              0,
              0,
              ) 
            )
        else:
            origExp = toonExp[toonId]
            earnedExp = []
            for i in range(len(ToontownBattleGlobals.Tracks)):
                earnedExp.append(getSkillGained(toonSkillPtsGained, toonId, i))
            items = toonItems.get(toonId, ([], []))
            
            piggyBank = toon.getPiggyBank()
            piggyMax = piggyBank[1]
            timeToNext = piggyBank[2]
            if time.time() < timeToNext:
                piggyAmount = 0
            else:
                if toonId in avId2SuitsKilled:
                    piggyAmount = toon.addPiggyBank(avId2SuitsKilled[toonId])
                else:
                    piggyAmount = 0
        
            toonsList.append(
              (
              toonId,
              origExp,
              earnedExp,
              toonOrigQuests.get(toonId, []),
              items[0],
              items[1],
              toonOrigMerits.get(toonId, [0, 0, 0, 0]),
              toonMerits.get(toonId, [0, 0, 0, 0]),
              toonParts.get(toonId, [0, 0, 0, 0]),
              piggyAmount,
              piggyMax,
              )
            )

    deathList = []
    toonIndices = {}
    for i in range(len(activeToons)):
        toonIndices[activeToons[i]] = i

    for deathRecord in suitsKilled:
        level = deathRecord['level']
        type = deathRecord['type']
        track = deathRecord['track']
        if deathRecord['isVP'] or deathRecord['isCFO']:
            level = 0
        involvedToonIds = deathRecord['activeToons']
        toonBits = 0
        for toonId in involvedToonIds:
            if toonId in toonIndices:
                toonBits |= 1 << toonIndices[toonId]

        flags = 0
        if deathRecord['isSkelecog']:
            flags |= ToontownBattleGlobals.DLF_SKELECOG
        if deathRecord['isForeman']:
            flags |= ToontownBattleGlobals.DLF_FOREMAN
        if deathRecord['isVP']:
            flags |= ToontownBattleGlobals.DLF_VP
        if deathRecord['isCFO']:
            flags |= ToontownBattleGlobals.DLF_CFO
        if deathRecord['isSupervisor']:
            flags |= ToontownBattleGlobals.DLF_SUPERVISOR
        if deathRecord['isVirtual']:
            flags |= ToontownBattleGlobals.DLF_VIRTUAL
        if 'hasRevives' in deathRecord and deathRecord['hasRevives']:
            flags |= ToontownBattleGlobals.DLF_REVIVES
        deathList.append([type, level, track, toonBits, flags])
    if helpfulToonsList == None:
        helpfulToonsList = []

    return [toonsList, deathList, helpfulToonsList, mvp]


def assignRewards(activeToons, toonSkillPtsGained, suitsKilled, zoneId, helpfulToons = None):
    if helpfulToons == None:
        BattleExperienceAINotify.warning('=============\nERROR ERROR helpfulToons=None in assignRewards , tell Red')
    activeToonList = []
    for t in activeToons:
        toon = simbase.air.doId2do.get(t)
        if toon != None:
            activeToonList.append(toon)

    for toon in activeToonList:
        for i in range(len(ToontownBattleGlobals.Tracks)):
            exp = getSkillGained(toonSkillPtsGained, toon.doId, i)
            totalExp = exp + toon.experience.getExp(i)
            if toon.experience.getExp(i) >= ToontownBattleGlobals.MaxSkill:
                continue
            if totalExp >= ToontownBattleGlobals.MaxSkill:
                toon.experience.setExp(i, ToontownBattleGlobals.MaxSkill)
                toon.inventory.addItem(i, ToontownBattleGlobals.UBER_GAG_LEVEL_INDEX)
                continue
            if exp > 0:
                newGagList = toon.experience.getNewGagIndexList(i, exp)
                toon.experience.addExp(i, amount=exp)
                toon.inventory.addItemWithList(i, newGagList)
        toon.b_setExperience(toon.experience.makeNetString())
        toon.d_setInventory(toon.inventory.makeNetString())
        toon.b_setAnimState('victory', 1)

        if simbase.air.config.GetBool('battle-passing-no-credit', True):
            if helpfulToons and toon.doId in helpfulToons:
                simbase.air.questManager.toonKilledCogs(toon, suitsKilled, zoneId, activeToonList)
                simbase.air.cogPageManager.toonKilledCogs(toon, suitsKilled, zoneId)
            else:
                BattleExperienceAINotify.debug('toon=%d unhelpful not getting killed cog quest credit' % toon.doId)
        else:
            simbase.air.questManager.toonKilledCogs(toon, suitsKilled, zoneId, activeToonList)
            simbase.air.cogPageManager.toonKilledCogs(toon, suitsKilled, zoneId)

    return
