from direct.directnotify import DirectNotifyGlobal

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyJukeboxActivityBaseAI import DistributedPartyJukeboxActivityBaseAI


class DistributedPartyValentineJukebox40ActivityAI(DistributedPartyJukeboxActivityBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyValentineJukebox40ActivityAI')

    def __init__(self, air, parent, activity):
        DistributedPartyJukeboxActivityBaseAI.__init__(self, air, parent, activity)
        self.music = PartyGlobals.PhaseToMusicData40
