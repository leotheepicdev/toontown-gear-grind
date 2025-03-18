from toontown.toonbase import ToontownBattleGlobals

def genRewardDicts(entries):
    toonRewardDicts = []
    for toonId, origExp, earnedExp, origQuests, items, missedItems, origMerits, merits, parts, piggyAmount, piggyMax in entries:
        if toonId != -1:
            dict = {}
            toon = base.cr.doId2do.get(toonId)
            if toon == None:
                continue
            dict['toon'] = toon
            dict['origExp'] = origExp
            dict['earnedExp'] = earnedExp
            dict['origQuests'] = origQuests
            dict['items'] = items
            dict['missedItems'] = missedItems
            dict['origMerits'] = origMerits
            dict['merits'] = merits
            dict['parts'] = parts
            dict['piggyAmount'] = piggyAmount
            dict['piggyMax'] = piggyMax
            toonRewardDicts.append(dict)

    return toonRewardDicts
