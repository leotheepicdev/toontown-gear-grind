from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed import ClockDelta
from direct.fsm.FSM import FSM

from toontown.fishing import BingoGlobals
from toontown.fishing import FishGlobals
from .NormalBingo import NormalBingo
from .FourCornerBingo import FourCornerBingo
from .DiagonalBingo import DiagonalBingo
from .ThreewayBingo import ThreewayBingo
from .BlockoutBingo import BlockoutBingo
from direct.showbase import RandomNumGen
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

import random

class DistributedPondBingoManagerAI(DistributedObjectAI, FSM):
    notify = directNotify.newCategory('DistributedPondBingoManagerAI')
    cardTypes = [BingoGlobals.NORMAL_CARD, BingoGlobals.FOURCORNER_CARD,
                 BingoGlobals.DIAGONAL_CARD, BingoGlobals.THREEWAY_CARD]

    cardTypeDict = {BingoGlobals.NORMAL_CARD: NormalBingo,
     BingoGlobals.FOURCORNER_CARD: FourCornerBingo,
     BingoGlobals.DIAGONAL_CARD: DiagonalBingo,
     BingoGlobals.THREEWAY_CARD: ThreewayBingo,
     BingoGlobals.BLOCKOUT_CARD: BlockoutBingo}

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedPondBingoManager')

        self.pond = None
        self.pondId = 0
        self.state = 'Off'
        self.timestamp = 0

        self.cardId = 0
        self.typeId = 0
        self.tileSeed = 0
        self.game = None
        self.bingo = False
        self.jackpot = 0
        self.durationTask = None
        self.typeId = BingoGlobals.NORMAL_CARD

        self.forcedTypeId = config.GetInt('force-bingo-type', -1) # For debugging.

    def delete(self):
        self.request('Off')
        DistributedObjectAI.delete(self)

    def setPond(self, pond):
        self.pond = pond
        self.pond.bingoMgr = self

    def getPondDoId(self):
        return self.pond.doId

    def sendUpdateToPond(self, field, args=[]):
        # Send a field update to all occupants
        # in the pond.
        for spot in self.pond.spots.values():
            if spot.avId is not None:
                self.sendUpdateToAvatarId(spot.avId, field, args)

    def awardPond(self):
        # Award the bingo money to everybody
        # playing in the pond.
        for spot in self.pond.spots.values():
            if spot.avId is not None:
                toon = self.air.doId2do.get(spot.avId)
                if not toon:
                    continue
                toon.addMoney(self.jackpot)

    def sendStatesToAvatar(self, avId):
        # A toon has joined the pond while bingo
        # is in session!  Let's give them the goods.
        if self.state == 'Intro':
            # Loading 'Intro' while the GUI is loading will crash the game.
            # It's kinda redundant anyways since the bucket would be already moved
            # back if the bingoManager is generated.
            return
        if avId not in self.air.doId2do:
            # "???" 2: Confusion Boogaloo.
            return
        self.sendUpdateToAvatarId(avId, 'setCardState', [self.cardId, self.typeId, self.tileSeed, self.game.gameState])
        self.sendUpdateToAvatarId(avId, 'setState', [self.state, self.timestamp])
        if self.jackpot != BingoGlobals.getJackpot(self.typeId):
            self.sendUpdateToAvatarId(avId, 'setJackpot', [self.jackpot])
        if self.bingo:
            self.sendUpdateToAvatarId(avId, 'enableBingo', [])

    def start(self):
        self.b_setState('Intro')

    def getNewBingoCard(self, blockout = False):
        if self.isDeleted():
            # ???
            return

        if self.state not in ('Intro', 'GameOver', 'Reward', 'Intermission'):
            self.notify.warning('getNewBingoCard called in invalid state: {}'.format(self.state))
            return

        if self.state != 'Intro' and not self.air.fishBingoManager.running \
        and not blockout:
            # Fish Bingo has closed down.
            self.b_setState('CloseEvent')
            return

        if self.air.fishBingoManager.intermission:
            # We are having an intermission.  It will end at the top
            # of the hour for Blockout Bingo.
            if not self.game:
                # Fix gameState crash if started without a game.
                 self.game = self.cardTypeDict.get(self.typeId)()
            timestamp = self.air.fishBingoManager.intermission
            self.b_setState('Intermission', timestamp)
            return

        self.cardId += 1
        self.cardId %= 1 << 16
        if blockout:
            self.typeId = BingoGlobals.BLOCKOUT_CARD
        elif self.forcedTypeId > -1:
            self.typeId = self.forcedTypeId
        else:
            self.typeId = random.choice(self.cardTypes)
        self.tileSeed = random.randint(0, 1 << 16)

        self.game = self.cardTypeDict.get(self.typeId)()
        self.game.generateCard(self.tileSeed, self.pond.getArea())
        self.jackpot = BingoGlobals.getJackpot(self.typeId)

        self.d_setCardState(self.cardId, self.typeId, self.tileSeed, self.game.gameState)
        self.b_setState('WaitCountdown')

    def setState(self, state, timestamp):
        self.state = state
        self.timestamp = timestamp
        self.request(state)

    def d_setState(self, state, timestamp):
        self.sendUpdateToPond('setState', [state, timestamp])

    def b_setState(self, state, timestamp = 0):
        if not timestamp:
            timestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.setState(state, timestamp)
        self.d_setState(state, timestamp)

    def d_setCardState(self, cardId, typeId, tileSeed, gameState):
        self.sendUpdateToPond('setCardState', [cardId, typeId, tileSeed, gameState])

    def enterIntro(self):
        taskMgr.doMethodLater(BingoGlobals.INTRO_SESSION, self.getNewBingoCard, self.uniqueName('intro-duration'), [])

    def enterWaitCountdown(self):
        taskMgr.doMethodLater(BingoGlobals.TIMEOUT_SESSION, self.b_setState, self.uniqueName('countdown-duration'), extraArgs=['Playing'])

    def enterPlaying(self):
        self.durationTask = taskMgr.doMethodLater(BingoGlobals.getGameTime(self.typeId), self.b_setState, self.uniqueName('playing-duration'), extraArgs=['GameOver'])

    def exitPlaying(self):
        if self.durationTask:
            taskMgr.remove(self.durationTask)
            self.durationTask = None
        if self.bingo:
            self.bingo = False

    def enterGameOver(self):
        taskMgr.doMethodLater(BingoGlobals.REWARD_TIMEOUT, self.getNewBingoCard, self.uniqueName('gameover-duration'), [])

    def enterReward(self):
        taskMgr.doMethodLater(BingoGlobals.REWARD_TIMEOUT, self.getNewBingoCard, self.uniqueName('reward-duration'), [])

    def enterCloseEvent(self):
        taskMgr.doMethodLater(BingoGlobals.CLOSE_EVENT_TIMEOUT, self.air.fishBingoManager.closeBingoMgr, self.uniqueName('closeevent-duration'), [self])

    def d_updateGameState(self, gameState, cellId):
        self.sendUpdateToPond('updateGameState', [gameState, cellId])

    def cardUpdate(self, cardId, cellId, genus, species):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId, 'Unknown player {} tried to update bingo card!'.format(avId))
            return

        if self.state != 'Playing':
            self.air.writeServerEvent('suspicious', avId, 'Player tried to update a bingo card while we\'re in the {} state!'.format(self.state))
            return

        if cardId != self.cardId:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to update a bingo card with an invalid Card ID!  Got: {}  Expecting: {}'.format(cellId, self.cellId))
            return

        # Update the bingo card.
        success = self.game.cellUpdateCheck(cellId, genus, species)
        if success == BingoGlobals.UPDATE:
            self.d_updateGameState(self.game.gameState, cellId)
        elif success == BingoGlobals.WIN:
            self.d_updateGameState(self.game.gameState, cellId)
            self.d_enableBingo()

    def d_enableBingo(self):
        self.bingo = True
        self.sendUpdateToPond('enableBingo')

    def handleBingoCall(self, cardId):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId, 'Unknown player {} tried to call bingo!'.format(avId))
            return

        if self.state != 'Playing':
            self.air.writeServerEvent('suspicious', avId, 'Player tried to call bingo while we\'re in the {} state!'.format(self.state))
            return

        if cardId != self.cardId:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to call bingo with an invalid Card ID!  Got: {}  Expecting: {}'.format(cellId, self.cellId))
            return

        if self.game.checkForBingo() != BingoGlobals.WIN:
            self.air.writeServerEvent('suspicious', avId, 'Player tried to call bingo even though we don\'t have a bingo winning card!')
            return

        # IT'S A BINGO!
        toon.d_announceBingo()

        # Give out the reward to everybody on the pond.
        self.awardPond()

        # And that's all she wrote for this bingo game!
        self.b_setState('Reward')

        # If it's a blockout win, let the FishBingoManager know.
        if self.typeId == BingoGlobals.BLOCKOUT_CARD and self.air.fishBingoManager.blockout:
            self.air.fishBingoManager.handleBlockoutWin(self)

    def setJackpot(self, jackpot):
        self.jackpot = jackpot

    def d_setJackpot(self, jackpot):
        self.sendUpdateToPond('setJackpot', [jackpot])

    def b_setJackpot(self, jackpot):
        self.setJackpot(jackpot)
        self.d_setJackpot(jackpot)
