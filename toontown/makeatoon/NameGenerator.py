from panda3d.core import *
import random
import copy
from toontown.toonbase import ToontownGlobals
import os
from direct.directnotify import DirectNotifyGlobal
import sys
from io import StringIO
from toontown.makeatoon import ToonNamesEnglish

class NameGenerator:
    text = TextNode('text')
    text.setFont(ToontownGlobals.getInterfaceFont())
    notify = DirectNotifyGlobal.directNotify.newCategory('NameGenerator')
    titles = []
    firsts = []
    capPrefixes = []
    lastPrefixes = []
    lastSuffixes = []

    def __init__(self):
        self.generateLists()

    def generateLists(self):
        self.titles = []
        self.firsts = []
        self.capPrefixes = []
        self.lastPrefixes = []
        self.lastSuffixes = []
        self.nameDictionary = {}
        dataInput = StringIO(ToonNamesEnglish.TOONNAMES)
        currentLine = dataInput.readline()
        while currentLine:
            if currentLine.lstrip()[0:1] != '#':
                a1 = currentLine.find('*')
                a2 = currentLine.find('*', a1 + 1)
                self.nameDictionary[int(currentLine[0:a1])] = (int(currentLine[a1 + 1:a2]), currentLine[a2 + 1:].rstrip())
            currentLine = dataInput.readline()

        masterList = [self.titles,
         self.firsts,
         self.capPrefixes,
         self.lastPrefixes,
         self.lastSuffixes]
        for tu in list(self.nameDictionary.values()):
            masterList[tu[0]].append(tu[1])

        return 1

    def _getNameParts(self, cat2part):
        nameParts = [{}, {}, {}, {}]
        for id, tpl in self.nameDictionary.items():
            cat, str = tpl
            if cat in cat2part:
                nameParts[cat2part[cat]][str] = id

        return nameParts
        
    def getNameParts(self):
        return self._getNameParts({0: 0,
         1: 1,
         2: 2,
         3: 2,
         4: 3})

    def getLastNamePrefixesCapped(self):
        return self.capPrefixes

    def returnUniqueID(self, name, listnumber):
        newtu = [(), (), ()]
        if listnumber == 0:
            newtu[0] = (0, name)
            newtu[1] = (0, name)
            newtu[2] = (0, name)
        elif listnumber == 1:
            newtu[0] = (1, name)
            newtu[1] = (1, name)
            newtu[2] = (1, name)
        elif listnumber == 2:
            newtu[0] = (2, name)
            newtu[1] = (3, name)
        else:
            newtu[0] = (4, name)
        for tu in list(self.nameDictionary.items()):
            for g in newtu:
                if tu[1] == g:
                    return tu[0]

        return -1

    def findWidestInList(self, text, nameList):
        maxWidth = 0
        maxName = ''
        for name in nameList:
            width = text.calcWidth(name)
            if width > maxWidth:
                maxWidth = text.calcWidth(name)
                maxName = name

        print(maxName + ' ' + str(maxWidth))
        return maxName

    def findWidestName(self):
        longestTitle = self.findWidestInList(self.text, self.titles)
        longestFirst = self.findWidestInList(self.text, self.firsts)
        longestLastPrefix = self.findWidestInList(self.text, self.lastPrefixes)
        longestLastSuffix = self.findWidestInList(self.text, self.lastSuffixes)
        longestName = longestTitle + ' ' + longestFirst + ' ' + longestLastPrefix + longestLastSuffix
        return longestName

    def findWidestTitleFirst(self):
        widestTitle = self.findWidestInList(self.text, self.titles)
        widestFirst = self.findWidestInList(self.text, self.firsts)
        
        return widestTitle + ' ' + widestFirst

    def findWidestTitle(self):
        widestTitle = self.findWidestInList(self.text, self.titles)
        return widestTitle

    def findWidestFirstName(self):
        widestFirst = self.findWidestInList(self.text, self.firsts)
        return widestFirst

    def findWidestLastName(self):
        longestLastPrefix = self.findWidestInList(self.text, self.lastPrefixes)
        longestLastSuffix = self.findWidestInList(self.text, self.lastSuffixes)
        longestLastName = longestLastPrefix + longestLastSuffix
        return longestLastName

    def findWidestNameWord(self):
        widestWord = self.findWidestInList(self.text, [self.findWidestTitle(), self.findWidestFirstName(), self.findWidestLastName()])
        return widestWord

    def findWidestNameWidth(self):
        name = self.findWidestName()
        return self.text.calcWidth(name)

    def printWidestName(self):
        name = self.findWidestName()
        width = self.text.calcWidth(name)
        widthStr = str(width)
        print('The widest name is: ' + name + ' (' + widthStr + ' units)')

    def printWidestLastName(self):
        name = self.findWidestLastName()
        width = self.text.calcWidth(name)
        widthStr = str(width)
        print('The widest last name is: ' + name + ' (' + widthStr + ' units)')

    def randomName(self):
        uberFlag = random.choice(['title-first',
         'title-last',
         'first',
         'last',
         'first-last',
         'title-first-last'])
        titleFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'title-last' or uberFlag == 'title-first-last':
            titleFlag = 1
        firstFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'first' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            firstFlag = 1
        lastFlag = 0
        if uberFlag == 'title-last' or uberFlag == 'last' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            lastFlag = 1
        retString = ''
        if titleFlag:
            retString += random.choice(self.titles) + ' '
        if firstFlag:
            retString += random.choice(self.firsts)
            if lastFlag:
                retString += ' '
        if lastFlag:
            lastPrefix = random.choice(self.lastPrefixes)
            lastSuffix = random.choice(self.lastSuffixes)
            if lastPrefix in self.capPrefixes:
                lastSuffix = lastSuffix.capitalize()
            retString += lastPrefix + lastSuffix
        return retString

    def randomNameMoreinfo(self):
        uberFlag = random.choice(['title-first',
         'title-last',
         'first',
         'last',
         'first-last',
         'title-first-last'])
        titleFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'title-last' or uberFlag == 'title-first-last':
            titleFlag = 1
        firstFlag = 0
        if uberFlag == 'title-first' or uberFlag == 'first' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            firstFlag = 1
        lastFlag = 0
        if uberFlag == 'title-last' or uberFlag == 'last' or uberFlag == 'first-last' or uberFlag == 'title-first-last':
            lastFlag = 1
        retString = ''
        uberReturn = [0,
         0,
         0,
         '',
         '',
         '',
         '']
        uberReturn[0] = titleFlag
        uberReturn[1] = firstFlag
        uberReturn[2] = lastFlag
        uberReturn[3] = random.choice(self.titles)
        uberReturn[4] = random.choice(self.firsts)
        lastPrefix = random.choice(self.lastPrefixes)
        lastSuffix = random.choice(self.lastSuffixes)
        if lastPrefix in self.capPrefixes:
            lastSuffix = lastSuffix.capitalize()
        uberReturn[5] = lastPrefix
        uberReturn[6] = lastSuffix
        if titleFlag:
            retString += uberReturn[3] + ' '
        if firstFlag:
            retString += uberReturn[4]
            if lastFlag:
                retString += ' '
        if lastFlag:
            retString += uberReturn[5] + uberReturn[6]
        uberReturn.append(retString)
        return uberReturn

    def printRandomNames(self, total = 1):
        i = 0
        while i < total:
            name = self.randomName()
            width = self.text.calcWidth(name)
            widthStr = str(width)
            print('Toon: ' + name + ' (' + widthStr + ' units)')
            i += 1

    def percentOver(self, limit = 9.0, samples = 1000):
        i = 0
        over = 0
        while i < samples:
            name = self.randomName()
            width = self.text.calcWidth(name)
            if width > limit:
                over += 1
            i += 1

        percent = float(over) / float(samples) * 100
        print('Samples: ' + str(samples) + ' Over: ' + str(over) + ' Percent: ' + str(percent))

    def totalNames(self):
        firsts = len(self.boyFirsts) + len(self.girlFirsts) + len(self.neutralFirsts)
        print('Total firsts: ' + str(firsts))
        lasts = len(self.lastPrefixes) * len(self.lastSuffixes)
        print('Total lasts: ' + str(lasts))
        neutralTitleFirsts = len(self.neutralTitles) * len(self.neutralFirsts)
        boyTitleFirsts = len(self.boyTitles) * (len(self.neutralFirsts) + len(self.boyFirsts)) + len(self.neutralTitles) * len(self.boyFirsts)
        girlTitleFirsts = len(self.girlTitles) * (len(self.neutralFirsts) + len(self.girlFirsts)) + len(self.neutralTitles) * len(self.girlFirsts)
        totalTitleFirsts = neutralTitleFirsts + boyTitleFirsts + girlTitleFirsts
        print('Total title firsts: ' + str(totalTitleFirsts))
        neutralTitleLasts = len(self.neutralTitles) * lasts
        boyTitleLasts = len(self.boyTitles) * lasts
        girlTitleLasts = len(self.girlTitles) * lasts
        totalTitleLasts = neutralTitleLasts + boyTitleFirsts + girlTitleLasts
        print('Total title lasts: ' + str(totalTitleLasts))
        neutralFirstLasts = len(self.neutralFirsts) * lasts
        boyFirstLasts = len(self.boyFirsts) * lasts
        girlFirstLasts = len(self.girlFirsts) * lasts
        totalFirstLasts = neutralFirstLasts + boyFirstLasts + girlFirstLasts
        print('Total first lasts: ' + str(totalFirstLasts))
        neutralTitleFirstLasts = neutralTitleFirsts * lasts
        boyTitleFirstLasts = boyTitleFirsts * lasts
        girlTitleFirstLasts = girlTitleFirsts * lasts
        totalTitleFirstLasts = neutralTitleFirstLasts + boyTitleFirstLasts + girlTitleFirstLasts
        print('Total title first lasts: ' + str(totalTitleFirstLasts))
        totalNames = firsts + lasts + totalTitleFirsts + totalTitleLasts + totalFirstLasts + totalTitleFirstLasts
        print('Total Names: ' + str(totalNames))
