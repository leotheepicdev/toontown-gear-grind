from direct.directnotify import DirectNotifyGlobal

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyJukeboxActivityBaseAI import DistributedPartyJukeboxActivityBaseAI


class DistributedPartyJukebox40ActivityAI(DistributedPartyJukeboxActivityBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyJukebox40ActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyJukeboxActivityBaseAI.__init__(self, air, parent, activity)
        self.music = PartyGlobals.PhaseToMusicData40
