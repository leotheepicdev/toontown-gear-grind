from direct.distributed.DistributedObject import DistributedObject
from .MagicWordGlobals import *
from . import MagicWordLocalizer
from direct.showbase.PythonUtil import describeException
from direct.showbase.InputStateGlobal import inputState
from toontown.friends import FriendHandle
from toontown.toon import Toon
from direct.showutil.TexViewer import TexViewer
import random

if base.wantKarts:
    from toontown.racing.KartDNA import KartDNA, InvalidEntry
    from toontown.racing.KartShopGui import getDefaultRim, getDefaultColor

class MagicWordManager(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.lastClickedAvId = None
        self.texViewer = None

    def generate(self):
        DistributedObject.generate(self)
        self.accept('magicWord', self.doMagicWord)
        self.accept('clickedNametag', self.setLastClickedAvId)
        words = {
          'oobe': {
                  'target': TARGET_SELF,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doOobe
                  },
          'oobecull': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'callback': self.doOobeCull
                  },
          'run': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doRun,
                  },
          'tex': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'argTypes': [(str, True)],
                  'callback': self.doTex
                  },
          'texmem': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'callback': self.doTexMem
                  },
          'verts': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'callback': self.doVerts
                  },
          'wire': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'callback': self.doWire
                  },
          'stereo': {
                  'target': TARGET_SELF,
                  'access': ACCESS_DEV,
                  'callback': self.doStereo
                  },
          'avid': {
                  'target': TARGET_BOTH,
                  'access': ACCESS_MOD,
                  'callback': self.doAvId
                  },
          'endgame': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doEndgame
                  },
          'wingame': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doWingame
                  },
          'walk': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doWalk
                  },
          'fps': {
                  'target': TARGET_SELF,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doFps
                  },
          'getpos': {
                  'target': TARGET_BOTH,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doGetPos
                 },
          'gethpr': {
                  'target': TARGET_BOTH,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doGetHpr
                 },
          'camposhpr': {
                  'target': TARGET_SELF,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doCamPosHpr,
                 },
          'getposhpr': {
                  'target': TARGET_BOTH,
                  'access': ACCESS_CREATIVE,
                  'callback': self.doGetPosHpr
                 },
          'collisionsoff': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doCollisionsOff
                  },
          'collisionson': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'callback': self.doCollisionsOn
                  },
          'xyz': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'argTypes': [(float, True), (float, True), (float, True)],
                  'callback': self.doXyz
                  },
          'hpr': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'argTypes': [(float, True), (float, True), (float, True)],
                  'callback': self.doHpr
                  },
          'warp': {
                  'target': TARGET_OTHER,
                  'access': ACCESS_MOD,
                  'callback': self.doWarp
                  },
          'buykart': {
                  'target': TARGET_SELF,
                  'access': ACCESS_MOD,
                  'argTypes': [(int, True)],
                  'callback': self.doBuyKart
                  }
        }
        self.cr.mwDispatcher.merge(words)

    def doBuyKart(self, av, target, args):
        body = args[0]

        if base.wantKarts:
            def doShtikerLater(task):
                base.localAvatar.addKartPage()
                return 0

            if base.localAvatar.hasKart():
                response = 'Returning Kart %s' % base.localAvatar.getKartBodyType()
                base.localAvatar.requestKartDNAFieldUpdate(KartDNA.bodyType, InvalidEntry)
                return response
            else:
                base.localAvatar.requestKartDNAFieldUpdate(KartDNA.rimsType, getDefaultRim())
                taskMgr.doMethodLater(1.0, doShtikerLater, 'doShtikerLater')

            response = 'Kart %s has been purchased with body and accessory color %s.' % (body, getDefaultColor())
            base.localAvatar.requestKartDNAFieldUpdate(KartDNA.bodyType, int(body))
            return response
        else:
            return 'Enable wantKarts in Config.prc'

    def doOobe(self, av, target, args):
        base.oobe()

    def doOobeCull(self, av, target, args):
        base.oobeCull()

    def doRun(self, av, target, args):
        if config.GetBool('want-running', 1):
            inputState.set('debugRunning', inputState.isSet('debugRunning') != True)

    def doTex(self, av, target, args):
        if len(args) <= 1:
            if self.texViewer:
                self.texViewer.cleanup()
                self.texViewer = None
                return
            base.toggleTexture()
            return
        if self.texViewer:
            self.texViewer.cleanup()
            self.texViewer = None
        tex = TexturePool.findTexture(args[1])
        if not tex:
            tex = TexturePool.findTexture('*%s*' % args[1])
        if not tex:
            self.magicWordResponseString('Unknown texture: %s' % args[1])
            return
        self.texViewer = TexViewer(tex)

    def doTexMem(self, av, target, args):
        base.toggleTexMem()

    def doVerts(self, av, target, args):
        base.toggleShowVertices()

    def doWire(self, av, target, args):
        base.toggleWireframe()

    def doStereo(self, av, target, args):
        base.toggleStereo()

    def doAvId(self, av, target, args):
        print(target.doId)
        return str(target.doId)
        
    def doEndgame(self, av, target, args):
        messenger.send('minigameAbort')
        
    def doWingame(self, av, target, args):
        messenger.send('minigameVictory')
        
    def doWalk(self, av, target, args):
        try:
            fsm = base.cr.playGame.getPlace().fsm
            fsm.forceTransition('walk')
        except:
            pass
            
    def doFps(self, av, target, args):
        if base.frameRateMeter:
            base.setFrameRateMeter(False)
        else:
            base.setFrameRateMeter(True)
            
    def doGetPos(self, av, target, args):
        pos = target.getPos()
        print(pos)
        return str(pos)
 
    def doGetHpr(self, av, target, args):
        hpr = target.getHpr()
        print(hpr)
        return str(hpr)

    def doGetPosHpr(self, av, target, args):
        posHpr = target.getPosHpr()
        print(posHpr)
        return str(posHpr)
        
    def doCamPosHpr(self, av, target, args):
        pos = base.camera.getPos()
        hpr = base.camera.getHpr()
        print('pos: %s hpr: %s' % (pos, hpr))
        return 'pos: %s hpr: %s' % (pos, hpr)

    def doCollisionsOff(self, av, target, args):
        base.localAvatar.collisionsOff()
        return 'Collisions are off.'

    def doCollisionsOn(self, av, target, args):
        base.localAvatar.collisionsOn()
        return 'Collisions are on.'   
        
    def doXyz(self, av, target, args):
        x, y, z, = args[0], args[1], args[2]
        base.localAvatar.setPos(x, y, z)
        
    def doHpr(self, av, target, args):
        h, p, r = args[0], args[1], args[2]
        base.localAvatar.setPos(h, p, r)
        
    def doWarp(self, av, target, args):
        target.setPosHpr(av.getPos(), av.getHpr())

    def disable(self):
        DistributedObject.disable(self)
        self.ignoreAll()

    def setLastClickedAvId(self, av):
        if av:
            if isinstance(av, Toon.Toon) or isinstance(av, FriendHandle.FriendHandle):
                if hasattr(av, 'doId'):
                    self.lastClickedAvId = av.doId
                else:
                    self.lastClickedAvId = 0
                return
        self.lastClickedAvId = 0

    def doMagicWord(self, mwString):
        avAccess = base.localAvatar.getAccessLevel()
        if avAccess < MIN_MAGIC_WORD_ACCESS:
            return
        if mwString.startswith('~~'):
            mwString = mwString[2:]
            if self.lastClickedAvId:
                targetId = self.lastClickedAvId
            else:
                targetId = base.localAvatar.doId
        elif mwString.startswith('~'):
            mwString = mwString[1:]
            targetId = base.localAvatar.doId

        if targetId not in base.cr.doId2do:
            return

        target = base.cr.doId2do[targetId]

        wordName, extraArgs = (mwString.split(' ', 1) + [''])[:2]
        wordName = wordName.lower()

        word = self.cr.mwDispatcher.getWord(wordName)
        if not word:
            return self.sendUpdate('doMagicWordAI', [mwString, targetId])

        minAccess = self.cr.mwDispatcher.getAccess(wordName)
        if avAccess < minAccess:
            return self.magicWordResponseCode(6)

        valid, response, parsedArgs = self.cr.mwDispatcher.checkIfWordIsValid(wordName, base.localAvatar, target, extraArgs)
        if not valid:
            return self.magicWordResponseCode(response)

        callback = self.cr.mwDispatcher.getCallback(wordName)

        try:
            callbackResponse = callback(base.localAvatar, target, parsedArgs)
            if callbackResponse:
                if type(callbackResponse) == str:
                    self.magicWordResponseString(callbackResponse)
                else:
                    self.magicWordResponseCode(callbackResponse)
        except:
            info = describeException()
            self.magicWordResponseString(info)

    # TODO: settings option for chat or system
    # TODO: magic word system messages should be unique

    def magicWordResponseString(self, responseStr):
        character = random.choice(MagicWordLocalizer.CharacterNames)
        base.localAvatar.setSystemMessage(0, '%s: ' % MagicWordLocalizer.MagicianName.format(character) + responseStr)

    def magicWordResponseCode(self, responseCode):
        try:
            response = MagicWordLocalizer.ResponseCode2String[responseCode]
        except:
            return
        character = random.choice(MagicWordLocalizer.CharacterNames)
        base.localAvatar.setSystemMessage(0, '%s: ' % MagicWordLocalizer.MagicianName.format(character) + response)