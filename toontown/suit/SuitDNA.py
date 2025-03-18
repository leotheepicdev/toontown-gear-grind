import random
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toonbase import TTLocalizer
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from toontown.suit import SuitGlobals
notify = directNotify.newCategory('SuitDNA')
index2Suits = {0: ['f', 'p', 'ym', 'mm', 'ds', 'hh', 'cr', 'tbc'],
 1: ['bf', 'b', 'dt', 'ac', 'bs', 'sd', 'le', 'bw'],
 2: ['sc', 'pp', 'tw', 'bc', 'nc', 'mb', 'ls', 'rb'],
 3: ['cc', 'tm', 'nd', 'gh', 'ms', 'tf', 'm', 'mh']}
suitHeadTypes = ['f',
 'p',
 'ym',
 'mm',
 'ds',
 'hh',
 'cr',
 'tbc',
 'bf',
 'b',
 'dt',
 'ac',
 'bs',
 'sd',
 'le',
 'bw',
 'sc',
 'pp',
 'tw',
 'bc',
 'nc',
 'mb',
 'ls',
 'rb',
 'cc',
 'tm',
 'nd',
 'gh',
 'ms',
 'tf',
 'm',
 'mh']
buildingCogTier2Options = {
 'c': {1: ['f', 'st'],
       2: ['p'],
       3: ['ym', 'po'],
       4: ['mm'],
       5: ['ds', 'bh'],
       6: ['hh'],
       7: ['cr', 'wk'],
       8: ['tbc']},
 'l': {1: ['bf', 'bd'],
       2: ['b'],
       3: ['dt', 'dc'],
       4: ['ac'],
       5: ['bs', 'r'],
       6: ['sd'],
       7: ['le', 'tms'],
       8: ['bw']},
 'm': {1: ['sc', 'sl'],
       2: ['pp'],
       3: ['tw', 'pb'],
       4: ['bc'],
       5: ['nc', 'gb'],
       6: ['mb'],
       7: ['ls', 'fc'],
       8: ['rb']},
 's': {1: ['cc', 'sb'],
       2: ['tm'],
       3: ['nd', 'fcs'],
       4: ['gh'],
       5: ['ms', 'bb'],
       6: ['tf'],
       7: ['m', 'hd'],      
       8: ['mh']}
}
buildingCogs = [
  'st',
  'po',
  'bh',
  'wk',
  'bd',
  'dc',
  'r',
  'tms',
  'sl',
  'pb',
  'gb',
  'fc',
  'sb',
  'fcs',
  'bb',
  'hd'
]
customTypes = ['null']
suitATypes = ['ym',
 'bh',
 'hh',
 'tbc',
 'dt',
 'dc',
 'bs',
 'le',
 'tms',
 'bw',
 'pp',
 'pb',
 'nc',
 'rb',
 'nd',
 'fcs',
 'tf',
 'm',
 'hd',
 'mh']
suitBTypes = ['p',
 'po',
 'ds',
 'wk',
 'b',
 'ac',
 'r',
 'sd',
 'sl',
 'bc',
 'ls',
 'tm',
 'ms',
 'bb']
suitCTypes = ['f',
 'st',
 'mm',
 'cr',
 'bf',
 'bd',
 'sc',
 'tw',
 'gb',
 'mb',
 'fc',
 'cc',
 'sb',
 'gh']
suitDepts = ['c',
 'l',
 'm',
 's']
suitDeptFullnames = {'c': TTLocalizer.Bossbot,
 'l': TTLocalizer.Lawbot,
 'm': TTLocalizer.Cashbot,
 's': TTLocalizer.Sellbot}
suitDeptFullnamesP = {'c': TTLocalizer.BossbotP,
 'l': TTLocalizer.LawbotP,
 'm': TTLocalizer.CashbotP,
 's': TTLocalizer.SellbotP}
corpPolyColor = VBase4(0.95, 0.75, 0.75, 1.0)
legalPolyColor = VBase4(0.75, 0.75, 0.95, 1.0)
moneyPolyColor = VBase4(0.65, 0.95, 0.85, 1.0)
salesPolyColor = VBase4(0.95, 0.75, 0.95, 1.0)
suitsPerLevel = [1,
 1,
 1,
 1,
 1,
 1,
 1,
 1]
suitsPerDept = 8
goonTypes = ['pg', 'sg']

def getSuitBodyType(name):
    if name in suitATypes:
        return 'a'
    elif name in suitBTypes:
        return 'b'
    elif name in suitCTypes:
        return 'c'
    else:
        print('Unknown body type for suit name: ', name)


def getSuitDept(name):
    dept = SuitGlobals.getDept(name)
    if dept:
        return dept
    print('Unknown dept for suit name: ', name)
    return None


def getDeptFullname(dept):
    if dept in suitDeptFullnames:
        return suitDeptFullnames[dept]
    return ''


def getDeptFullnameP(dept):
    if dept in suitDeptFullnames:
        return suitDeptFullnamesP[dept]
    return ''


def getSuitDeptFullname(name):
    return suitDeptFullnames[getSuitDept(name)]


def getSuitType(name):
    return SuitGlobals.getTier(name)


def getRandomSuitType(level, rng = random):
    return random.randint(max(level - 4, 1), min(level, 8))

def getRandomSuitTypeStreet(level, rng = random):
    return random.randint(max(level - 4, 1), min(level, 6))

def getRandomSuitByDept(dept):
    deptNumber = suitDepts.index(dept)
    return suitHeadTypes[suitsPerDept * deptNumber + random.randint(0, 7)]


class SuitDNA(AvatarDNA.AvatarDNA):

    def __init__(self, str = None, type = None, dna = None, r = None, b = None, g = None):
        if str != None:
            self.makeFromNetString(str)
        elif type != None:
            if type == 's':
                self.newSuit()
        else:
            self.type = 'u'
        self.size = 0
        self.height = 0
        self.variant = 0

    def __str__(self):
        if self.type == 's':
            return 'type = %s\nbody = %s, dept = %s, name = %s' % ('suit',
             self.body,
             self.dept,
             self.name)
        elif self.type == 'b':
            return 'type = boss cog\ndept = %s' % self.dept
        else:
            return 'type undefined'

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 's':
            dg.addFixedString(self.name, 4)
            dg.addFixedString(self.dept, 4)
            dg.addFixedString(self.body, 1)
            dg.addFixedString(str(self.size), 20)
            dg.addFixedString(str(self.height), 20)
            dg.addFixedString(str(self.variant), 1)
        elif self.type == 'b':
            dg.addFixedString(self.dept, 1)
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type: ', self.type)
        return dg.getMessage()

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 's':
            self.name = dgi.getFixedString(4)
            self.dept = dgi.getFixedString(4)
            self.body = dgi.getFixedString(1)
            self.size = float(dgi.getFixedString(20))
            self.height = float(dgi.getFixedString(20))
            self.variant = float(dgi.getFixedString(1))
        elif self.type == 'b':
            self.dept = dgi.getFixedString(1)
        else:
            notify.error('unknown avatar type: ', self.type)
        return None

    def __defaultGoon(self):
        self.type = 'g'
        self.name = goonTypes[0]

    def __defaultSuit(self):
        self.type = 's'
        self.name = 'ds'
        self.dept = getSuitDept(self.name)
        self.body = getSuitBodyType(self.name)
        self.size = SuitGlobals.getScale(self.name)
        self.height = SuitGlobals.getHeight(self.name)

    def newSuit(self, name = None):
        if name == None:
            self.__defaultSuit()
        else:
            self.type = 's'
            self.name = name
            self.dept = getSuitDept(self.name)
            self.body = getSuitBodyType(self.name)
            self.size = SuitGlobals.getScale(self.name)
            self.height = SuitGlobals.getHeight(self.name)

    def newBossCog(self, dept):
        self.type = 'b'
        self.dept = dept

    def newSuitRandom(self, level = None, dept = None):
        self.type = 's'
        if level == None:
            level = random.choice(list(range(1, len(suitsPerLevel))))
        elif level < 0 or level > len(suitsPerLevel):
            notify.error('Invalid suit level: %d' % level)
        if dept == None:
            dept = random.choice(suitDepts)
        self.dept = dept
        index = suitDepts.index(dept)
        base = index * suitsPerDept
        offset = 0
        if level > 1:
            for i in range(1, level):
                offset = offset + suitsPerLevel[i - 1]

        bottom = base + offset
        top = bottom + suitsPerLevel[level - 1]
        self.name = suitHeadTypes[random.choice(list(range(bottom, top)))]
        self.body = getSuitBodyType(self.name)
        self.size = SuitGlobals.getScale(self.name)
        self.height = SuitGlobals.getHeight(self.name)
        if self.name in SuitGlobals.Suit2VariantChance:
            self.variant = random.choice(SuitGlobals.Suit2VariantChance[self.name])
            
    def newSuitBuilding(self, level, dept, chance, street=False):
        self.type = 's'
        self.dept = dept
        if street:
            _type = getRandomSuitTypeStreet(level)
        else:
            _type = getRandomSuitType(level)
        potentialNames = buildingCogTier2Options[dept][_type]
        potentialNamesLen = len(potentialNames)
        if potentialNamesLen == 1:
            self.name = potentialNames[0]
        elif len(potentialNames) == 2:
            if random.random() <= chance:
                self.name = potentialNames[0]
            else:
                self.name = potentialNames[1]

        self.body = getSuitBodyType(self.name)
        self.size = SuitGlobals.getScale(self.name)
        self.height = SuitGlobals.getHeight(self.name)
        if self.name in SuitGlobals.Suit2VariantChance:
            self.variant = random.choice(SuitGlobals.Suit2VariantChance[self.name])    
        
    def newSuitNull(self, level):
        self.type = 's'
        self.dept = 'null'
        self.name = 'null'
        self.body = random.choice(['a', 'b', 'c'])
        if self.body == 'a':
            self.size = random.choice(SuitGlobals.CogAScales)
        elif self.body == 'b':
            self.size = random.choice(SuitGlobals.CogBScales)
        elif self.body == 'c':
            self.size = random.choice(SuitGlobals.CogCScales)
        self.height = SuitGlobals.Scale2Height[self.size]

    def newGoon(self, name = None):
        if type == None:
            self.__defaultGoon()
        else:
            self.type = 'g'
            if name in goonTypes:
                self.name = name
            else:
                notify.error('unknown goon type: ', name)
        return

    def getType(self):
        if self.type == 's':
            type = 'suit'
        elif self.type == 'b':
            type = 'boss'
        else:
            notify.error('Invalid DNA type: ', self.type)
        return type
