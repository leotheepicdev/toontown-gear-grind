from . import SafeZoneLoader
from . import RRHPlayground
from toontown.toonbase import ToontownGlobals

class RRHSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = RRHPlayground.RRHPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_14/dna/resistance_ranger_hideout_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_14/dna/storage_RRH_sz.dna'
        
    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)
        base.localAvatar.stopSleepWatch()
        
    def createSafeZone(self, dnaFile):
        SafeZoneLoader.SafeZoneLoader.createSafeZone(self, dnaFile)
        aaLinkTunnel = self.geom.find('**/LinkTunnel1')
        aaLinkTunnel.setName('linktunnel_oz_6000_DNARoot')