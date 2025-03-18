from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.util import random
notify = directNotify.newCategory('ToonDNA')
toonSpeciesTypes = ['d',
 'c',
 'h',
 'm',
 'r',
 'f',
 'p',
 'b',
 's']
toonHeadTypes = ['dls',
 'dss',
 'dsl',
 'dll',
 'cls',
 'css',
 'csl',
 'cll',
 'hls',
 'hss',
 'hsl',
 'hll',
 'mls',
 'mss',
 'rls',
 'rss',
 'rsl',
 'rll',
 'fls',
 'fss',
 'fsl',
 'fll',
 'pls',
 'pss',
 'psl',
 'pll',
 'bls',
 'bss',
 'bsl',
 'bll',
 'sls',
 'sss',
 'ssl',
 'sll']

def getHeadList(species):
    headList = []
    for head in toonHeadTypes:
        if head[0] == species:
            headList.append(head)

    return headList


def getHeadStartIndex(species):
    for head in toonHeadTypes:
        if head[0] == species:
            return toonHeadTypes.index(head)


def getSpecies(head):
    for species in toonSpeciesTypes:
        if species == head[0]:
            return species


def getSpeciesName(head):
    species = getSpecies(head)
    if species == 'd':
        speciesName = 'dog'
    elif species == 'c':
        speciesName = 'cat'
    elif species == 'h':
        speciesName = 'horse'
    elif species == 'm':
        speciesName = 'mouse'
    elif species == 'r':
        speciesName = 'rabbit'
    elif species == 'f':
        speciesName = 'duck'
    elif species == 'p':
        speciesName = 'monkey'
    elif species == 'b':
        speciesName = 'bear'
    elif species == 's':
        speciesName = 'pig'
    return speciesName


toonHeadAnimalIndices = [0,
 4,
 8,
 12,
 14,
 18,
 22,
 26,
 30]
toonHeadAnimalIndicesTrial = [0,
 4,
 12,
 14,
 18,
 30]
allToonHeadAnimalIndices = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
 25,
 26,
 27,
 28,
 29,
 30,
 31,
 32,
 33]
allToonHeadAnimalIndicesTrial = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 30,
 31,
 32,
 33]
toonTorsoTypes = ['ss',
 'ms',
 'ls',
 'sd',
 'md',
 'ld',
 's',
 'm',
 'l']
toonLegTypes = ['s', 'm', 'l']
Shirts = ['phase_3/maps/desat_shirt_1.jpg',
 'phase_3/maps/desat_shirt_2.jpg',
 'phase_3/maps/desat_shirt_3.jpg',
 'phase_3/maps/desat_shirt_4.jpg',
 'phase_3/maps/desat_shirt_5.jpg',
 'phase_3/maps/desat_shirt_6.jpg',
 'phase_3/maps/desat_shirt_7.jpg',
 'phase_3/maps/desat_shirt_8.jpg',
 'phase_3/maps/desat_shirt_9.jpg',
 'phase_3/maps/desat_shirt_10.jpg',
 'phase_3/maps/desat_shirt_11.jpg',
 'phase_3/maps/desat_shirt_12.jpg',
 'phase_3/maps/desat_shirt_13.jpg',
 'phase_3/maps/desat_shirt_14.jpg',
 'phase_3/maps/desat_shirt_15.jpg',
 'phase_3/maps/desat_shirt_16.jpg',
 'phase_3/maps/desat_shirt_17.jpg',
 'phase_3/maps/desat_shirt_18.jpg',
 'phase_3/maps/desat_shirt_19.jpg',
 'phase_3/maps/desat_shirt_20.jpg',
 'phase_3/maps/desat_shirt_21.jpg',
 'phase_3/maps/desat_shirt_22.jpg',
 'phase_3/maps/desat_shirt_23.jpg',
 'phase_4/maps/female_shirt1b.jpg',
 'phase_4/maps/female_shirt2.jpg',
 'phase_4/maps/female_shirt3.jpg',
 'phase_4/maps/male_shirt1.jpg',
 'phase_4/maps/male_shirt2_palm.jpg',
 'phase_4/maps/male_shirt3c.jpg',
 'phase_4/maps/shirt_ghost.jpg',
 'phase_4/maps/shirt_pumkin.jpg',
 'phase_4/maps/holiday_shirt1.jpg',
 'phase_4/maps/holiday_shirt2b.jpg',
 'phase_4/maps/holidayShirt3b.jpg',
 'phase_4/maps/holidayShirt4.jpg',
 'phase_4/maps/female_shirt1b.jpg',
 'phase_4/maps/female_shirt5New.jpg',
 'phase_4/maps/shirtMale4B.jpg',
 'phase_4/maps/shirt6New.jpg',
 'phase_4/maps/shirtMaleNew7.jpg',
 'phase_4/maps/femaleShirtNew6.jpg',
 'phase_4/maps/Vday1Shirt5.jpg',
 'phase_4/maps/Vday1Shirt6SHD.jpg',
 'phase_4/maps/Vday1Shirt4.jpg',
 'phase_4/maps/Vday_shirt2c.jpg',
 'phase_4/maps/shirtTieDyeNew.jpg',
 'phase_4/maps/male_shirt1.jpg',
 'phase_4/maps/StPats_shirt1.jpg',
 'phase_4/maps/StPats_shirt2.jpg',
 'phase_4/maps/ContestfishingVestShirt2.jpg',
 'phase_4/maps/ContestFishtankShirt1.jpg',
 'phase_4/maps/ContestPawShirt1.jpg',
 'phase_4/maps/CowboyShirt1.jpg',
 'phase_4/maps/CowboyShirt2.jpg',
 'phase_4/maps/CowboyShirt3.jpg',
 'phase_4/maps/CowboyShirt4.jpg',
 'phase_4/maps/CowboyShirt5.jpg',
 'phase_4/maps/CowboyShirt6.jpg',
 'phase_4/maps/4thJulyShirt1.jpg',
 'phase_4/maps/4thJulyShirt2.jpg',
 'phase_4/maps/shirt_Cat7_01.jpg',
 'phase_4/maps/shirt_Cat7_02.jpg',
 'phase_4/maps/contest_backpack3.jpg',
 'phase_4/maps/contest_leder.jpg',
 'phase_4/maps/contest_mellon2.jpg',
 'phase_4/maps/contest_race2.jpg',
 'phase_4/maps/PJBlueBanana2.jpg',
 'phase_4/maps/PJRedHorn2.jpg',
 'phase_4/maps/PJGlasses2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_valentine1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_valentine2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_desat4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_gardening1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_gardening2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_party1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_party2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racing1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racing2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_summer1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_summer2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_golf1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_golf2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_marathon1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_toonTask1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_toonTask2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trolley1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trolley2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_winter1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween3.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_valentine3.jpg',
 'phase_4/maps/tt_t_chr_shirt_scientistC.jpg',
 'phase_4/maps/tt_t_chr_shirt_scientistA.jpg',
 'phase_4/maps/tt_t_chr_shirt_scientistB.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_mailbox.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trashcan.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_loonyLabs.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_hydrant.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_whistle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_cogbuster.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated01.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_victoryParty01.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_victoryParty02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_sellbotIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_sellbotVPIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_sellbotCrusher.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_jellyBeans.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_doodle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween5.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloweenTurtle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_greentoon1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_getConnectedMoverShaker.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racingGrandPrix.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_lawbotIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_lawbotVPIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_lawbotCrusher.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_bee.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_pirate.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_supertoon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_vampire.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_dinosaur.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_golf03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racing03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding3.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trolley03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_golf04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween06.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_winter03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_halloween07.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_winter02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing06.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_fishing07.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_golf05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racing04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_racing05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trolley04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_trolley05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirt_anniversary.jpg',
 'phase_4/maps/BetaOverallShirt.jpg']

Sleeves = ['phase_3/maps/desat_sleeve_1.jpg',
 'phase_3/maps/desat_sleeve_2.jpg',
 'phase_3/maps/desat_sleeve_3.jpg',
 'phase_3/maps/desat_sleeve_4.jpg',
 'phase_3/maps/desat_sleeve_5.jpg',
 'phase_3/maps/desat_sleeve_6.jpg',
 'phase_3/maps/desat_sleeve_7.jpg',
 'phase_3/maps/desat_sleeve_8.jpg',
 'phase_3/maps/desat_sleeve_9.jpg',
 'phase_3/maps/desat_sleeve_10.jpg',
 'phase_3/maps/desat_sleeve_15.jpg',
 'phase_3/maps/desat_sleeve_16.jpg',
 'phase_3/maps/desat_sleeve_19.jpg',
 'phase_3/maps/desat_sleeve_20.jpg',
 'phase_4/maps/female_sleeve1b.jpg',
 'phase_4/maps/female_sleeve2.jpg',
 'phase_4/maps/female_sleeve3.jpg',
 'phase_4/maps/male_sleeve1.jpg',
 'phase_4/maps/male_sleeve2_palm.jpg',
 'phase_4/maps/male_sleeve3c.jpg',
 'phase_4/maps/shirt_Sleeve_ghost.jpg',
 'phase_4/maps/shirt_Sleeve_pumkin.jpg',
 'phase_4/maps/holidaySleeve1.jpg',
 'phase_4/maps/holidaySleeve3.jpg',
 'phase_4/maps/female_sleeve1b.jpg',
 'phase_4/maps/female_sleeve5New.jpg',
 'phase_4/maps/male_sleeve4New.jpg',
 'phase_4/maps/sleeve6New.jpg',
 'phase_4/maps/SleeveMaleNew7.jpg',
 'phase_4/maps/female_sleeveNew6.jpg',
 'phase_4/maps/Vday5Sleeve.jpg',
 'phase_4/maps/Vda6Sleeve.jpg',
 'phase_4/maps/Vday_shirt4sleeve.jpg',
 'phase_4/maps/Vday2cSleeve.jpg',
 'phase_4/maps/sleeveTieDye.jpg',
 'phase_4/maps/male_sleeve1.jpg',
 'phase_4/maps/StPats_sleeve.jpg',
 'phase_4/maps/StPats_sleeve2.jpg',
 'phase_4/maps/ContestfishingVestSleeve1.jpg',
 'phase_4/maps/ContestFishtankSleeve1.jpg',
 'phase_4/maps/ContestPawSleeve1.jpg',
 'phase_4/maps/CowboySleeve1.jpg',
 'phase_4/maps/CowboySleeve2.jpg',
 'phase_4/maps/CowboySleeve3.jpg',
 'phase_4/maps/CowboySleeve4.jpg',
 'phase_4/maps/CowboySleeve5.jpg',
 'phase_4/maps/CowboySleeve6.jpg',
 'phase_4/maps/4thJulySleeve1.jpg',
 'phase_4/maps/4thJulySleeve2.jpg',
 'phase_4/maps/shirt_sleeveCat7_01.jpg',
 'phase_4/maps/shirt_sleeveCat7_02.jpg',
 'phase_4/maps/contest_backpack_sleeve.jpg',
 'phase_4/maps/Contest_leder_sleeve.jpg',
 'phase_4/maps/contest_mellon_sleeve2.jpg',
 'phase_4/maps/contest_race_sleeve.jpg',
 'phase_4/maps/PJSleeveBlue.jpg',
 'phase_4/maps/PJSleeveRed.jpg',
 'phase_4/maps/PJSleevePurple.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_desat4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_party1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_party2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_summer1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_summer2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_marathon1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley2.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween3.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine3.jpg',
 'phase_4/maps/tt_t_chr_shirtSleeve_scientist.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_mailbox.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcan.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_loonyLabs.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_hydrant.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_whistle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_cogbuster.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated01.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty01.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotVPIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_jellyBeans.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_doodle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween5.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloweenTurtle.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_greentoon1.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_getConnectedMoverShaker.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racingGrandPrix.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotVPIcon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotCrusher.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_bee.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_pirate.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_supertoon.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_vampire.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_dinosaur.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding3.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween06.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween07.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter02.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing06.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing07.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated03.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley04.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding4.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding05.jpg',
 'phase_4/maps/tt_t_chr_avt_shirtSleeve_anniversary.jpg',
 'phase_4/maps/BetaOverallSleeve.jpg']
SHORTS = 0
SKIRT = 1
Shorts = [('phase_3/maps/desat_shorts_1.jpg', SHORTS), # 0
 ('phase_3/maps/desat_shorts_2.jpg', SHORTS), # 1
 ('phase_3/maps/desat_shorts_4.jpg', SHORTS), # 2
 ('phase_3/maps/desat_shorts_5.jpg', SHORTS), # 3
 ('phase_3/maps/desat_shorts_6.jpg', SHORTS), # 4
 ('phase_3/maps/desat_shorts_7.jpg', SHORTS), # 5
 ('phase_3/maps/desat_shorts_8.jpg', SHORTS), # 6
 ('phase_3/maps/desat_shorts_9.jpg', SHORTS), # 7
 ('phase_3/maps/desat_shorts_10.jpg', SHORTS), # 8
 ('phase_3/maps/desat_skirt_1.jpg', SKIRT), # 9
 ('phase_3/maps/desat_skirt_2.jpg', SKIRT), # 10
 ('phase_3/maps/desat_skirt_3.jpg', SKIRT), # 11
 ('phase_3/maps/desat_skirt_4.jpg', SKIRT), # 12
 ('phase_3/maps/desat_skirt_5.jpg', SKIRT), # 13
 ('phase_3/maps/desat_skirt_6.jpg', SKIRT), # 14
 ('phase_3/maps/desat_skirt_7.jpg', SKIRT), # 15
 ('phase_4/maps/female_skirt1.jpg', SKIRT), # 16
 ('phase_4/maps/female_skirt2.jpg', SKIRT), # 17
 ('phase_4/maps/female_skirt3.jpg', SKIRT), # 18
 ('phase_4/maps/VdaySkirt1.jpg', SKIRT), # 19
 ('phase_4/maps/skirtNew5.jpg', SKIRT), # 20
 ('phase_4/maps/VdayShorts2.jpg', SHORTS), # 21
 ('phase_4/maps/shorts4.jpg', SHORTS), # 22
 ('phase_4/maps/shorts1.jpg', SHORTS), # 23
 ('phase_4/maps/shorts5.jpg', SHORTS), # 24
 ('phase_4/maps/CowboyShorts1.jpg', SHORTS), # 25
 ('phase_4/maps/CowboyShorts2.jpg', SHORTS), # 26
 ('phase_4/maps/CowboySkirt1.jpg', SKIRT), # 27
 ('phase_4/maps/CowboySkirt2.jpg', SKIRT), # 28
 ('phase_4/maps/4thJulyShorts1.jpg', SHORTS), # 29
 ('phase_4/maps/4thJulySkirt1.jpg', SKIRT), # 30
 ('phase_4/maps/shortsCat7_01.jpg', SHORTS), # 31
 ('phase_4/maps/skirtCat7_01.jpg', SKIRT), # 32
 ('phase_4/maps/Blue_shorts_1.jpg', SHORTS), # 33
 ('phase_4/maps/Red_shorts_1.jpg', SHORTS), # 34
 ('phase_4/maps/Purple_shorts_1.jpg', SHORTS), # 35
 ('phase_4/maps/tt_t_chr_avt_shorts_winter1.jpg', SHORTS), # 36
 ('phase_4/maps/tt_t_chr_avt_shorts_winter2.jpg', SHORTS), # 37
 ('phase_4/maps/tt_t_chr_avt_shorts_winter3.jpg', SHORTS), # 38
 ('phase_4/maps/tt_t_chr_avt_shorts_winter4.jpg', SHORTS), # 39
 ('phase_4/maps/tt_t_chr_avt_skirt_winter1.jpg', SKIRT), # 40
 ('phase_4/maps/tt_t_chr_avt_skirt_winter2.jpg', SKIRT), # 41
 ('phase_4/maps/tt_t_chr_avt_skirt_winter3.jpg', SKIRT), # 42
 ('phase_4/maps/tt_t_chr_avt_skirt_winter4.jpg', SKIRT), # 43
 ('phase_4/maps/tt_t_chr_avt_shorts_valentine1.jpg', SHORTS), # 44
 ('phase_4/maps/tt_t_chr_avt_shorts_valentine2.jpg', SHORTS), # 45
 ('phase_4/maps/tt_t_chr_avt_shorts_fishing1.jpg', SHORTS), # 46
 ('phase_4/maps/tt_t_chr_avt_shorts_gardening1.jpg', SHORTS), # 47
 ('phase_4/maps/tt_t_chr_avt_shorts_party1.jpg', SHORTS), # 48
 ('phase_4/maps/tt_t_chr_avt_shorts_racing1.jpg', SHORTS), # 49
 ('phase_4/maps/tt_t_chr_avt_shorts_summer1.jpg', SHORTS), # 50
 ('phase_4/maps/tt_t_chr_avt_shorts_golf1.jpg', SHORTS), # 51
 ('phase_4/maps/tt_t_chr_avt_shorts_halloween1.jpg', SHORTS), # 52
 ('phase_4/maps/tt_t_chr_avt_shorts_halloween2.jpg', SHORTS), # 53
 ('phase_4/maps/tt_t_chr_avt_shorts_saveBuilding1.jpg', SHORTS), # 54
 ('phase_4/maps/tt_t_chr_avt_shorts_trolley1.jpg', SHORTS), # 55
 ('phase_4/maps/tt_t_chr_avt_shorts_halloween4.jpg', SHORTS), # 56
 ('phase_4/maps/tt_t_chr_avt_shorts_halloween3.jpg', SHORTS), # 57
 ('phase_4/maps/tt_t_chr_shorts_scientistA.jpg', SHORTS), # 58
 ('phase_4/maps/tt_t_chr_shorts_scientistB.jpg', SHORTS), # 59
 ('phase_4/maps/tt_t_chr_shorts_scientistC.jpg', SHORTS), # 60
 ('phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg', SHORTS), # 61
 ('phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.jpg', SHORTS), # 62
 ('phase_4/maps/tt_t_chr_avt_shorts_halloween5.jpg', SHORTS), # 63
 ('phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.jpg', SHORTS), # 64
 ('phase_4/maps/tt_t_chr_avt_shorts_greentoon1.jpg', SHORTS), # 65
 ('phase_4/maps/tt_t_chr_avt_shorts_racingGrandPrix.jpg', SHORTS), # 66
 ('phase_4/maps/tt_t_chr_avt_skirt_valentine1.jpg', SKIRT), # 67
 ('phase_4/maps/tt_t_chr_avt_skirt_valentine2.jpg', SKIRT), # 68
 ('phase_4/maps/tt_t_chr_avt_skirt_fishing1.jpg', SKIRT), # 69
 ('phase_4/maps/tt_t_chr_avt_skirt_gardening1.jpg', SKIRT), # 70
 ('phase_4/maps/tt_t_chr_avt_skirt_party1.jpg', SKIRT), # 71
 ('phase_4/maps/tt_t_chr_avt_skirt_racing1.jpg', SKIRT), # 72
 ('phase_4/maps/tt_t_chr_avt_skirt_summer1.jpg', SKIRT), # 73
 ('phase_4/maps/tt_t_chr_avt_skirt_golf1.jpg', SKIRT), # 74
 ('phase_4/maps/tt_t_chr_avt_skirt_halloween1.jpg', SKIRT), # 75
 ('phase_4/maps/tt_t_chr_avt_skirt_halloween2.jpg', SKIRT), # 76
 ('phase_4/maps/tt_t_chr_avt_skirt_saveBuilding1.jpg', SKIRT), # 77
 ('phase_4/maps/tt_t_chr_avt_skirt_trolley1.jpg', SKIRT), # 78
 ('phase_4/maps/tt_t_chr_avt_skirt_halloween3.jpg', SKIRT), # 79
 ('phase_4/maps/tt_t_chr_avt_skirt_halloween4.jpg', SKIRT), # 80
 ('phase_4/maps/tt_t_chr_avt_skirt_greentoon1.jpg', SKIRT), # 81
 ('phase_4/maps/tt_t_chr_avt_skirt_racingGrandPrix.jpg', SKIRT), # 82
 ('phase_4/maps/tt_t_chr_avt_shorts_lawbotCrusher.jpg', SHORTS), # 83
 ('phase_4/maps/tt_t_chr_avt_shorts_bee.jpg', SHORTS), # 84
 ('phase_4/maps/tt_t_chr_avt_shorts_pirate.jpg', SHORTS), # 85
 ('phase_4/maps/tt_t_chr_avt_shorts_supertoon.jpg', SHORTS), # 86
 ('phase_4/maps/tt_t_chr_avt_shorts_vampire.jpg', SHORTS), # 87
 ('phase_4/maps/tt_t_chr_avt_shorts_dinosaur.jpg', SHORTS), # 88
 ('phase_4/maps/tt_t_chr_avt_shorts_golf03.jpg', SHORTS), # 89
 ('phase_4/maps/tt_t_chr_avt_shorts_racing03.jpg', SHORTS), # 90
 ('phase_4/maps/tt_t_chr_avt_shorts_golf04.jpg', SHORTS), # 91
 ('phase_4/maps/tt_t_chr_avt_shorts_golf05.jpg', SHORTS), # 92
 ('phase_4/maps/tt_t_chr_avt_shorts_racing04.jpg', SHORTS), # 93
 ('phase_4/maps/tt_t_chr_avt_shorts_racing05.jpg', SHORTS), # 94
 ('phase_4/maps/tt_t_chr_avt_skirt_pirate.jpg', SKIRT), # 95
 ('phase_4/maps/tt_t_chr_avt_skirt_golf02.jpg', SKIRT), # 96
 ('phase_4/maps/tt_t_chr_avt_skirt_racing03.jpg', SKIRT), # 97
 ('phase_4/maps/tt_t_chr_avt_skirt_golf03.jpg', SKIRT), # 98
 ('phase_4/maps/tt_t_chr_avt_skirt_golf04.jpg', SKIRT), # 99
 ('phase_4/maps/tt_t_chr_avt_skirt_racing04.jpg', SKIRT), # 100
 ('phase_4/maps/tt_t_chr_avt_skirt_racing05.jpg', SKIRT), # 101
 ('phase_4/maps/BetaOverallShorts.jpg', SHORTS)] # 102
ClothesColors = [VBase4(0.933594, 0.265625, 0.28125, 1.0),
 VBase4(0.863281, 0.40625, 0.417969, 1.0),
 VBase4(0.710938, 0.234375, 0.4375, 1.0),
 VBase4(0.992188, 0.480469, 0.167969, 1.0),
 VBase4(0.996094, 0.898438, 0.320312, 1.0),
 VBase4(0.550781, 0.824219, 0.324219, 1.0),
 VBase4(0.242188, 0.742188, 0.515625, 1.0),
 VBase4(0.433594, 0.90625, 0.835938, 1.0),
 VBase4(0.347656, 0.820312, 0.953125, 1.0),
 VBase4(0.191406, 0.5625, 0.773438, 1.0),
 VBase4(0.285156, 0.328125, 0.726562, 1.0),
 VBase4(0.460938, 0.378906, 0.824219, 1.0),
 VBase4(0.546875, 0.28125, 0.75, 1.0),
 VBase4(0.570312, 0.449219, 0.164062, 1.0),
 VBase4(0.640625, 0.355469, 0.269531, 1.0),
 VBase4(0.996094, 0.695312, 0.511719, 1.0),
 VBase4(0.832031, 0.5, 0.296875, 1.0),
 VBase4(0.992188, 0.480469, 0.167969, 1.0),
 VBase4(0.550781, 0.824219, 0.324219, 1.0),
 VBase4(0.433594, 0.90625, 0.835938, 1.0),
 VBase4(0.347656, 0.820312, 0.953125, 1.0),
 VBase4(0.96875, 0.691406, 0.699219, 1.0),
 VBase4(0.996094, 0.957031, 0.597656, 1.0),
 VBase4(0.855469, 0.933594, 0.492188, 1.0),
 VBase4(0.558594, 0.589844, 0.875, 1.0),
 VBase4(0.726562, 0.472656, 0.859375, 1.0),
 VBase4(0.898438, 0.617188, 0.90625, 1.0),
 VBase4(1.0, 1.0, 1.0, 1.0),
 VBase4(0.0, 0.2, 0.956862, 1.0),
 VBase4(0.972549, 0.094117, 0.094117, 1.0),
 VBase4(0.447058, 0.0, 0.90196, 1.0),
 VBase4(0.3, 0.3, 0.35, 1)]
ShirtStyles = {'bss1': [0, 0, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12),
           (27, 27),
           (31, 31)]],
 'bss2': [1, 1, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12),
           (31, 31)]],
 'bss3': [2, 2, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12)]],
 'bss4': [3, 3, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12)]],
 'bss5': [4, 4, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12)]],
 'bss6': [5, 5, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12)]],
 'bss7': [8, 8, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (8, 8),
           (9, 9),
           (11, 11),
           (12, 12),
           (27, 27)]],
 'bss8': [9, 9, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12)]],
 'bss9': [10, 0, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (10, 10),
           (11, 11),
           (12, 12),
           (27, 27),
           (31, 31)]],
 'bss10': [11, 0, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (27, 27)]],
 'bss11': [14, 10, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (27, 27),
            (31, 31)]],
 'bss12': [16, 0, [(27, 27),
            (27, 4),
            (27, 5),
            (27, 6),
            (27, 7),
            (27, 8),
            (27, 9)]],
 'bss13': [17, 0, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (27, 27),
            (31, 31)]],
 'bss14': [18, 12, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (8, 8),
            (9, 9),
            (11, 11),
            (12, 12),
            (27, 27)]],
 'bss15': [19, 13, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (27, 27),
            (31, 31)]],
 'gss6': [6, 6, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (11, 11),
           (12, 12),
           (21, 21),
           (22, 22),
           (23, 23),
           (24, 24),
           (25, 25),
           (26, 26)]],
 'gss7': [7, 7, [(0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5),
           (6, 6),
           (7, 7),
           (8, 8),
           (9, 9),
           (11, 11),
           (12, 12),
           (21, 21),
           (22, 22),
           (23, 23),
           (24, 24),
           (25, 25),
           (26, 26),
           (27, 27),
           (31, 31)]],
 'gss9': [12, 0, [(27, 27)]],
 'gss10': [13, 11, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (21, 21),
            (22, 22),
            (23, 23),
            (24, 24),
            (25, 25),
            (26, 26)]],
 'gss11': [15, 11, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (21, 21),
            (22, 22),
            (23, 23),
            (24, 24),
            (25, 25),
            (26, 26),
            (27, 27),
            (31, 31)]],
 'gss13': [20, 0, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (21, 21),
            (22, 22),
            (23, 23),
            (24, 24),
            (25, 25),
            (26, 26),
            (27, 27),
            (31, 31)]],
 'gss14': [21, 0, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (21, 21),
            (22, 22),
            (23, 23),
            (24, 24),
            (25, 25),
            (26, 26)]],
 'gss15': [22, 0, [(0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
            (21, 21),
            (22, 22),
            (23, 23),
            (24, 24),
            (25, 25),
            (26, 26),
            (27, 27),
            (31, 31)]],
 'c_ss1': [25, 16, [(27, 27)]],
 'c_ss2': [27, 18, [(27, 27)]],
 'c_ss3': [38, 27, [(27, 27)]],
 'c_bss1': [26, 17, [(27, 27)]],
 'c_bss2': [28, 19, [(27, 27)]],
 'c_bss3': [37, 26, [(27, 27)]],
 'c_bss4': [39, 28, [(27, 27)]],
 'c_gss1': [23, 14, [(27, 27)]],
 'c_gss2': [24, 15, [(27, 27)]],
 'c_gss3': [35, 24, [(27, 27)]],
 'c_gss4': [36, 25, [(27, 27)]],
 'c_gss5': [40, 29, [(27, 27)]],
 'c_ss4': [45, 34, [(27, 27)]],
 'c_ss5': [46, 35, [(27, 27)]],
 'c_ss6': [52, 41, [(27, 27)]],
 'c_ss7': [53, 42, [(27, 27)]],
 'c_ss8': [54, 43, [(27, 27)]],
 'c_ss9': [55, 44, [(27, 27)]],
 'c_ss10': [56, 45, [(27, 27)]],
 'c_ss11': [57, 46, [(27, 27)]],
 'hw_ss1': [29, 20, [(27, 27)]],
 'hw_ss2': [30, 21, [(27, 27)]],
 'hw_ss3': [114, 101, [(27, 27)]],
 'hw_ss4': [115, 102, [(27, 27)]],
 'hw_ss5': [122, 109, [(27, 27)]],
 'hw_ss6': [123, 110, [(27, 27)]],
 'hw_ss7': [124, 111, [(27, 27)]],
 'hw_ss8': [125, 112, [(27, 27)]],
 'hw_ss9': [126, 113, [(27, 27)]],
 'wh_ss1': [31, 22, [(27, 27)]],
 'wh_ss2': [32, 22, [(27, 27)]],
 'wh_ss3': [33, 23, [(27, 27)]],
 'wh_ss4': [34, 23, [(27, 27)]],
 'vd_ss1': [41, 30, [(27, 27)]],
 'vd_ss2': [42, 31, [(27, 27)]],
 'vd_ss3': [43, 32, [(27, 27)]],
 'vd_ss4': [44, 33, [(27, 27)]],
 'vd_ss5': [69, 58, [(27, 27)]],
 'vd_ss6': [70, 59, [(27, 27)]],
 'vd_ss7': [96, 85, [(27, 27)]],
 'sd_ss1': [47, 36, [(27, 27)]],
 'sd_ss2': [48, 37, [(27, 27)]],
 'sd_ss3': [116, 103, [(27, 27)]],
 'tc_ss1': [49, 38, [(27, 27)]],
 'tc_ss2': [50, 39, [(27, 27)]],
 'tc_ss3': [51, 40, [(27, 27)]],
 'tc_ss4': [62, 51, [(27, 27)]],
 'tc_ss5': [63, 52, [(27, 27)]],
 'tc_ss6': [64, 53, [(27, 27)]],
 'tc_ss7': [65, 54, [(27, 27)]],
 'j4_ss1': [58, 47, [(27, 27)]],
 'j4_ss2': [59, 48, [(27, 27)]],
 'c_ss12': [60, 49, [(27, 27)]],
 'c_ss13': [61, 50, [(27, 27)]],
 'pj_ss1': [66, 55, [(27, 27)]],
 'pj_ss2': [67, 56, [(27, 27)]],
 'pj_ss3': [68, 57, [(27, 27)]],
 'sa_ss1': [71, 60, [(27, 27)]],
 'sa_ss2': [72, 61, [(27, 27)]],
 'sa_ss3': [73, 62, [(27, 27)]],
 'sa_ss4': [74, 63, [(27, 27)]],
 'sa_ss5': [75, 64, [(27, 27)]],
 'sa_ss6': [76, 65, [(27, 27)]],
 'sa_ss7': [77, 66, [(27, 27)]],
 'sa_ss8': [78, 67, [(27, 27)]],
 'sa_ss9': [79, 68, [(27, 27)]],
 'sa_ss10': [80, 69, [(27, 27)]],
 'sa_ss11': [81, 70, [(27, 27)]],
 'sa_ss12': [82, 71, [(27, 27)]],
 'sa_ss13': [83, 72, [(27, 27)]],
 'sa_ss14': [84, 73, [(27, 27)]],
 'sa_ss15': [85, 74, [(27, 27)]],
 'sa_ss16': [86, 75, [(27, 27)]],
 'sa_ss17': [87, 76, [(27, 27)]],
 'sa_ss18': [88, 77, [(27, 27)]],
 'sa_ss19': [89, 78, [(27, 27)]],
 'sa_ss20': [90, 79, [(27, 27)]],
 'sa_ss21': [91, 80, [(27, 27)]],
 'sa_ss22': [92, 81, [(27, 27)]],
 'sa_ss23': [93, 82, [(27, 27)]],
 'sa_ss24': [94, 83, [(27, 27)]],
 'sa_ss25': [95, 84, [(27, 27)]],
 'sa_ss26': [106, 93, [(27, 27)]],
 'sa_ss27': [110, 97, [(27, 27)]],
 'sa_ss28': [111, 98, [(27, 27)]],
 'sa_ss29': [120, 107, [(27, 27)]],
 'sa_ss30': [121, 108, [(27, 27)]],
 'sa_ss31': [118, 105, [(27, 27)]],
 'sa_ss32': [127, 114, [(27, 27)]],
 'sa_ss33': [128, 115, [(27, 27)]],
 'sa_ss34': [129, 116, [(27, 27)]],
 'sa_ss35': [130, 117, [(27, 27)]],
 'sa_ss36': [131, 118, [(27, 27)]],
 'sa_ss37': [132, 119, [(27, 27)]],
 'sa_ss38': [133, 120, [(27, 27)]],
 'sa_ss39': [134, 121, [(27, 27)]],
 'sa_ss40': [135, 122, [(27, 27)]],
 'sa_ss41': [136, 123, [(27, 27)]],
 'sa_ss42': [137, 124, [(27, 27)]],
 'sa_ss43': [138, 125, [(27, 27)]],
 'sa_ss44': [139, 126, [(27, 27)]],
 'sa_ss45': [140, 127, [(27, 27)]],
 'sa_ss46': [141, 128, [(27, 27)]],
 'sa_ss47': [142, 129, [(27, 27)]],
 'sa_ss48': [143, 130, [(27, 27)]],
 'sa_ss49': [144, 116, [(27, 27)]],
 'sa_ss50': [145, 131, [(27, 27)]],
 'sa_ss51': [146, 133, [(27, 27)]],
 'sa_ss52': [147, 134, [(27, 27)]],
 'sa_ss53': [148, 135, [(27, 27)]],
 'sa_ss54': [149, 136, [(27, 27)]],
 'sa_ss55': [150, 137, [(27, 27)]],
 'sc_1': [97, 86, [(27, 27)]],
 'sc_2': [98, 86, [(27, 27)]],
 'sc_3': [99, 86, [(27, 27)]],
 'sil_1': [100, 87, [(27, 27)]],
 'sil_2': [101, 88, [(27, 27)]],
 'sil_3': [102, 89, [(27, 27)]],
 'sil_4': [103, 90, [(27, 27)]],
 'sil_5': [104, 91, [(27, 27)]],
 'sil_6': [105, 92, [(27, 27)]],
 'sil_7': [107, 94, [(27, 27)]],
 'sil_8': [108, 95, [(27, 27)]],
 'emb_us1': [103, 90, [(27, 27)]],
 'emb_us2': [100, 87, [(27, 27)]],
 'emb_us3': [101, 88, [(27, 27)]],
 'sb_1': [109, 96, [(27, 27)]],
 'jb_1': [112, 99, [(27, 27)]],
 'jb_2': [113, 100, [(27, 27)]],
 'ugcms': [117, 104, [(27, 27)]],
 'lb_1': [119, 106, [(27, 27)]],
 'beta': [151, 138, [(27, 27)]]}
BottomStyles = {'bbs1': [0, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           19,
           20,
           27,
           31]],
 'bbs2': [1, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           19,
           20,
           27,
           31]],
 'bbs3': [2, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           19,
           20]],
 'bbs4': [4, [0,
           1,
           2,
           4,
           6,
           8,
           9,
           11,
           12,
           13,
           15,
           16,
           17,
           18,
           19,
           20,
           27]],
 'bbs5': [5, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           19,
           20]],
 'bbs6': [6, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           14,
           15,
           16,
           17,
           18,
           19,
           20,
           27]],
 'bbs7': [7, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           20,
           27,
           31]],
 'bbs8': [8, [0,
           1,
           2,
           4,
           6,
           9,
           10,
           11,
           12,
           13,
           14,
           15,
           16,
           17,
           18,
           19,
           20,
           27]],
 'vd_bs1': [21, [27]],
 'vd_bs2': [44, [27]],
 'vd_bs3': [45, [27]],
 'c_bs1': [22, [27]],
 'c_bs2': [23, [27]],
 'c_bs5': [31, [27]],
 'sd_bs1': [24, [27]],
 'sd_bs2': [65, [27]],
 'pj_bs1': [33, [27]],
 'pj_bs2': [34, [27]],
 'pj_bs3': [35, [27]],
 'wh_bs1': [36, [27]],
 'wh_bs2': [37, [27]],
 'wh_bs3': [38, [27]],
 'wh_bs4': [39, [27]],
 'hw_bs1': [84, [27]],
 'hw_bs2': [85, [27]],
 'hw_bs5': [86, [27]],
 'hw_bs6': [87, [27]],
 'hw_bs7': [88, [27]],
 'gsk1': [9, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26,
           27,
           31]],
 'gsk2': [10, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26]],
 'gsk3': [11, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26]],
 'gsk4': [12, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26]],
 'gsk5': [13, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26]],
 'gsk6': [14, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26,
           27,
           31]],
 'gsk7': [15, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26,
           27]],
 'gsh2': [3, [0,
           1,
           2,
           3,
           4,
           5,
           6,
           7,
           8,
           9,
           11,
           12,
           21,
           22,
           23,
           24,
           25,
           26,
           27]],
 'c_gsk1': [16, [27]],
 'c_gsk2': [17, [27]],
 'c_gsk3': [18, [27]],
 'vd_gs1': [19, [27]],
 'vd_gs2': [67, [27]],
 'vd_gs3': [68, [27]],
 'c_gsk4': [20, [27]],
 'sd_gs1': [24, [27]],
 'sd_gs2': [81, [27]],
 'c_gsk5': [27, [27]],
 'c_gsk6': [28, [27]],
 'c_bs3': [25, [27]],
 'c_bs4': [26, [27]],
 'j4_bs1': [29, [27]],
 'j4_gs1': [30, [27]],
 'c_gsk7': [32, [27]],
 'pj_gs1': [33, [27]],
 'pj_gs2': [34, [27]],
 'pj_gs3': [35, [27]],
 'wh_gsk1': [40, [27]],
 'wh_gsk2': [41, [27]],
 'wh_gsk3': [42, [27]],
 'wh_gsk4': [43, [27]],
 'sa_bs1': [46, [27]],
 'sa_bs2': [47, [27]],
 'sa_bs3': [48, [27]],
 'sa_bs4': [49, [27]],
 'sa_bs5': [50, [27]],
 'sa_bs6': [51, [27]],
 'sa_bs7': [52, [27]],
 'sa_bs8': [53, [27]],
 'sa_bs9': [54, [27]],
 'sa_bs10': [55, [27]],
 'sa_bs11': [56, [27]],
 'sa_bs12': [57, [27]],
 'sa_bs13': [62, [27]],
 'sa_bs14': [83, [27]],
 'sa_bs15': [66, [27]],
 'sa_bs16': [89, [27]],
 'sa_bs17': [90, [27]],
 'sa_bs18': [91, [27]],
 'sa_bs19': [92, [27]],
 'sa_bs20': [93, [27]],
 'sa_bs21': [94, [27]],
 'sa_gs1': [69, [27]],
 'sa_gs2': [70, [27]],
 'sa_gs3': [71, [27]],
 'sa_gs4': [72, [27]],
 'sa_gs5': [73, [27]],
 'sa_gs6': [74, [27]],
 'sa_gs7': [75, [27]],
 'sa_gs8': [76, [27]],
 'sa_gs9': [77, [27]],
 'sa_gs10': [78, [27]],
 'sa_gs11': [79, [27]],
 'sa_gs12': [80, [27]],
 'sa_gs13': [62, [27]],
 'sa_gs14': [83, [27]],
 'sa_gs15': [82, [27]],
 'sa_gs16': [96, [27]],
 'sa_gs17': [97, [27]],
 'sa_gs18': [98, [27]],
 'sa_gs19': [99, [27]],
 'sa_gs20': [100, [27]],
 'sa_gs21': [101, [27]],
 'sc_bs1': [58, [27]],
 'sc_bs2': [59, [27]],
 'sc_bs3': [60, [27]],
 'sc_gs1': [77, [27]],
 'sc_gs2': [78, [27]],
 'sc_gs3': [79, [27]],
 'sil_bs1': [61, [27]],
 'hw_bs3': [63, [27]],
 'hw_bs4': [64, [27]],
 'hw_gs1': [84, [27]],
 'hw_gs2': [85, [27]],
 'hw_gs5': [86, [27]],
 'hw_gs6': [87, [27]],
 'hw_gs7': [88, [27]],
 'hw_gsk1': [95, [27]],
 'beta_short': [102, [27]]}
MAKE_A_TOON = 1
TAMMY_TAILOR = 2004
LONGJOHN_LEROY = 1007
TAILOR_HARMONY = 4008
BONNIE_BLOSSOM = 5007
WARREN_BUNDLES = 3008
WORNOUT_WAYLON = 9010
TailorCollections = {MAKE_A_TOON: [['bss1', 'bss2'],
               ['bbs1', 'bbs2', 'gsk1']],
 TAMMY_TAILOR: [['bss1', 'bss2', 'sc_1', 'sc_2', 'sc_3'],
               ['bbs1', 'bbs2', 'sc_bs1', 'sc_bs2', 'sc_bs3', 'gsk1', 'sc_gs1', 'sc_gs2', 'sc_gs3']],
 LONGJOHN_LEROY: [['bss3', 'bss4', 'bss14', 'gss14'],
                  ['bbs3', 'bbs4', 'gsk2', 'gsh2']],
 TAILOR_HARMONY: [['bss5', 'bss6', 'bss10', 'gss6', 'gss9'],
                  ['bbs5', 'gsk3']],
 BONNIE_BLOSSOM: [['bss7', 'bss8', 'bss12', 'gss10'],
                  ['bbs6', 'gsk4', 'gsk5']],
 WARREN_BUNDLES: [['bss9', 'bss13', 'gss7', 'gss11'],
                  ['bbs7', 'gsk6']],
 WORNOUT_WAYLON: [['bss11', 'bss15', 'gss13', 'gss15', 'beta'],
                  ['bbs8', 'gsk7', 'beta_short']]}
TOON_SHIRTS = 0
TOON_SHORTS = 1
HAT = 1
GLASSES = 2
BACKPACK = 4
SHOES = 8
MakeAToonBottoms = []
MakeAToonShirts = []
for style in TailorCollections[MAKE_A_TOON][TOON_SHORTS]:
    index = BottomStyles[style][0]
    MakeAToonBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][TOON_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonShirts.append(index)

def getRandomTop(tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    style = generator.choice(collection[TOON_SHIRTS])
    styleList = ShirtStyles[style]
    colors = generator.choice(styleList[2])
    return (styleList[0],
     colors[0],
     styleList[1],
     colors[1])


def getRandomBottom(tailorId = MAKE_A_TOON, generator = None, girlBottomType = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if girlBottomType is None:
        style = generator.choice(collection[TOON_SHORTS])
    elif girlBottomType == SKIRT:
        skirtCollection = [style for style in collection[TOON_SHORTS] if Shorts[BottomStyles[style][0]][1] == SKIRT]
        style = generator.choice(skirtCollection)
    elif girlBottomType == SHORTS:
        shortsCollection = [style for style in collection[TOON_SHORTS] if Shorts[BottomStyles[style][0]][1] == SHORTS]
        style = generator.choice(shortsCollection)
    else:
        notify.error('Bad girlBottomType: %s' % girlBottomType)
    styleList = BottomStyles[style]
    color = generator.choice(styleList[1])
    return (styleList[0], color)


def getRandomizedTops(gender, tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    collection = collection[TOON_SHIRTS][:]
    tops = []
    random.shuffle(collection)
    for style in collection:
        colors = ShirtStyles[style][2][:]
        random.shuffle(colors)
        for color in colors:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[style][1],
             color[1]))

    return tops


def getRandomizedBottoms(gender, tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    collection = collection[TOON_SHORTS][:]
    bottoms = []
    random.shuffle(collection)
    for style in collection:
        colors = BottomStyles[style][1][:]
        random.shuffle(colors)
        for color in colors:
            bottoms.append((BottomStyles[style][0], color))

    return bottoms


def getTops(gender, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHIRTS]
    tops = []
    for style in collection:
        for color in ShirtStyles[style][2]:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[style][1],
             color[1]))

    return tops

def getTopColors(gender, top, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHIRTS]
    tops = getTopStyles(gender, tailorId)
    colors = []
    index = collection[tops.index(top)]
    for color in ShirtStyles[index][2]:
        colors.append((color[0], color[1]))
    return colors

def getTopStyles(gender, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHIRTS]
    tops = []
    for style in collection:
        tops.append((ShirtStyles[style][0], ShirtStyles[style][1]))
    return tops

def getAllTops():
    tops = []
    for style in list(ShirtStyles.keys()):
        for color in ShirtStyles[style][2]:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[style][1],
             color[1]))

    return tops


def getBottoms(gender, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHORTS]
    bottoms = []
    for style in collection:
        for color in BottomStyles[style][1]:
            bottoms.append((BottomStyles[style][0], color))

    return bottoms

def getBottomStyles(gender, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHORTS]
    bottoms = []
    for style in collection:
            bottoms.append(BottomStyles[style][0])

    return bottoms

def getBottomColors(gender, bottom, tailorId = MAKE_A_TOON):
    collection = TailorCollections[tailorId][TOON_SHORTS]
    bottoms = getBottomStyles(gender, tailorId)
    colors = []
    index = collection[bottoms.index(bottom)]
    for color in BottomStyles[index][1]:
        colors.append(color)
    return colors

allColorsList = [VBase4(1.0, 1.0, 1.0, 1.0),
 VBase4(0.96875, 0.691406, 0.699219, 1.0),
 VBase4(0.933594, 0.265625, 0.28125, 1.0),
 VBase4(0.863281, 0.40625, 0.417969, 1.0),
 VBase4(0.710938, 0.234375, 0.4375, 1.0),
 VBase4(0.570312, 0.449219, 0.164062, 1.0),
 VBase4(0.640625, 0.355469, 0.269531, 1.0),
 VBase4(0.996094, 0.695312, 0.511719, 1.0),
 VBase4(0.832031, 0.5, 0.296875, 1.0),
 VBase4(0.992188, 0.480469, 0.167969, 1.0),
 VBase4(0.996094, 0.898438, 0.320312, 1.0),
 VBase4(0.996094, 0.957031, 0.597656, 1.0),
 VBase4(0.855469, 0.933594, 0.492188, 1.0),
 VBase4(0.550781, 0.824219, 0.324219, 1.0),
 VBase4(0.242188, 0.742188, 0.515625, 1.0),
 VBase4(0.304688, 0.96875, 0.402344, 1.0),
 VBase4(0.433594, 0.90625, 0.835938, 1.0),
 VBase4(0.347656, 0.820312, 0.953125, 1.0),
 VBase4(0.191406, 0.5625, 0.773438, 1.0),
 VBase4(0.558594, 0.589844, 0.875, 1.0),
 VBase4(0.285156, 0.328125, 0.726562, 1.0),
 VBase4(0.460938, 0.378906, 0.824219, 1.0),
 VBase4(0.546875, 0.28125, 0.75, 1.0),
 VBase4(0.726562, 0.472656, 0.859375, 1.0),
 VBase4(0.898438, 0.617188, 0.90625, 1.0),
 VBase4(0.7, 0.7, 0.8, 1.0),
 VBase4(0.3, 0.3, 0.35, 1.0),
 VBase4(0.325, 0.407, 0.601, 1.0),
 VBase4(0.1725490196, 0.45882352941, 1.0, 1.0),
 VBase4(1, 0.75686274509, 0.8, 1.0),
 VBase4(1.0, 0.26274509803, 0.6431372549, 1.0),
 VBase4(0.89019607843, 0.85490196078, 0.78823529411, 1.0),
 VBase4(0.75294117647, 0.75294117647, 0.75294117647, 1.0),
 VBase4(0.50196078431, 0.50196078431, 0.50196078431, 1.0),
 VBase4(0.80392156862, 0.49803921568, 0.19607843137, 1.0),
 VBase4(0.38039215686, 0.25098039215, 0.31764705882, 1.0),
 VBase4(0.45098039215, 0.45098039215, 0.69411764705, 1.0)]
# TODO: use defaultColorList in the code and get rid of the gendered color lists
defaultColorList = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
 25,
 26,
 27,
 28,
 29,
 30,
 31,
 32,
 33,
 34,
 35,
 36]
allColorsListApproximations = [VBase4(round(x[0], 3), round(x[1], 3), round(x[2], 3), round(x[3], 3)) for x in allColorsList]
allowedColors = defaultColorList.copy() # TODO: do I even need to have this variable?
HatModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_baseball', # 1
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_safari', # 2
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_ribbon', # 3
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_heart', # 4 
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_topHat', # 5
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_anvil', # 6
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_flowerPot', # 7
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sandbag', # 8
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_weight', # 9
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fez', # 10
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_golfHat', # 11
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_partyHat', # 12
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pillBox', # 13
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_crown', # 14
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_cowboyHat', # 15
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pirateHat', # 16
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_propellerHat', # 17
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fishingHat', # 18
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sombreroHat', # 19
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_strawHat', # 20
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sunHat', # 21
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_antenna', # 22
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_beeHiveHairdo', # 23
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bowler', # 24
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_chefsHat', # 25
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_detective', # 26
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_feathers', # 27
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fedora', # 28
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_mickeysBandConductorHat', # 29
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_nativeAmericanFeather', # 30
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pompadorHairdo', # 31
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_princess', # 32
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_robinHoodHat', # 33
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_romanHelmet', # 34
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_spiderAntennaThingy', # 35
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_tiara', # 36
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_vikingHelmet', # 37
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_witch', # 38
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_wizard', # 39
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_conquistadorHelmet', # 40
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_firefighterHelmet', # 41
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_foilPyramid', # 42
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_minersHardhatWithLight', # 43
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_napoleonHat', # 44
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pilotsCap', # 45
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_policeHat', # 46
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_rainbowAfroWig', # 47
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sailorHat', # 48
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_carmenMirandaFruitHat', # 49
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bobbyHat', # 50
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_jugheadHat', # 51
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_winter', # 52
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bandana', # 53
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_dinosaur', # 54
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_band', # 55
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_birdNest'] #56
HatTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRed.jpg', # 1
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPurple.jpg', # 2
 'phase_4/maps/tt_t_chr_avt_acc_hat_heartYellow.jpg', # 3
 'phase_4/maps/tt_t_chr_avt_acc_hat_topHatBlue.jpg', # 4
 'phase_4/maps/tt_t_chr_avt_acc_hat_safariBrown.jpg', # 5
 'phase_4/maps/tt_t_chr_avt_acc_hat_safariGreen.jpg', # 6
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballBlue.jpg', # 7
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballOrange.jpg', # 8
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonYellow.jpg', # 9
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonChecker.jpg', # 10
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonLtRed.jpg', # 11
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRainbow.jpg', # 12
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballYellow.jpg', # 13
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballRed.jpg', # 14
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballTeal.jpg', # 15
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPinkDots.jpg', # 16
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballPurple.jpg', # 17
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonCheckerGreen.jpg', # 18
 'phase_4/maps/tt_t_chr_avt_acc_hat_partyToon.jpg', # 19
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonBlue.jpg', # 20
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonGreen.jpg', # 21
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonBlackWhite.jpg', # 22
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonSepia.jpg', # 23
 ]
GlassesModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_roundGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_miniblinds',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_narrowGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_starGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_3dGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_aviator',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_catEyeGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_dorkGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_jackieOShades',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_scubaMask',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_goggles',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_grouchoMarxEyebrow',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_heartGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_insectEyeGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask3',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_monocle',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_mouthGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_squareRims',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_eyepatch',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_alienGlasses']
GlassesTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask2.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask4.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask5.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_eyepatchGems.jpg']
BackpackModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpack',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_batWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_beeWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonFlyWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_scubaTank',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_sharkFin',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_angelWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpackWithToys',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_butterflyWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonWing',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_jetPack',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_spiderLegs',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackA',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_birdWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackCat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackDog',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_airplane',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_woodenSword',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_supertoonCape',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_vampireCape',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dinosaurTail',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_band',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_gags',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_flunky']
BackpackTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackOrange.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_angelWingsMultiColor.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_butterflyWingsStyle2.jpg']
ShoesModels = ['feet',
 'shoes',
 'boots_short',
 'boots_long']
ShoesTextures = ['phase_3/maps/tt_t_chr_avt_acc_sho_athleticGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticRed.jpg',
 'phase_3/maps/tt_t_chr_avt_acc_sho_docMartinBootsGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleGreen.jpg', # 4
 'phase_4/maps/tt_t_chr_avt_acc_sho_wingtips.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoes.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_deckShoes.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleBlack.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleWhite.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStylePink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_cowboyBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakers.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesBrown.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_superToonRedBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsAqua.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsBrown.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsBlueSquares.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreenHearts.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreyDots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsOrangeStars.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPinkStars.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_loafers.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_motorcycleBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_oxfords.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_santaBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsBeige.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_workBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakersPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsRedDots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesViolet.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsBlue.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticBlack.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_pirate.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_dinosaur.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleBlue.jpg', # 49
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStylePurple.jpg' # 50
 ]
HatStyles = {'none': [0, 0, 0],
 'hbb1': [1, 0, 0],
 'hsf1': [2, 0, 0],
 'hsf2': [2, 5, 0],
 'hsf3': [2, 6, 0],
 'hht1': [4, 0, 0],
 'hht2': [4, 3, 0],
 'htp1': [5, 0, 0],
 'htp2': [5, 4, 0],
 'hav1': [6, 0, 0],
 'hfp1': [7, 0, 0],
 'hsg1': [8, 0, 0],
 'hwt1': [9, 0, 0],
 'hfz1': [10, 0, 0],
 'hgf1': [11, 0, 0],
 'hpt1': [12, 0, 0],
 'hpt2': [12, 19, 0],
 'hpb1': [13, 0, 0],
 'hcr1': [14, 0, 0],
 'hbb2': [1, 7, 0],
 'hbb3': [1, 8, 0],
 'hcw1': [15, 0, 0],
 'hpr1': [16, 0, 0],
 'hpp1': [17, 0, 0],
 'hfs1': [18, 0, 0],
 'hsb1': [19, 0, 0],
 'hst1': [20, 0, 0],
 'hat1': [22, 0, 0],
 'hhd1': [23, 0, 0],
 'hbw1': [24, 0, 0],
 'hch1': [25, 0, 0],
 'hdt1': [26, 0, 0],
 'hft1': [27, 0, 0],
 'hfd1': [28, 0, 0],
 'hmk1': [29, 0, 0],
 'hft2': [30, 0, 0],
 'hhd2': [31, 0, 0],
 'hrh1': [33, 0, 0],
 'hhm1': [34, 0, 0],
 'hat2': [35, 0, 0],
 'htr1': [36, 0, 0],
 'hhm2': [37, 0, 0],
 'hwz1': [38, 0, 0],
 'hwz2': [39, 0, 0],
 'hhm3': [40, 0, 0],
 'hhm4': [41, 0, 0],
 'hfp2': [42, 0, 0],
 'hhm5': [43, 0, 0],
 'hnp1': [44, 0, 0],
 'hpc2': [45, 0, 0],
 'hph1': [46, 0, 0],
 'hwg1': [47, 0, 0],
 'hbb4': [1, 13, 0],
 'hbb5': [1, 14, 0],
 'hbb6': [1, 15, 0],
 'hsl1': [48, 0, 0],
 'hfr1': [49, 0, 0],
 'hby1': [50, 0, 0],
 'hjh1': [51, 0, 0],
 'hbb7': [1, 17, 0],
 'hwt2': [52, 0, 0],
 'hhw2': [54, 0, 0],
 'hob1': [55, 0, 0],
 'hbn1': [56, 0, 0],
 'hrb1': [3, 0, 0],
 'hrb2': [3, 1, 0],
 'hrb3': [3, 2, 0],
 'hsu1': [21, 0, 0],
 'hrb4': [3, 9, 0],
 'hrb5': [3, 10, 0],
 'hrb6': [3, 11, 0],
 'hrb7': [3, 12, 0],
 'hpc1': [32, 0, 0],
 'hrb8': [3, 16, 0],
 'hrb9': [3, 18, 0],
 'hrb10': [3, 20, 0],
 'hrb11': [3, 21, 0],
 'hrb12': [3, 22, 0],
 'hrb13': [3, 23, 0],
 'hhw1': [53, 0, 0]}
GlassesStyles = {'none': [0, 0, 0],
 'grd1': [1, 0, 0],
 'gmb1': [2, 0, 0],
 'gnr1': [3, 0, 0],
 'gst1': [4, 0, 0],
 'g3d1': [5, 0, 0],
 'gav1': [6, 0, 0],
 'gjo1': [9, 0, 0],
 'gsb1': [10, 0, 0],
 'ggl1': [11, 0, 0],
 'ggm1': [12, 0, 0],
 'ghg1': [13, 0, 0],
 'gie1': [14, 0, 0],
 'gmt1': [15, 0, 0],
 'gmt2': [15, 1, 0],
 'gmt3': [16, 0, 0],
 'gmt4': [16, 2, 0],
 'gmt5': [16, 3, 0],
 'gmn1': [17, 0, 0],
 'gmo1': [18, 0, 0],
 'gsr1': [19, 0, 0],
 'gce1': [7, 0, 0],
 'gdk1': [8, 0, 0],
 'gag1': [21, 0, 0],
 'ghw1': [20, 0, 0],
 'ghw2': [20, 4, 0]}
BackpackStyles = {'none': [0, 0, 0],
 'bpb1': [1, 0, 0],
 'bpb2': [1, 1, 0],
 'bpb3': [1, 2, 0],
 'bpd1': [1, 3, 0],
 'bpd2': [1, 4, 0],
 'bwg1': [2, 0, 0],
 'bwg2': [3, 0, 0],
 'bwg3': [4, 0, 0],
 'bst1': [5, 0, 0],
 'bfn1': [6, 0, 0],
 'baw1': [7, 0, 0],
 'baw2': [7, 5, 0],
 'bwt1': [8, 0, 0],
 'bwg4': [9, 0, 0],
 'bwg5': [9, 6, 0],
 'bwg6': [10, 0, 0],
 'bjp1': [11, 0, 0],
 'blg1': [12, 0, 0],
 'bsa1': [13, 0, 0],
 'bwg7': [14, 0, 0],
 'bsa2': [15, 0, 0],
 'bsa3': [16, 0, 0],
 'bap1': [17, 0, 0],
 'bhw1': [18, 0, 0],
 'bhw2': [19, 0, 0],
 'bhw3': [20, 0, 0],
 'bhw4': [21, 0, 0],
 'bob1': [22, 0, 0],
 'bfg1': [23, 0, 0],
 'bfl1': [24, 0, 0]}
ShoesStyles = {'none': [0, 0, 0],
 'sat1': [1, 0, 0],
 'sat2': [1, 1, 0],
 'smb1': [3, 2, 0],
 'scs1': [2, 3, 0],
 'sdk1': [1, 6, 0],
 'sat3': [1, 7, 0],
 'scs2': [2, 8, 0],
 'scs3': [2, 9, 0],
 'scs4': [2, 10, 0],
 'scs7': [2, 49, 0],
 'scs8': [2, 50, 0],
 'scb1': [3, 11, 0],
 'sht1': [2, 13, 0],
 'ssb1': [3, 16, 0],
 'sts1': [1, 17, 0],
 'sts2': [1, 18, 0],
 'scs5': [2, 19, 0],
 'smb2': [3, 20, 0],
 'smb3': [3, 21, 0],
 'smb4': [3, 22, 0],
 'slf1': [1, 28, 0],
 'smt1': [3, 30, 0],
 'sox1': [1, 31, 0],
 'srb1': [3, 32, 0],
 'sst1': [3, 33, 0],
 'swb1': [3, 34, 0],
 'swb2': [3, 35, 0],
 'swk1': [2, 36, 0],
 'scs6': [2, 37, 0],
 'smb5': [3, 38, 0],
 'sht2': [2, 39, 0],
 'srb2': [3, 40, 0],
 'sts3': [1, 41, 0],
 'sts4': [1, 42, 0],
 'sts5': [1, 43, 0],
 'srb3': [3, 44, 0],
 'srb4': [3, 45, 0],
 'sat4': [1, 46, 0],
 'shw1': [3, 47, 0],
 'shw2': [3, 48, 0],
 'swt1': [1, 4, 0],
 'smj1': [2, 5, 0],
 'sfb1': [3, 12, 0],
 'smj2': [2, 14, 0],
 'smj3': [2, 15, 0],
 'sfb2': [3, 23, 0],
 'sfb3': [3, 24, 0],
 'sfb4': [3, 25, 0],
 'sfb5': [3, 26, 0],
 'sfb6': [3, 27, 0],
 'smj4': [2, 29, 0]}

def isValidHat(itemIdx, textureIdx, colorIdx):
    for style in list(HatStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True
    return False


def isValidGlasses(itemIdx, textureIdx, colorIdx):
    for style in list(GlassesStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidBackpack(itemIdx, textureIdx, colorIdx):
    for style in list(BackpackStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidShoes(itemIdx, textureIdx, colorIdx):
    for style in list(ShoesStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidAccessory(itemIdx, textureIdx, colorIdx, which):
    if which == HAT:
        return isValidHat(itemIdx, textureIdx, colorIdx)
    elif which == GLASSES:
        return isValidGlasses(itemIdx, textureIdx, colorIdx)
    elif which == BACKPACK:
        return isValidBackpack(itemIdx, textureIdx, colorIdx)
    elif which == SHOES:
        return isValidShoes(itemIdx, textureIdx, colorIdx)
    else:
        return False


class ToonDNA(AvatarDNA.AvatarDNA):

    def __init__(self, str = None, type = None, dna = None, r = None, b = None, g = None):
        if str != None:
            self.makeFromNetString(str)
        elif type != None:
            if type == 't':
                if dna == None:
                    self.newToonRandom(r, g, b)
                else:
                    self.newToonFromProperties(*dna.asTuple())
        else:
            self.type = 'u'
        self.cache = ()

    def __str__(self):
        string = 'type = toon\n'
        string = string + 'gender = %s\n' % self.gender
        string = string + 'head = %s, torso = %s, legs = %s\n' % (self.head, self.torso, self.legs)
        string = string + 'arm color = %d\n' % self.armColor
        string = string + 'glove color = %d\n' % self.gloveColor
        string = string + 'leg color = %d\n' % self.legColor
        string = string + 'head color = %d\n' % self.headColor
        string = string + 'top texture = %d\n' % self.topTex
        string = string + 'top texture color = %d\n' % self.topTexColor
        string = string + 'sleeve texture = %d\n' % self.sleeveTex
        string = string + 'sleeve texture color = %d\n' % self.sleeveTexColor
        string = string + 'bottom texture = %d\n' % self.botTex
        string = string + 'bottom texture color = %d\n' % self.botTexColor
        string = string + 'hat = (%s,%s,%s)\n' % self.hat
        string = string + 'glasses = (%s,%s,%s)\n' % self.glasses
        string = string + 'backpack = (%s,%s,%s)\n' % self.backpack
        string = string + 'shoes = (%s,%s,%s)\n' % self.shoes
        return string

    def clone(self):
        d = ToonDNA()
        d.makeFromNetString(self.makeNetString())
        return d

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 't':
            headIndex = toonHeadTypes.index(self.head)
            torsoIndex = toonTorsoTypes.index(self.torso)
            legsIndex = toonLegTypes.index(self.legs)
            dg.addUint8(headIndex)
            dg.addUint8(torsoIndex)
            dg.addUint8(legsIndex)
            if self.gender == 'm':
                dg.addUint8(1)
            else:
                dg.addUint8(0)
            dg.addUint8(self.topTex)
            dg.addUint8(self.topTexColor)
            dg.addUint8(self.sleeveTex)
            dg.addUint8(self.sleeveTexColor)
            dg.addUint8(self.botTex)
            dg.addUint8(self.botTexColor)
            dg.addUint8(self.armColor)
            dg.addUint8(self.gloveColor)
            dg.addUint8(self.legColor)
            dg.addUint8(self.headColor)
            dg.addUint8(self.hat[0])
            dg.addUint8(self.hat[1])
            dg.addUint8(self.hat[2])
            dg.addUint8(self.glasses[0])
            dg.addUint8(self.glasses[1])
            dg.addUint8(self.glasses[2])
            dg.addUint8(self.backpack[0])
            dg.addUint8(self.backpack[1])
            dg.addUint8(self.backpack[2])
            dg.addUint8(self.shoes[0])
            dg.addUint8(self.shoes[1])
            dg.addUint8(self.shoes[2])
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type: ', self.type)
        return dg.getMessage()

    def isValidNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        if dgi.getRemainingSize() not in (15, 27):
            return False
        type = dgi.getFixedString(1)
        if type not in ('t',):
            return False
        headIndex = dgi.getUint8()
        torsoIndex = dgi.getUint8()
        legsIndex = dgi.getUint8()
        if headIndex >= len(toonHeadTypes):
            return False
        if torsoIndex >= len(toonTorsoTypes):
            return False
        if legsIndex >= len(toonLegTypes):
            return False
        gender = dgi.getUint8()
        if gender == 1:
            gender = 'm'
        else:
            gender = 'f'
        topTex = dgi.getUint8()
        topTexColor = dgi.getUint8()
        sleeveTex = dgi.getUint8()
        sleeveTexColor = dgi.getUint8()
        botTex = dgi.getUint8()
        botTexColor = dgi.getUint8()
        armColor = dgi.getUint8()
        gloveColor = dgi.getUint8()
        legColor = dgi.getUint8()
        headColor = dgi.getUint8()
        if dgi.getRemainingSize():
            hat = [dgi.getUint8(), dgi.getUint8(), dgi.getUint8()]
            glasses = [dgi.getUint8(), dgi.getUint8(), dgi.getUint8()]
            backpack = [dgi.getUint8(), dgi.getUint8(), dgi.getUint8()]
            shoes = [dgi.getUint8(), dgi.getUint8(), dgi.getUint8()]
            if hat not in list(HatStyles.values()):
                return False
            if glasses not in list(GlassesStyles.values()):
                return False
            if backpack not in list(BackpackStyles.values()):
                return False
            if shoes not in list(ShoesStyles.values()):
                return False
                
        if topTex >= len(Shirts):
            return False
        if topTexColor >= len(ClothesColors):
            return False
        if sleeveTex >= len(Sleeves):
            return False
        if sleeveTexColor >= len(ClothesColors):
            return False
        if botTex >= len(Shorts):
            return False
        if botTexColor >= len(ClothesColors):
            return False
        if armColor >= len(allColorsList):
            return False
        if gloveColor >= len(allColorsList):
            return False
        if legColor >= len(allColorsList):
            return False
        if headColor >= len(allColorsList):
            return False
        return True

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 't':
            headIndex = dgi.getUint8()
            torsoIndex = dgi.getUint8()
            legsIndex = dgi.getUint8()
            self.head = toonHeadTypes[headIndex]
            self.torso = toonTorsoTypes[torsoIndex]
            self.legs = toonLegTypes[legsIndex]
            gender = dgi.getUint8()
            if gender == 1:
                self.gender = 'm'
            else:
                self.gender = 'f'
            self.topTex = dgi.getUint8()
            self.topTexColor = dgi.getUint8()
            self.sleeveTex = dgi.getUint8()
            self.sleeveTexColor = dgi.getUint8()
            self.botTex = dgi.getUint8()
            self.botTexColor = dgi.getUint8()
            self.armColor = dgi.getUint8()
            self.gloveColor = dgi.getUint8()
            self.legColor = dgi.getUint8()
            self.headColor = dgi.getUint8()
            if dgi.getRemainingSize():
                self.hat = (dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
                self.glasses = (dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
                self.backpack = (dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
                self.shoes = (dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
            else:
                self.hat = (0, 0, 0)
                self.glasses = (0, 0, 0)
                self.backpack = (0, 0, 0)
                self.shoes = (0, 0, 0)
        else:
            notify.error('unknown avatar type: ', self.type)
        return None

    def defaultColor(self):
        return 25

    def __defaultColors(self):
        color = self.defaultColor()
        self.armColor = color
        self.gloveColor = 0
        self.legColor = color
        self.headColor = color

    def newToon(self, dna, color = None):
        if len(dna) == 4:
            self.type = 't'
            self.head = dna[0]
            self.torso = dna[1]
            self.legs = dna[2]
            self.gender = dna[3]
            self.topTex = 0
            self.topTexColor = 0
            self.sleeveTex = 0
            self.sleeveTexColor = 0
            self.botTex = 0
            self.botTexColor = 0
            if color == None:
                color = self.defaultColor()
            self.armColor = color
            self.legColor = color
            self.headColor = color
            self.gloveColor = 0
            self.hat = (0, 0, 0)
            self.glasses = (0, 0, 0)
            self.backpack = (0, 0, 0)
            self.shoes = (0, 0, 0)
        else:
            notify.error("tuple must be in format ('%s', '%s', '%s', '%s')")
        return

    def newToonFromProperties(self, head, torso, legs, gender, armColor, gloveColor, legColor, headColor, topTexture, topTextureColor, sleeveTexture, sleeveTextureColor, bottomTexture, bottomTextureColor, hat=(0, 0, 0), glasses=(0, 0, 0), backpack=(0, 0, 0), shoes=(0, 0, 0)):
        self.type = 't'
        self.head = head
        self.torso = torso
        self.legs = legs
        self.gender = gender
        self.armColor = armColor
        self.gloveColor = gloveColor
        self.legColor = legColor
        self.headColor = headColor
        self.topTex = topTexture
        self.topTexColor = topTextureColor
        self.sleeveTex = sleeveTexture
        self.sleeveTexColor = sleeveTextureColor
        self.botTex = bottomTexture
        self.botTexColor = bottomTextureColor
        self.hat = hat
        self.glasses = glasses
        self.backpack = backpack
        self.shoes = shoes

    def updateToonProperties(self, head = None, torso = None, legs = None, gender = None, armColor = None, gloveColor = None, legColor = None, headColor = None, topTexture = None, topTextureColor = None, sleeveTexture = None, sleeveTextureColor = None, bottomTexture = None, bottomTextureColor = None, shirt = None, bottom = None, hat=(0, 0, 0), glasses=(0, 0, 0), backpack=(0, 0, 0), shoes=(0, 0, 0)):
        if head:
            self.head = head
        if torso:
            self.torso = torso
        if legs:
            self.legs = legs
        if gender:
            self.gender = gender
        if armColor:
            self.armColor = armColor
        if gloveColor:
            self.gloveColor = gloveColor
        if legColor:
            self.legColor = legColor
        if headColor:
            self.headColor = headColor
        if topTexture:
            self.topTex = topTexture
        if topTextureColor:
            self.topTexColor = topTextureColor
        if sleeveTexture:
            self.sleeveTex = sleeveTexture
        if sleeveTextureColor:
            self.sleeveTexColor = sleeveTextureColor
        if bottomTexture:
            self.botTex = bottomTexture
        if bottomTextureColor:
            self.botTexColor = bottomTextureColor
        if shirt:
            str, colorIndex = shirt
            defn = ShirtStyles[str]
            self.topTex = defn[0]
            self.topTexColor = defn[2][colorIndex][0]
            self.sleeveTex = defn[1]
            self.sleeveTexColor = defn[2][colorIndex][1]
        if bottom:
            str, colorIndex = bottom
            defn = BottomStyles[str]
            self.botTex = defn[0]
            self.botTexColor = defn[1][colorIndex]
        self.hat = hat
        self.glasses = glasses
        self.backpack = backpack
        self.shoes = shoes

    def newToonRandom(self, seed = None, gender = 'm', npc = 0, stage = None):
        if seed:
            generator = random.Random()
            generator.seed(seed)
        else:
            generator = random
        self.type = 't'
        self.legs = generator.choice(toonLegTypes + ['m',
         'l',
         'l',
         'l'])
        self.gender = gender
        if not npc:
            if stage == MAKE_A_TOON:
                if not base.cr.isPaid():
                    animalIndicesToUse = allToonHeadAnimalIndicesTrial
                else:
                    animalIndicesToUse = allToonHeadAnimalIndices
                animal = generator.choice(animalIndicesToUse)
                self.head = toonHeadTypes[animal]
            else:
                self.head = generator.choice(toonHeadTypes)
        else:
            self.head = generator.choice(toonHeadTypes[:22])
        top, topColor, sleeve, sleeveColor = getRandomTop(generator=generator)
        bottom, bottomColor = getRandomBottom(generator=generator)
        if gender == 'm':
            self.torso = generator.choice(toonTorsoTypes[:3])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            self.botTex = bottom
            self.botTexColor = bottomColor
            color = generator.choice(defaultColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        else:
            self.torso = generator.choice(toonTorsoTypes[:6])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            if self.torso[1] == 'd':
                bottom, bottomColor = getRandomBottom(generator=generator, girlBottomType=SKIRT)
            else:
                bottom, bottomColor = getRandomBottom(generator=generator, girlBottomType=SHORTS)
            self.botTex = bottom
            self.botTexColor = bottomColor
            color = generator.choice(defaultColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        self.gloveColor = 0
        self.hat = (0, 0, 0)
        self.glasses = (0, 0, 0)
        self.backpack = (0, 0, 0)
        self.shoes = (0, 0, 0)

    def asTuple(self):
        return (self.head,
         self.torso,
         self.legs,
         self.gender,
         self.armColor,
         self.gloveColor,
         self.legColor,
         self.headColor,
         self.topTex,
         self.topTexColor,
         self.sleeveTex,
         self.sleeveTexColor,
         self.botTex,
         self.botTexColor,
         self.hat,
         self.glasses,
         self.backpack,
         self.shoes)

    def getType(self):
        if self.type == 't':
            type = self.getAnimal()
        else:
            notify.error('Invalid DNA type: ', self.type)
        return type

    def getAnimal(self):
        if self.head[0] == 'd':
            return 'dog'
        elif self.head[0] == 'c':
            return 'cat'
        elif self.head[0] == 'm':
            return 'mouse'
        elif self.head[0] == 'h':
            return 'horse'
        elif self.head[0] == 'r':
            return 'rabbit'
        elif self.head[0] == 'f':
            return 'duck'
        elif self.head[0] == 'p':
            return 'monkey'
        elif self.head[0] == 'b':
            return 'bear'
        elif self.head[0] == 's':
            return 'pig'
        else:
            notify.error('unknown headStyle: ', self.head[0])

    def getHeadSize(self):
        if self.head[1] == 'l':
            return 'long'
        elif self.head[1] == 's':
            return 'short'
        else:
            notify.error('unknown head size: ', self.head[1])

    def getMuzzleSize(self):
        if self.head[2] == 'l':
            return 'long'
        elif self.head[2] == 's':
            return 'short'
        else:
            notify.error('unknown muzzle size: ', self.head[2])

    def getTorsoSize(self):
        if self.torso[0] == 'l':
            return 'long'
        elif self.torso[0] == 'm':
            return 'medium'
        elif self.torso[0] == 's':
            return 'short'
        else:
            notify.error('unknown torso size: ', self.torso[0])

    def getLegSize(self):
        if self.legs == 'l':
            return 'long'
        elif self.legs == 'm':
            return 'medium'
        elif self.legs == 's':
            return 'short'
        else:
            notify.error('unknown leg size: ', self.legs)

    def getGender(self):
        return self.gender

    def getClothes(self):
        if len(self.torso) == 1:
            return 'naked'
        elif self.torso[1] == 's':
            return 'shorts'
        elif self.torso[1] == 'd':
            return 'dress'
        else:
            notify.error('unknown clothing type: ', self.torso[1])

    def getArmColor(self):
        try:
            return allColorsList[self.armColor]
        except:
            return allColorsList[0]

    def getLegColor(self):
        try:
            return allColorsList[self.legColor]
        except:
            return allColorsList[0]

    def getHeadColor(self):
        try:
            return allColorsList[self.headColor]
        except:
            return allColorsList[0]

    def getGloveColor(self):
        try:
            return allColorsList[self.gloveColor]
        except:
            return allColorsList[0]

    def getBlackColor(self):
        try:
            return allColorsList[26]
        except:
            return allColorsList[0]

    def setTemporary(self, newHead, newArmColor, newLegColor, newHeadColor):
        if not self.cache and self.getArmColor != newArmColor:
            self.cache = (self.head,
             self.armColor,
             self.legColor,
             self.headColor)
            self.updateToonProperties(head=newHead, armColor=newArmColor, legColor=newLegColor, headColor=newHeadColor)

    def restoreTemporary(self, oldStyle):
        cache = ()
        if oldStyle:
            cache = oldStyle.cache
        if cache:
            self.updateToonProperties(head=cache[0], armColor=cache[1], legColor=cache[2], headColor=cache[3])
            if oldStyle:
                oldStyle.cache = ()
