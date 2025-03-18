from panda3d.direct import DCPacker
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM
from direct.distributed.MsgTypes import CLIENTAGENT_DECLARE_OBJECT, CLIENTAGENT_UNDECLARE_OBJECT
import functools, pickle, time

class GetAvatarInfoOperation(FSM):

    def __init__(self, mgr, senderId, avId, callback):
        FSM.__init__(self, 'GetAvatarInfoOperation')
        self.mgr = mgr
        self.senderId = senderId
        self.avId = avId
        self.callback = callback
        self.isPet = False

    def start(self):
        self.demand('GetAvatarInfo')

    def enterGetAvatarInfo(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.avId, self.__gotAvatarInfo)

    def __gotAvatarInfo(self, dclass, fields):
        if dclass not in (self.mgr.air.dclassesByName['DistributedToonUD'], self.mgr.air.dclassesByName['DistributedPetAI']):
            self.demand('Failure', 'Invalid dclass for avId %d' % self.avId)
            return

        self.isPet = dclass == self.mgr.air.dclassesByName['DistributedPetAI']
        self.dclass = dclass
        self.fields = fields
        self.fields['avId'] = self.avId
        self.demand('Finished')

    def enterFinished(self):
        if not self.isPet:
            self.mgr.avBasicInfoCache[self.avId] = {'expire': time.time() + config.GetInt('friend-detail-cache-expire', 3600), 'avInfo': [self.avId, self.fields['setName'][0], self.fields['setDNAString'][0], self.fields['setPetId'][0]]}

        self.callback(success = True, avId = self.senderId, dclass = self.dclass, fields = self.fields, isPet = self.isPet)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success = False, avId = None, dclass = None, fields = None, isPet = False)

class GetFriendsListOperation(FSM):

    def __init__(self, mgr, avId, callback):
        FSM.__init__(self, 'GetFriendsListOperation')

        self.mgr = mgr
        self.avId = avId
        self.callback = callback

        self.friendsDetails = []
        self.iterated = 0
        self.operations = {}
        self.onlineFriends = []

    def start(self):
        self.demand('GetFriendsList')

    def enterGetFriendsList(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.avId, self.__gotFriendsList)

    def __gotFriendsList(self, dclass, fields):
        if self.state != 'GetFriendsList':
            self.demand('Failure', '__gotFriendsList called when looking for friends list, avId %d' % self.avId)
            return

        if dclass != self.mgr.air.dclassesByName['DistributedToonUD']:
            self.demand('Failure', 'Invalid dclass for avId %d' % self.avId)
            return

        self.friendsList = fields['setFriendsList'][0]
        self.demand('GetFriendDetails')

    def enterGetFriendDetails(self):
        if len(self.friendsList) <= 0:
            self.callback(success = False, avId = self.avId, friendsDetails = None, onlineFriends = None)
            return

        for friendId, trueFriend in self.friendsList:
            details = self.mgr.avBasicInfoCache.get(friendId)
            if details:
                expire = details.get('expire')
                avInfo = details.get('avInfo')
                if expire and avInfo:
                    if expire > time.time():
                        self.friendsDetails.append(avInfo)
                        self.iterated += 1
                        self.__testFinished()
                        continue
                    else:
                        del self.mgr.avBasicInfoCache[friendId]

            newOperation = GetAvatarInfoOperation(self.mgr, self.avId, friendId, self.__gotAvatarInfo)
            newOperation.start()
            self.operations[friendId] = newOperation

    def __gotAvatarInfo(self, success, avId, dclass, fields, isPet):
        if fields['avId'] in self.operations:
            del self.operations[fields['avId']]

        if not success:
            self.demand('Failure', '__gotAvatarInfo received unsuccessful callback, avId=%d' % self.avId)
            return

        if self.state != 'GetFriendDetails':
            self.demand('Failure', '__gotAvatarInfo while not looking for friends details, avId=%d' % self.avId)
            return

        if avId != self.avId:
            self.demand('Failure', '__gotAvatarInfo response for wrong requester. wrongId=%d, rightId=%d' % (self.avId, avId))
            return

        self.iterated += 1
        self.friendsDetails.append([fields['avId'], fields['setName'][0], fields['setDNAString'][0], fields['setPetId'][0]])
        self.__testFinished()

    def __testFinished(self):
        if self.iterated >= len(self.friendsList) and len(self.operations) == 0:
            self.demand('CheckFriendsOnline')

    def enterCheckFriendsOnline(self):
        self.iterated = 0
        for friendId, trueFriend in self.friendsList:
            self.mgr.air.getActivated(friendId, self.__gotActivatedResp)

    def __gotActivatedResp(self, avId, activated):
        self.iterated += 1
        if activated:
            self.onlineFriends.append(avId)

        if self.iterated == len(self.friendsList):
            self.demand('Finished')

    def enterFinished(self):
        self.callback(success = True, avId = self.avId, friendsDetails = self.friendsDetails, onlineFriends = self.onlineFriends)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success = False, avId = self.avId, friendsDetails = None, onlineFriends = None)

class UpdateAvatarFieldOperation(FSM):

    def __init__(self, mgr, senderId, avId, callback):
        FSM.__init__(self, 'UpdateAvatarFieldOperation')

        self.mgr = mgr
        self.senderId = senderId
        self.avId = avId
        self.callback = callback

        self.field = None
        self.value = None

    def start(self, field, value):
        self.field = field
        self.value = value
        self.demand('GetAvatarOnline')

    def enterGetAvatarOnline(self):
        self.mgr.air.getActivated(self.avId, self.__avatarOnlineResp)

    def __avatarOnlineResp(self, avId, activated):
        if self.state != 'GetAvatarOnline':
            self.demand('Failure', 'Received __avatarOnlineResp while not in GetAvatarOnline state.')
            return

        self.online = activated
        self.demand('UpdateAvatarField')

    def enterUpdateAvatarField(self):
        if self.online:
            dg = self.mgr.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(self.field, self.avId, self.avId, self.mgr.air.ourChannel, [self.value])
            self.mgr.air.send(dg)
        else:
            self.mgr.air.dbInterface.updateObject(self.mgr.air.dbId, self.avId, self.mgr.air.dclassesByName['DistributedToonUD'], {self.field: [self.value]})

        self.demand('Finished')

    def enterFinished(self):
        self.callback(success = True, avId = self.senderId, online = self.online)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success = False)

class ToontownFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ToontownFriendsManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.operations = {}
        self.avBasicInfoCache = {}
        self.invisibleToons = []
        self.invisibleToonCooldowns = {}

        # Accept net mesenger messages:
        self.air.netMessenger.accept('avatarOnline', self, self.comingOnline)
        self.air.netMessenger.accept('avatarInvisible', self, self.avatarInvisible)
        self.air.netMessenger.accept('avatarOffline', self, self.goingOffline)

    def deleteOperation(self, avId):
        operation = self.operations.get(avId)
        if not operation:
            self.notify.debug('%s tried to delete non-existent operation!' % avId)
            return

        if operation.state != 'Off':
            operation.demand('Off')

        del self.operations[avId]

    def getFriendsListRequest(self):
        avId = self.air.getAvatarIdFromSender()

        if not avId:
            return

        if avId in self.operations:
            return

        newOperation = GetFriendsListOperation(self, avId, self.__gotFriendsList)
        newOperation.start()
        self.operations[avId] = newOperation

    def __gotFriendsList(self, success, avId, friendsDetails, onlineFriends):
        self.deleteOperation(avId)

        if not success:
            return

        self.sendUpdateToAvatarId(avId, 'friendsListRequestResp', [friendsDetails])

        for friendId in onlineFriends:
            if friendId in self.invisibleToons:
                self.sendUpdateToAvatarId(avId, 'friendInvisible', [friendId, 1, 0])
            else:
                self.sendUpdateToAvatarId(avId, 'friendOnline', [friendId, 0, 0])

    def getAvatarDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if not senderId:
            return

        if senderId in self.operations:
            return

        newOperation = GetAvatarInfoOperation(self, senderId, avId, self.__gotAvatarDetails)
        newOperation.start()
        self.operations[senderId] = newOperation

    def __gotAvatarDetails(self, success, avId, dclass, fields, isPet):
        self.deleteOperation(avId)

        dg = PyDatagram()
        dg.addUint32(fields['avId'])
        dg.addUint8(0 if success else 1)

        if success:
            # Pack our details into the datagram.
            details = self.packAvatarDetails(dclass, fields)
            dg.appendData(details)

        # Reply to the avatar.
        self.sendUpdateToAvatarId(avId, 'avatarDetailsResp', [dg.getMessage()])

    def packAvatarDetails(self, dclass, fields):
        # Pack required fields.
        fieldPacker = DCPacker()
        for i in range(dclass.getNumInheritedFields()):
            field = dclass.getInheritedField(i)
            if not field.isRequired() or field.asMolecularField():
                continue

            k = field.getName()
            v = fields.get(k, None)

            fieldPacker.beginPack(field)
            if not v:
                fieldPacker.packDefaultValue()
            else:
                field.packArgs(fieldPacker, v)

            fieldPacker.endPack()

        return fieldPacker.getBytes()

    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId in self.operations:
            return

        newOperation = GetAvatarInfoOperation(self, avId, avId, functools.partial(self.__handleRemoveFriend, friendId = friendId))
        newOperation.start()
        self.operations[avId] = newOperation

    def __handleRemoveFriend(self, success, avId, dclass, fields, isPet, friendId = None, final = False):
        self.deleteOperation(avId)

        if not (success and friendId):
            return

        if fields['avId'] not in [avId, friendId]:
            self.notify.warning('__handleRemoveFriend received wrong Toon fields from DB, avId=%d' % avId)
            return

        friendsList = fields['setFriendsList'][0]
        searchId = avId if final else friendId
        for index, friend in enumerate(friendsList):
            if friend[0] == searchId:
                del friendsList[index]
                break

        newOperation = UpdateAvatarFieldOperation(self, avId, friendId if final else avId, functools.partial(self.__handleFriendRemoved, friendId = friendId, final = final))
        newOperation.start('setFriendsList', friendsList)
        self.operations[avId] = newOperation

    def __handleFriendRemoved(self, success, avId, online = False, friendId = None, final = False):
        self.deleteOperation(avId)

        if not (success and friendId):
            return

        if not final:
            newOperation = GetAvatarInfoOperation(self, avId, friendId, functools.partial(self.__handleRemoveFriend, friendId = friendId, final = True))
            newOperation.start()
            self.operations[avId] = newOperation
        else:
            if online:
                dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate('friendsNotify', friendId, friendId, self.air.ourChannel, [avId, 1])
                self.air.send(dg)

    def comingOnline(self, avId, friendId):
        self.air.getActivated(friendId, functools.partial(self.__comingOnlineFriendOnline, otherId = avId, declareObjects = True))

    def __comingOnlineFriendOnline(self, avId, activated, otherId = None, declareObjects=True):
        if not (otherId and activated):
            return

        if declareObjects:
            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
            dg.addUint32(otherId)
            dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
            self.air.send(dg)

            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(otherId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
            dg.addUint32(avId)
            dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
            self.air.send(dg)

        # Tell the client that their friend is online.
        
        if otherId in self.invisibleToons:
            self.sendUpdateToAvatarId(avId, 'friendInvisible', [otherId, 1, 0])
        else:
            self.sendUpdateToAvatarId(avId, 'friendOnline', [otherId, 0, 0])
        
    def avatarInvisible(self, avId):
        self.invisibleToons.append(avId)
        
    def toggleInvisible(self, invisible):
        avId = self.air.getAvatarIdFromSender()
        
        if avId in self.invisibleToonCooldowns:
            elapsed = time.time() - self.invisibleToonCooldowns[avId]
            if elapsed < 10:
                try:
                    dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate('invisibleCallback', avId, avId, self.air.ourChannel, [2])
                    self.air.send(dg)
                except:
                    pass
                return
        
        newOperation = GetAvatarInfoOperation(self, avId, avId, functools.partial(self.__handleAvatarInvisible, invisible = invisible))
        newOperation.start()
        
    def __handleAvatarInvisible(self, success, avId, dclass, fields, isPet, invisible):
        if invisible:
            if avId not in self.invisibleToons:
                self.invisibleToons.append(avId)
            for friendId, trueFriend in fields['setFriendsList'][0]:
                self.air.getActivated(friendId, functools.partial(self.__handleGoneInvisible, otherId = avId, accId = fields['setDISLid'][0]))
        else:
            if avId in self.invisibleToons:
                self.invisibleToons.remove(avId)
            for friendId, trueFriend in fields['setFriendsList'][0]:
                self.air.getActivated(friendId, functools.partial(self.__comingOnlineFriendOnline, otherId = avId, declareObjects = False))
        
        self.invisibleToonCooldowns[avId] = time.time()
                
        newOperation = UpdateAvatarFieldOperation(self, avId, avId, functools.partial(self.__handleAvatarInvisibleUpdate, invisible = invisible))
        newOperation.start('setInvisibleMode', invisible)
        self.operations[avId] = newOperation

    def __handleAvatarInvisibleUpdate(self, success, avId, online = False, invisible=True):
        self.deleteOperation(avId)    
    
        if online:
            dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate('invisibleCallback', avId, avId, self.air.ourChannel, [invisible])
            self.air.send(dg)            

    def goingOffline(self, avId):
        newOperation = GetAvatarInfoOperation(self, avId, avId, self.__handleGoingOffline)
        newOperation.start()

    def __handleGoingOffline(self, success, avId, dclass, fields, isPet):
        if not success:
            return
        
        alert = 1
        if avId in self.invisibleToons:
            self.invisibleToons.remove(avId)
            alert = 0

        for friendId, trueFriend in fields['setFriendsList'][0]:
            self.air.getActivated(friendId, functools.partial(self.__handleGoneOffline, otherId = avId, accId = fields['setDISLid'][0], alert = alert))
            
    def __handleGoneInvisible(self, avId, activated, otherId = None, accId = None):
        if not (otherId and activated and accId):
            return
        self.sendUpdateToAvatarId(avId, 'friendInvisible', [otherId, 1, 1])

    def __handleGoneOffline(self, avId, activated, otherId = None, accId = None, alert = 1):
        if not (otherId and activated and accId):
            return

        # Undeclare to the friend.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(otherId)
        self.air.send(dg)

        # Undeclare to the now-offline avId.
        dg = PyDatagram()
        dg.addServerHeader(self.GetAccountConnectionChannel(accId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(avId)
        self.air.send(dg)

        # Tell them they're offline.
        self.sendUpdateToAvatarId(avId, 'friendOffline', [otherId, alert])

    def clearList(self, avId):
        newOperation = GetAvatarInfoOperation(self, avId, avId, self.__handleClearListGotFriendsList)
        newOperation.start()
        self.operations[avId] = newOperation

    def __handleClearListGotFriendsList(self, success, avId, fields, isPet):
        if not success:
            return

        if avId != fields['avId']:
            return

        friendIds = fields['setFriendsList'][0][:]
        friendIds.append((avId, 1))
        if friendIds[0][0] == avId:
            return

        newOperation = GetAvatarInfoOperation(self, avId, friendIds[0][0], functools.partial(self.__handleClearListGotFriendData, friendIds = friendIds[1:]))
        newOperation.start()
        self.operations[avId] = newOperation

    def __handleClearListGotFriendData(self, success, avId, fields, isPet, friendIds = []):
        self.deleteOperation(avId)

        if not success:
            if friendIds:
                newOperation = GetAvatarInfoOperation(self, avId, friendIds[0][0], functools.partial(self.__handleClearListGotFriendData, friendIds = friendIds[1:]))
                newOperation.start()
                self.operations[avId] = newOperation
            else:
                return

        friendsIds = fields['setFriendsList'][0][:]
        if avId == fields['avId']:
            friendsIds = []
        else:
            for friend in friendsIds:
                if friend[0] == avId:
                    friendsIds.remove(friend)

        newOperation = UpdateAvatarFieldOperation(self, avId, fields['avId'], functools.partial(self.__handleClearListUpdatedAvatarField, friendId = fields['avId'], friendIds = friendIds[1:]))
        newOperation.start('setFriendsList', friendsIds)
        self.operations[avId] = newOperation

    def __handleClearListUpdatedAvatarField(self, success, avId, online = False, friendId = None, friendIds = []):
        self.deleteOperation(avId)

        if success and online:
            dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate('friendsNotify', friendId, friendId, self.air.ourChannel, [avId, 1])
            self.air.send(dg)

        if not friendIds:
            return

        newOperation = GetAvatarInfoOperation(self, avId, friendIds[0][0], functools.partial(self.__handleClearListGotFriendData, friendIds = friendIds[1:]))
        newOperation.start()
        self.operations[avId] = newOperation
