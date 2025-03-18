from otp.uberdog.SpeedchatRelayUD import SpeedchatRelayUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class TTSpeedchatRelayUD(SpeedchatRelayUD):
    notify = directNotify.newCategory('TTSpeedchatRelayUD')

