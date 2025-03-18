from .MagicWordGlobals import *

class MagicWordDispatcher:

    def __init__(self):
        self.words = {}

    def register(self, aliases, info):
        for alias in aliases:
            self.words[alias] = info

    def merge(self, words):
        self.words.update(words)

    def getWord(self, word):
        return self.words.get(word, None)

    def getAccess(self, word):
        word = self.getWord(word)
        if word:
            return word.get('access')

    def getArgTypes(self, word):
        word = self.getWord(word)
        if word:
            return word.get('argTypes', [])

    def getCallback(self, word):
        word = self.getWord(word)
        if word:
            return word.get('callback')

    def getTargetClass(self, word):
        word = self.getWord(word)
        if word:
            return word.get('class', [])

    def getTargetType(self, word):
        word = self.getWord(word)
        if word:
            return word.get('target')

    def getDefaults(self, word):
        word = self.getWord(word)
        if word:
            return word.get('defaults', {})

    def checkIfWordIsValid(self, wordName, av, target, extraArgs):
        targetType = self.getTargetType(wordName)
        if targetType == TARGET_SELF:
            if av.doId != target.doId:
                return (False, 0, [])
        elif targetType == TARGET_OTHER:
            if av.doId == target.doId:
                return (False, 1, [])

        if target.__class__.__name__ == 'DistributedToonAI' and target.doId != av.doId:
            if target.getAccessLevel() >= av.getAccessLevel():
                return (False, 7, [])

        argTypes = self.getArgTypes(wordName)

        maxArgs = len(argTypes)
        minArgs = 0
        for i in range(0, maxArgs):
            arg, required = argTypes[i][0], argTypes[i][1]
            if required:
                minArgs += 1

        args = extraArgs.split(None, maxArgs-1)
        if len(args) < minArgs:
            return (False, 3, [])

        parsedArgs = []

        for i in range(0, maxArgs):
            argtype = argTypes[i][0]
            required = argTypes[i][0]
            try:
                args[i]
            except:
                args.append(self.getDefaults(wordName)[i])
            if argtype == int:
                try:
                    parsedArg = int(args[i])
                except:
                    return (False, 4, [])
            elif argtype == float:
                try:
                    parsedArg = float(args[i])
                except:
                    return (False, 4, [])
            else:
                parsedArg = str(args[0])
            parsedArgs.append(parsedArg)

        return (True, '', parsedArgs)