from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.quest import Quests

class QuestManagerAI:
    notify = directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air

    def toonPlayedMinigame(self, toon, toons):
        # toons is never used. Sad!
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.TrolleyQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def recoverItems(self, toon, suitsKilled, zoneId):
        recovered, notRecovered = ([] for _ in range(2))
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                isComplete = quest.getCompletionStatus(toon, toon.quests[index])
                if isComplete == Quests.COMPLETE:
                    continue

                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.Any or quest.getHolderType() in ['type', 'track', 'level']:
                        for suit in suitsKilled:
                            if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                                break

                            if (quest.getHolder() == Quests.Any) or (
                                    quest.getHolderType() == 'type' and quest.getHolder() == suit['type']) or (
                                    quest.getHolderType() == 'track' and quest.getHolder() == suit['track']) or (
                                    quest.getHolderType() == 'level' and quest.getHolder() <= suit['level']):
                                # This seems to be how Disney did it.
                                progress = toon.quests[index][4] & pow(2, 16) - 1
                                completion = quest.testRecover(progress)
                                if completion[0]:
                                    # Recovered!
                                    recovered.append(quest.getItem())
                                    self.__incrementQuestProgress(toon.quests[index])
                                else:
                                    # Not recovered. Sad!
                                    notRecovered.append(quest.getItem())

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

        return recovered, notRecovered

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToons):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.CogQuest):
                for suit in suitsKilled:
                    for _ in range(quest.doesCogCount(toon.getDoId(), suit, zoneId, activeToons)):
                        self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonKilledCogdo(self, toon, difficulty, numFloors, zoneId, activeToons):
        pass

    def toonKilledBuilding(self, toon, tracks, difficulty, floors, zoneId, activeToons):
        # TODO: support mixed dept buildings
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.BuildingQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getBuildingTrack() == Quests.Any or quest.getBuildingTrack() == tracks[0]:
                        if floors >= quest.getNumFloors():
                            for _ in range(quest.doesBuildingCount(toon.getDoId(), activeToons)):
                                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())
            
    def toonKilledTomBuilding(self, toon, activeToons):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.TutorialTomBuildingQuest):
                for _ in range(quest.doesBuildingCount(toon.getDoId(), activeToons)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonDefeatedFactory(self, toon, factoryId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FactoryQuest):
                for _ in range(quest.doesFactoryCount(toon.getDoId(), factoryId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonRecoveredCogSuitPart(self, toon, zoneId, toonList):
        pass

    def toonDefeatedMint(self, toon, mintId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.MintQuest):
                for _ in range(quest.doesMintCount(toon.getDoId(), mintId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())
            
    def toonDefeatedCountryClub(self, toon, countryClubId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.CountryClubQuest):
                for _ in range(quest.doesCountryClubCount(toon.getDoId(), countryClubId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonDefeatedStage(self, toon, stageId, activeToonVictors):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.StageQuest):
                for _ in range(quest.doesStageCount(toon.getDoId(), stageId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def requestInteract(self, avId, npc):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        for index, quest in enumerate(self.__toonQuestsList2Quests(av.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = av.quests[index]
            isComplete = quest.getCompletionStatus(av, av.quests[index], npc)
            if isComplete != Quests.COMPLETE:
                continue

            if avId in self.air.tutorialManager.playerDict:
                self.air.tutorialManager.playerDict[avId].preparePlayerForTunnel()

            if isinstance(quest, Quests.DeliverGagQuest):
                track, level = quest.getGagType()
                av.inventory.setItem(track, level, av.inventory.numItem(track, level) - quest.getNumGags())
                av.b_setInventory(av.inventory.makeNetString())

            nextQuest = Quests.getNextQuest(questId, npc, av)
            if nextQuest == (Quests.NA, Quests.NA):
                if isinstance(quest, Quests.TrackChoiceQuest):
                    npc.presentTrackChoice(avId, questId, quest.getChoices())
                    return

                rewardId = Quests.getAvatarRewardId(av, questId)
                npc.completeQuest(avId, questId, rewardId)
                self.completeQuest(av, questId)
                self.giveReward(av, rewardId)
                return
            else:
                self.completeQuest(av, questId)
                nextQuestId = nextQuest[0]
                nextRewardId = Quests.getFinalRewardId(questId, 1)
                nextToNpcId = nextQuest[1]
                self.npcGiveQuest(npc, av, nextQuestId, nextRewardId, nextToNpcId)
                return

        if len(self.__toonQuestsList2Quests(av.quests)) >= av.getQuestCarryLimit():
            npc.rejectAvatar(avId)
            return

        if avId in self.air.tutorialManager.playerDict:
            if av.getRewardHistory()[0] == 0:
                self.npcGiveQuest(npc, av, 101, Quests.findFinalRewardId(101)[0], Quests.getQuestToNpcId(101),
                                  storeReward=True)
                self.air.tutorialManager.playerDict[avId].preparePlayerForBattle()
                return

        tier = av.getRewardHistory()[0]
        if Quests.avatarHasAllRequiredRewards(av, tier):
            if not Quests.avatarWorkingOnRequiredRewards(av):
                if tier != Quests.LOOPING_FINAL_TIER:
                    tier += 1

                av.b_setRewardHistory(tier, [])
            else:
                npc.rejectAvatarTierNotDone(avId)
                return

        bestQuests = Quests.chooseBestQuests(tier, npc, av)
        if not bestQuests:
            npc.rejectAvatar(avId)
            return

        npc.presentQuestChoice(avId, bestQuests)
        return

    def __toonQuestsList2Quests(self, quests):
        return [Quests.getQuest(x[0]) for x in quests]

    def avatarCancelled(self, avId):
        pass

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        self.npcGiveQuest(npc, av, questId, rewardId, toNpcId, storeReward=True)

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Show the completion movie and remove the task.
        npc.completeQuest(avId, pendingTrackQuest, Quests.getRewardIdFromTrackId(trackId))
        self.completeQuest(av, pendingTrackQuest)

        # Set their track their working on.
        av.b_setTrackProgress(trackId, 0)

    def npcGiveQuest(self, npc, av, questId, rewardId, toNpcId, storeReward=False):
        rewardId = Quests.transformReward(rewardId, av)
        finalReward = rewardId if storeReward else 0
        progress = 0
        av.addQuest((questId, npc.getDoId(), toNpcId, rewardId, progress), finalReward)
        npc.assignQuest(av.getDoId(), questId, rewardId, toNpcId)

    def __incrementQuestProgress(self, quest):
        quest[4] += 1

    def completeQuest(self, toon, questId):
        toon.toonUp(toon.getMaxHp())
        toon.removeQuest(questId)

    def toonRodeTrolleyFirstTime(self, toon):
        # For this, we just call toonPlayedMinigame with the toon.
        # And for toons, we just pass in an empty list. Not like
        # it matters anyway, as that argument is never used.
        self.toonPlayedMinigame(toon, [])

    def giveReward(self, toon, rewardId):
        reward = Quests.getReward(rewardId)
        if reward:
            reward.sendRewardAI(toon)

    def toonMadeFriend(self, toon, otherToon):
        # This is so sad, can we leave otherToon unused?
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FriendQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())

    def toonFished(self, toon, zoneId):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                    continue

                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.AnyFish:
                        # This seems to be how Disney did it.
                        progress = toon.quests[index][4] & pow(2, 16) - 1
                        completion = quest.testRecover(progress)
                        if completion[0]:
                            # Recovered!
                            self.__incrementQuestProgress(toon.quests[index])
                            if toon.quests:
                                toon.d_setQuests(toon.getQuests())

                            return quest.getItem()

        return 0

    def toonCalledClarabelle(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.PhoneQuest):
                self.__incrementQuestProgress(toon.quests[index])

        if toon.quests:
            toon.d_setQuests(toon.getQuests())
            
    def completeAllQuestsMagically(self, av):
        avQuests = av.quests
        for quest in avQuests:
            quest[4] = 1000
        av.b_setQuests(avQuests)
        return 1
        
    def completeQuestMagically(self, av, index):
        avQuests = av.quests
        if index < len(av.quests):
            avQuests[index][4] = 1000
            av.b_setQuests(avQuests)
            return 1
        return 0