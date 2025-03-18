from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class TTPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    notify = directNotify.newCategory('TTPlayerFriendsManagerUD')

