from panda3d.core import *
from lib.libotp import WhisperPopup
from lib.libotp import CFQuicktalker, CFPageButton, CFQuitButton, CFSpeech, CFThought, CFTimeout
from otp.chat import ChatGarbler
import string
from direct.task import Task
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from direct.showbase import PythonUtil
from otp.avatar import DistributedAvatar
import time
from otp.avatar import Avatar, PlayerBase
from otp.chat import TalkAssistant
from otp.otpbase import OTPGlobals
from otp.avatar.Avatar import teleportNotify
from otp.distributed.TelemetryLimited import TelemetryLimited
if base.config.GetBool('want-chatfilter-hacks', 0):
    from otp.switchboard import badwordpy
    import os
    badwordpy.init(os.environ.get('OTP') + '\\src\\switchboard\\', '')

class DistributedPlayer(DistributedAvatar.DistributedAvatar, PlayerBase.PlayerBase, TelemetryLimited):
    TeleportFailureTimeout = 60.0
    chatGarbler = ChatGarbler.ChatGarbler()

    def __init__(self, cr):
        try:
            self.DistributedPlayer_initialized
        except:
            self.DistributedPlayer_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            PlayerBase.PlayerBase.__init__(self)
            TelemetryLimited.__init__(self)
            self.__teleportAvailable = 0
            self.inventory = None
            self.experience = None
            self.friendsList = []
            self.oldFriendsList = None
            self.timeFriendsListChanged = None
            self.ignoreList = []
            self.lastFailedTeleportMessage = {}
            self._districtWeAreGeneratedOn = None
            self.DISLname = ''
            self.DISLid = 0
            self.accessLevel = 0
            self.invisibleMode = 0
            self.autoRun = 0
            self.wishNameState = ''
            self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1)

        return

    @staticmethod
    def GetPlayerGenerateEvent():
        return 'DistributedPlayerGenerateEvent'

    @staticmethod
    def GetPlayerNetworkDeleteEvent():
        return 'DistributedPlayerNetworkDeleteEvent'

    @staticmethod
    def GetPlayerDeleteEvent():
        return 'DistributedPlayerDeleteEvent'

    def networkDelete(self):
        DistributedAvatar.DistributedAvatar.networkDelete(self)
        messenger.send(self.GetPlayerNetworkDeleteEvent(), [self])

    def disable(self):
        DistributedAvatar.DistributedAvatar.disable(self)
        messenger.send(self.GetPlayerDeleteEvent(), [self])

    def delete(self):
        try:
            self.DistributedPlayer_deleted
        except:
            self.DistributedPlayer_deleted = 1
            del self.experience
            if self.inventory:
                self.inventory.unload()
            del self.inventory
            DistributedAvatar.DistributedAvatar.delete(self)

    def generate(self):
        DistributedAvatar.DistributedAvatar.generate(self)

    def announceGenerate(self):
        DistributedAvatar.DistributedAvatar.announceGenerate(self)
        messenger.send(self.GetPlayerGenerateEvent(), [self])

    def setLocation(self, parentId, zoneId):
        DistributedAvatar.DistributedAvatar.setLocation(self, parentId, zoneId)
        if not (parentId in (0, None) and zoneId in (0, None)):
            if not self.cr._isValidPlayerLocation(parentId, zoneId):
                self.cr.disableDoId(self.doId)
                self.cr.deleteObject(self.doId)
        return None

    def isGeneratedOnDistrict(self, districtId = None):
        if districtId is None:
            return self._districtWeAreGeneratedOn is not None
        else:
            return self._districtWeAreGeneratedOn == districtId
        return

    def getArrivedOnDistrictEvent(self, districtId = None):
        if districtId is None:
            return 'arrivedOnDistrict'
        else:
            return 'arrivedOnDistrict-%s' % districtId
        return

    def arrivedOnDistrict(self, districtId):
        curFrameTime = globalClock.getFrameTime()
        if hasattr(self, 'frameTimeWeArrivedOnDistrict') and curFrameTime == self.frameTimeWeArrivedOnDistrict:
            if districtId == 0 and self._districtWeAreGeneratedOn:
                self.notify.warning('ignoring arrivedOnDistrict 0, since arrivedOnDistrict %d occured on the same frame' % self._districtWeAreGeneratedOn)
                return
        self._districtWeAreGeneratedOn = districtId
        self.frameTimeWeArrivedOnDistrict = globalClock.getFrameTime()
        messenger.send(self.getArrivedOnDistrictEvent(districtId))
        messenger.send(self.getArrivedOnDistrictEvent())

    def setLeftDistrict(self):
        self._districtWeAreGeneratedOn = None
        return

    def setAccountName(self, accountName):
        self.accountName = accountName

    def setSystemMessage(self, aboutId, chatString, whisperType = WhisperPopup.WTSystem):
        self.displayWhisper(aboutId, chatString, whisperType)

    def displayWhisper(self, fromId, chatString, whisperType):
        print('Whisper type %s from %s: %s' % (whisperType, fromId, chatString))

    def displayWhisperPlayer(self, playerId, chatString, whisperType):
        print('WhisperPlayer type %s from %s: %s' % (whisperType, playerId, chatString))

    def setWhisperSCFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, fromId)

    def _isValidWhisperSource(self, source):
        return True

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if not self._isValidWhisperSource(handle):
            self.notify.warning('displayWhisper from non-toon %s' % fromId)
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, fromId)

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCEmoteWhisperMsg(emoteId, handle.getName())
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTEmote)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_EMOTE, emoteId, fromId)
        return

    def d_setWhisperIgnored(self, sendToId):
        pass

    def setChatAbsolute(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        DistributedAvatar.DistributedAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)
        if not quiet:
            pass

    def b_setChat(self, chatString, chatFlags):
        if self.cr.wantMagicWords and len(chatString) > 0 and chatString[0] == '~':
            messenger.send('magicWord', [chatString])
        else:
            if base.config.GetBool('want-chatfilter-hacks', 0):
                if base.config.GetBool('want-chatfilter-drop-offending', 0):
                    if badwordpy.test(chatString):
                        return
                else:
                    chatString = badwordpy.scrub(chatString)
            messenger.send('wakeup')
            self.setChatAbsolute(chatString, chatFlags)
            self.d_setChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags, 0])

    def setTalk(self, fromAV, fromAC, avatarName, message, flags):
        message = base.talkAssistant.whiteListFilterMessage(message)
        self.displayTalk(message)
        if base.talkAssistant.isThought(message):
            newText = base.talkAssistant.removeThoughtPrefix(newText)
            base.talkAssistant.receiveThought(fromAV, avatarName, fromAC, None, newText, scrubbed)
        else:
            base.talkAssistant.receiveOpenTalk(fromAV, avatarName, fromAC, None, newText, scrubbed)

    def setTalkWhisper(self, fromAV, fromAC, avatarName, message, flags):
        message = base.talkAssistant.whiteListFilterMessage(message)
        self.displayTalkWhisper(fromAV, avatarName, message)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.doId, self.getName(), message, scrubbed=0)

    def displayTalkWhisper(self, fromId, avatarName, chatString):
        print('TalkWhisper from %s: %s' % (fromId, chatString))

    def scrubTalk(self, chat, mods):
        return chat

    def setChat(self, chatString, chatFlags, DISLid):
        self.notify.error('Should call setTalk')
        chatString = base.talkAssistant.whiteListFilterMessage(chatString)
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if base.localAvatar.garbleChat and not self.isUnderstandable():
            chatString = self.chatGarbler.garble(self, chatString)
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        if chatFlags & CFThought:
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= CFSpeech | CFTimeout
        self.setChatAbsolute(chatString, chatFlags)

    def b_setSC(self, msgIndex, cfType=CFSpeech):
        self.setSC(msgIndex, cfType)
        self.d_setSC(msgIndex, cfType)

    def d_setSC(self, msgIndex, cfType=CFSpeech):
        messenger.send('wakeup')
        self.sendUpdate('setSC', [msgIndex, cfType])

    def setSC(self, msgIndex, cfType=CFSpeech):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            if cfType == CFThought:
                self.setChatAbsolute(chatString, cfType | CFQuicktalker, quiet = 1)
            else:
                self.setChatAbsolute(chatString, cfType | CFQuicktalker | CFTimeout, quiet=1)
        if base.localAvatar.chatLog:
            avatar = base.cr.identifyAvatar(self.doId)
            base.localAvatar.chatLog.log(avatar.getName(), chatString)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, self.doId)

    def b_setSCCustom(self, msgIndex):
        self.setSCCustom(msgIndex)
        self.d_setSCCustom(msgIndex)

    def d_setSCCustom(self, msgIndex):
        messenger.send('wakeup')
        self.sendUpdate('setSCCustom', [msgIndex])

    def setSCCustom(self, msgIndex):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, self.doId)

    def b_setSCEmote(self, emoteId):
        self.b_setEmoteState(emoteId, animMultiplier=self.animMultiplier)
        
    def b_setSCDisguiseEmote(self, emoteId):
        self.b_setDisguiseEmoteState(emoteId, animMultiplier=self.animMultiplier)

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        avatar = base.cr.identifyFriend(avId)
        if avatar != None:
            if status == 1:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNoLongerFriend % avatar.getName())
            elif status == 2:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNowSpecialFriend % avatar.getName())
        return
        
    def invisibleCallback(self, invisibleMode):
        if invisibleMode == 1:
            self.setSystemMessage(0, OTPLocalizer.InvisibleSuccess)
        elif invisibleMode == 2:
            self.setSystemMessage(0, OTPLocalizer.InvisibleFailed)
        else:
            self.setSystemMessage(0, OTPLocalizer.VisibleSuccess)

    def iWantToTeleportToSomeone(self, toId):
        self.sendUpdate('iWantToTeleportToSomeone', [toId])

    def someoneWantsToTeleportToMe(self, requesterId, requesterShardId):
        teleportNotify.debug('Avatar Id {0} wants to teleport to me!'.format(requesterId))
        avatar = base.cr.playerFriendsManager.identifyFriend(requesterId)
        if avatar != None:
            teleportNotify.debug('avatar is not None')
            if base.cr.avatarFriendsManager.checkIgnored(requesterId):
                teleportNotify.debug('avatar ignored via avatarFriendsManager')
                self.respondToRequestedTeleport(2, 0, 0, 0, requesterId)
                return
            if requesterId in self.ignoreList:
                teleportNotify.debug('avatar ignored via ignoreList')
                self.respondToRequestedTeleport(2, 0, 0, 0, requesterId)
                return
            if hasattr(base, 'distributedParty'):
                if base.distributedParty.partyInfo.isPrivate:
                    if requesterId not in base.distributedParty.inviteeIds:
                        teleportNotify.debug('avatar not in inviteeIds')
                        self.respondToRequestedTeleport(0, 0, 0, 0, requesterId)
                        return
                if base.distributedParty.isPartyEnding:
                    teleportNotify.debug('party is ending')
                    self.respondToRequestedTeleport(0, 0, 0, 0, requesterId)
                    return
            if self.__teleportAvailable and not self.ghostMode and base.config.GetBool('can-be-teleported-to', 1):
                teleportNotify.debug('teleport initiation successful')
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperComingToVisit % avatar.getName())
                if requesterShardId != base.localAvatar.defaultShard:
                    response = 1
                else:
                    response = 3
                messenger.send('teleportQuery', [response, requesterId])
                return
            teleportNotify.debug('teleport initiation failed')
            if self.failedTeleportMessageOk(requesterId):
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % avatar.getName())
        teleportNotify.debug('sending try-again-later message')
        self.respondToRequestedTeleport(0, 0, 0, 0, requesterId)

    def failedTeleportMessageOk(self, fromId):
        now = globalClock.getFrameTime()
        lastTime = self.lastFailedTeleportMessage.get(fromId, None)
        if lastTime != None:
            elapsed = now - lastTime
            if elapsed < self.TeleportFailureTimeout:
                return 0
        self.lastFailedTeleportMessage[fromId] = now
        return 1

    def respondToRequestedTeleport(self, response, shardId, hoodId, zoneId, requesterId):
        teleportNotify.debug('sending response to our teleport request')
        self.sendUpdate('personRespondedToTeleportRequest', [response, shardId, hoodId, zoneId], requesterId)

    def teleportResponse(self, response, avId, shardId, hoodId, zoneId):
        teleportNotify.debug('received teleportResponse%s' % ((response,
          avId,
          shardId,
          hoodId,
          zoneId),))
        messenger.send('teleportResponse', [response, avId,
         shardId,
         hoodId,
         zoneId])

    def teleportGiveup(self, toId):
        teleportNotify.debug('received teleportGiveup(%s)' % (toId,))
        avatar = base.cr.identifyAvatar(toId)
        if not self._isValidWhisperSource(avatar):
            self.notify.warning('teleportGiveup from non-toon %s' % toId)
            return
        if avatar != None:
            self.setSystemMessage(0, OTPLocalizer.WhisperGiveupVisit % avatar.getName())
        return

    def d_teleportGreeting(self):
        self.sendUpdate('requestTeleportGreeting', [])

    def teleportGreetingSuccess(self, avId):
        avatar = base.cr.getDo(avId)
        if isinstance(avatar, Avatar.Avatar):
            self.setChatAbsolute(OTPLocalizer.TeleportGreetings[self.getTeleportGreeting()] % avatar.getName(), CFSpeech | CFTimeout)
        elif avatar is not None:
            self.notify.warning('got teleportGreetingSuccess from %s referencing non-toon %s' % (self.doId, avId))
            
    def setTeleportGreeting(self, teleportGreeting):
        self.teleportGreeting = teleportGreeting
        if self.isLocal() and self.tutorialAck:
            messenger.send('greetingMessagesChanged')
            
    def setTutorialAck(self, tutorialAck):
        self.tutorialAck = tutorialAck
        
    def getTeleportGreeting(self):
        return self.teleportGreeting

    def setTeleportAvailable(self, available):
        self.__teleportAvailable = available

    def getTeleportAvailable(self):
        return self.__teleportAvailable

    def getFriendsList(self):
        return self.friendsList

    def setFriendsList(self, friendsList):
        self.oldFriendsList = self.friendsList
        self.friendsList = friendsList
        self.timeFriendsListChanged = globalClock.getFrameTime()
        messenger.send('friendsListChanged')
        Avatar.reconsiderAllUnderstandable()
        
    def setInvisibleMode(self, invisibleMode):
        self.invisibleMode = invisibleMode
        messenger.send('updateInvisibleButton', [invisibleMode])

    def getInvisibleMode(self):
        return self.invisibleMode

    def setDISLname(self, name):
        self.DISLname = name

    def setDISLid(self, id):
        self.DISLid = id

    def setAccessLevel(self, accessLevel):
        self.accessLevel = accessLevel

    def getAccessLevel(self):
        return self.accessLevel

    def setAutoRun(self, value):
        self.autoRun = value

    def getAutoRun(self):
        return self.autoRun
        
    def WishNameState(self, wishNameState):
        self.wishNameState = wishNameState
        
    def getWishNameState(self):
        return self.wishNameState
