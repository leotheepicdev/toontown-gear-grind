from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.pets import PetDNA
from toontown.pets import PetUtil
from toontown.pets.PetNameGenerator import PetNameGenerator

import json, os, random, time

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

def getDayId():
    return int(time.time() // DAY)

class PetManagerAI:
    notify = directNotify.newCategory('PetManagerAI')
    cachePath = config.GetString('air-pet-cache', 'backups/pets/')

    def __init__(self, air):
        self.air = air
        self.cacheFile = '{0}pets_{1}.pets'.format(self.cachePath, self.air.districtId)

        if not os.path.exists(self.cachePath):
            os.makedirs(self.cachePath)

        if os.path.isfile(self.cacheFile):
            with open(self.cacheFile, 'rb') as f:
                data = f.read()

            try:
                self.seeds = json.loads(data)
            except ValueError:
                self.seeds = {}

            if self.seeds.get('day', -1) != getDayId():
                self.seeds = {}
        else:
            self.seeds = {}

        self.nameGenerator = PetNameGenerator()

    def getAvailablePets(self, firstNumPets, secondNumPets):
        numPets = firstNumPets + secondNumPets

        if not self.seeds.get(str(numPets), []) or self.seeds.get('day', -1) != getDayId():
            self.seeds[str(numPets)] = random.sample(range(256), numPets)
            self.updatePetSeedCache()

        return self.seeds.get(str(numPets), [numPets])[0:numPets]

    def updatePetSeedCache(self):
        self.seeds['day'] = getDayId()

        with open(self.cacheFile, 'w', encoding='utf8') as f:
            f.write(json.dumps(self.seeds))

    def createNewPetFromSeed(self, avId, seed, nameIndex, gender, safeZoneId):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        petName = self.nameGenerator.getName(nameIndex)
        _, dna, traitSeed = PetUtil.getPetInfoFromSeed(seed, safeZoneId)
        head, ears, nose, tail, bodyTexture, color, colorScale, eyeColor, _, hat = dna
        numGenders = len(PetDNA.PetGenders)
        gender %= numGenders
        fields = {'setOwnerId': avId, 'setPetName': petName, 'setTraitSeed': traitSeed, 'setSafeZone': safeZoneId,
                  'setHead': head, 'setEars': ears, 'setNose': nose, 'setTail': tail, 'setBodyTexture': bodyTexture,
                  'setColor': color, 'setColorScale': colorScale, 'setEyeColor': eyeColor, 'setGender': gender, 
                  'setHat': (hat[0], hat[1], hat[2])
                  }

        def response(doId):
            if not doId:
                self.notify.warning('Cannot create pet for %s!' % avId)
                return

            self.air.writeServerEvent('bought-pet', avId = avId, petId = doId)
            av.b_setPetId(doId)
            
        createFields = {}
        for key, value in list(fields.items()):
            if type(value) == tuple:
                createFields[key] = value
            else:
                createFields[key] = (value,)
                

        self.air.dbInterface.createObject(self.air.dbId, self.air.dclassesByName['DistributedPetAI'],
                                          createFields, response)

    def deleteToonsPet(self, avId):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        petId = av.getPetId()
        pet = self.air.doId2do.get(petId)

        if pet:
            pet.requestDelete()

        av.b_setPetId(0)
        self.air.writeServerEvent('returned-pet', avId = avId, petId = petId)
