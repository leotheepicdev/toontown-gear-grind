from toontown.estate import HouseGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from . import CatalogItem

class CatalogHousePaintItem(CatalogItem.CatalogItem):

    def makeNewItem(self, houseColor):
        self.houseColor = houseColor
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 1
        
    def output(self, store=-1):
        return 'CatalogHousePaintItem(%s%s)' % (self.houseColor, self.formatOptionalData(store))

    def getTypeName(self):
        return TTLocalizer.HousePaintTypeName

    def getName(self):
        return TTLocalizer.HousePaintTypeName
        
    def getDisplayName(self):
        return TTLocalizer.HouseColorNames[self.houseColor]

    def getPicture(self, avatar):
        self.model = loader.loadModel('phase_5.5/models/estate/houseA')
        self.model.setBin('unsorted', 0, 1)
        self.model.find('**/mat').removeNode()
        color = HouseGlobals.houseColors[self.houseColor]
        dark = (0.8 * color[0], 0.8 * color[1], 0.8 * color[2])
        self.model.find('**/*back').setColor(color[0], color[1], color[2], 1)
        self.model.find('**/*front').setColor(color[0], color[1], color[2], 1)
        self.model.find('**/*right').setColor(dark[0], dark[1], dark[2], 1)
        self.model.find('**/*left').setColor(dark[0], dark[1], dark[2], 1)
        color = HouseGlobals.houseColors2[self.houseColor]
        chimneyList = self.model.findAllMatches('**/chim*')
        for chimney in chimneyList:
            chimney.setColor(color[0], color[1], color[2], 1)

        self.model.setH(180)
        self.hasPicture = True
        return self.makeFrameModel(self.model)

    def cleanupPicture(self):
        CatalogItem.CatalogItem.cleanupPicture(self)
        self.model.detachNode()
        self.model = None

    def reachedPurchaseLimit(self, avatar):
        if avatar.onOrder.count(self) != 0:
            return 1
        if avatar.onGiftOrder.count(self) != 0:
            return 1
        if avatar.mailboxContents.count(self) != 0:
            return 1
        if self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        if avatar.getHouseColor() == self.houseColor:
            return 1
        return 0
        
    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.houseColor = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.houseColor)
        
    def getBasePrice(self):
        return 2000

    def getDeliveryTime(self):
        return 1

    def isGift(self):
        return False

    def getDaysToGo(self, avatar):
        return 0

    def loyaltyRequirement(self):
        return 0

    def recordPurchase(self, avatar, optional):
        if avatar:
            house = simbase.air.doId2do.get(avatar.getHouseId())
            if house:
                avatar.b_setHouseColor(self.houseColor)
                house.b_setColor(self.houseColor)
        return ToontownGlobals.P_ItemAvailable
