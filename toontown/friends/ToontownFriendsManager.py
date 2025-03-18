from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class ToontownFriendsManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ToontownFriendsManager')

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def avatarDetailsResp(self, details):
        dg = PyDatagram(details)
        di = PyDatagramIterator(dg)
        self.cr.handleGetAvatarDetailsResp(di)

    def d_getFriendsListRequest(self):
        self.sendUpdate('getFriendsListRequest')

    def friendsListRequestResp(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, commonChatFlags, whitelistChatFlags, alert = True):
        base.cr.handleFriendOnline(id, commonChatFlags, whitelistChatFlags, alert)

    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def friendOffline(self, id, alert=True):
        base.cr.handleFriendOffline(id, alert)

    def friendInvisible(self, id, invisible, alert):
        base.cr.handleFriendInvisible(id, invisible, alert)

    def d_toggleInvisible(self, invisible):
        self.sendUpdate('toggleInvisible', [invisible])