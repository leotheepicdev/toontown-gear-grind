from toontown.safezone import DistributedSZTreasure
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3
Models = {ToontownGlobals.ToontownCentral: 'phase_4/models/props/ttcTreasure',
 ToontownGlobals.DonaldsDock: 'phase_4/models/props/ddlTreasure',
 ToontownGlobals.TheBrrrgh: 'phase_4/models/props/tbTreasure',
 ToontownGlobals.MinniesMelodyland: 'phase_4/models/props/mmlTreasure',
 ToontownGlobals.DaisyGardens: 'phase_4/models/props/dgTreasure',
 ToontownGlobals.DonaldsDreamland: 'phase_4/models/props/ddlTreasure'}

class DistributedCashbotBossTreasure(DistributedSZTreasure.DistributedSZTreasure):

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        self.hoodId = 0

    def setStyle(self, hoodId):
        newModel = Models[hoodId]
        self.hoodId = hoodId
        if self.modelPath != newModel:
            if self.modelPath:
                self.loadModel(newModel)
            self.modelPath = newModel
            
    def loadModel(self, modelPath, modelFindString=None):
        if self.hoodId == ToontownGlobals.MinniesMelodyland:
            modelFindString = 'note%s' % str(self.getVariant() + 1)
        elif self.hoodId == ToontownGlobals.TheBrrrgh:
            modelFindString = 'flake%s' % str(self.getVariant() + 1) 
    
        DistributedSZTreasure.DistributedSZTreasure.loadModel(self, modelPath, modelFindString)

        if self.hoodId == ToontownGlobals.ToontownCentral:     
            if self.getVariant() == 1:
                self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce1.png'), 1)
                self.treasure.find('**/cone').setTexture(loader.loadTexture('phase_4/maps/chocolate_cone.png'), 1)
            elif self.getVariant() == 2:
                self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce2.png'), 1)
            elif self.getVariant() == 3:
                self.treasure.find('**/cream').setTexture(loader.loadTexture('phase_4/maps/icecreamChestIce3.png'), 1)
        elif self.hoodId == ToontownGlobals.DonaldsDock:
            if self.getVariant() == 1:
                self.treasure.setTexture(loader.loadTexture('phase_4/maps/starfish_orange.png'), 1)
            elif self.getVariant() == 2:
                self.treasure.setTexture(loader.loadTexture('phase_4/maps/starfish_pink.png'), 1)
        elif self.hoodId == ToontownGlobals.DaisyGardens:
            if self.getVariant() == 1:
                self.treasure.find('**/pedals').setColorScale(0.975, 0.382, 0, 1)
            elif self.getVariant() == 2:
                self.treasure.find('**/pedals').setColorScale(1, 1, 0, 1)
            elif self.getVariant() == 3:
                self.treasure.find('**/pedals').setColorScale(0.85, 0.61, 0.75, 1)
        elif self.hoodId == ToontownGlobals.DonaldsDreamland:
                self.treasure.setColorScale(0.99, 0.894, 0.3137, 1)        

    def setGoonId(self, goonId):
        self.goonId = goonId

    def setFinalPosition(self, x, y, z):
        if not self.nodePath:
            self.makeNodePath()
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        startPos = None
        goon = self.cr.doId2do[self.goonId]
        if goon:
            startPos = goon.getPos()
        lerpTime = 1
        self.treasureFlyTrack = Sequence(Func(self.collNodePath.stash), Parallel(ProjectileInterval(self.treasure, startPos=Point3(0, 0, 0), endPos=Point3(0, 0, 0), duration=lerpTime, gravityMult=2.0), LerpPosInterval(self.nodePath, lerpTime, Point3(x, y, z), startPos=startPos)), Func(self.collNodePath.unstash))
        self.treasureFlyTrack.start()
        return
