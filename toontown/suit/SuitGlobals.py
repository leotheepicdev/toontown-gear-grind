aSize = 6.06
bSize = 5.29
cSize = 4.14

# name: dept, tier, scale, height
cogInfo = {
 'f': ('c', 1, 4.0 / cSize, 4.88), 
 'st': ('c', 1, 4.2 / cSize, 5.18),
 'p': ('c', 2, 3.35 / bSize, 5.0),
 'ym': ('c', 3, 4.125 / aSize, 5.28),
 'po': ('c', 3, 4.25 / bSize, 5.63),
 'mm': ('c', 4, 2.5 / cSize, 3.25),
 'ds': ('c', 5, 4.5 / bSize, 6.08),
 'bh': ('c', 5, 5.75 / aSize, 7.45),
 'hh': ('c', 6, 6.5 / aSize, 7.45),
 'cr': ('c', 7, 6.75 / cSize, 8.23),
 'wk': ('c', 7, 6.75 / bSize, 8.69),
 'tbc': ('c', 8, 7.0 / aSize, 9.34),
 'bf': ('l', 1, 4.0 / cSize, 4.81),
 'bd': ('l', 1, 4.0 / cSize, 4.88),
 'b': ('l', 2, 4.375 / bSize, 6.17),
 'dt': ('l', 3, 4.25 / aSize, 5.63),
 'dc': ('l', 3, 4.375 / aSize, 5.755),
 'ac': ('l', 4, 4.35 / bSize, 6.39),
 'bs': ('l', 5, 4.5 / aSize, 6.71),
 'r': ('l', 5, 4.95 / bSize, 6.39),
 'sd': ('l', 6, 5.65 / bSize, 7.9),
 'le': ('l', 7, 7.125 / aSize, 8.27),
 'tms': ('l', 7, 7.0 / aSize, 8.69),
 'bw': ('l', 8, 7.0 / aSize, 8.69),
 'sc': ('m', 1, 3.6 / cSize, 4.77),
 'sl': ('m', 1, 3.75 / bSize, 4.81),
 'pp': ('m', 2, 3.55 / aSize, 5.26),
 'tw': ('m', 3, 4.5 / cSize, 5.41),
 'pb': ('m', 3, 4.3 / aSize, 5.41),
 'bc': ('m', 4, 4.4 / bSize, 5.95),
 'nc': ('m', 5, 5.25 / aSize, 7.22),
 'gb': ('m', 5, 5.25 / cSize, 6.61),
 'mb': ('m', 6, 5.3 / cSize, 6.97),
 'ls': ('m', 7, 6.5 / bSize, 8.58),
 'fc': ('m', 7, 6.5 / cSize, 8.08),
 'rb': ('m', 8, 7.0 / aSize, 8.95),
 'cc': ('s', 1, 3.5 / cSize, 4.63),
 'sb': ('s', 1, 4.0 / cSize, 4.81),
 'tm': ('s', 2, 3.75 / bSize, 5.18),
 'nd': ('s', 3, 4.35 / aSize, 5.88),
 'fcs': ('s', 3, 4.35 / aSize, 5.88),
 'gh': ('s', 4, 4.75 / cSize, 6.4),
 'ms': ('s', 5, 4.75 / bSize, 6.4),
 'bb': ('s', 5, 5.0 / bSize, 6.71),
 'tf': ('s', 6, 5.25 / aSize, 6.95),
 'm': ('s', 7, 5.75 / aSize, 7.61),
 'hd': ('s', 7, 5.75 / aSize, 7.61),
 'mh': ('s', 8, 7.0 / aSize, 8.95),
 'null': ('null', 1, 0, 0)
}

def getDept(suitName):
    if suitName in cogInfo:
        return cogInfo[suitName][0]
    return None
    
def getTier(suitName):
    if suitName in cogInfo:
        return cogInfo[suitName][1]
    return None

def getScale(suitName):
    if suitName in cogInfo:
        return cogInfo[suitName][2]
    return None
    
def getHeight(suitName):
    if suitName in cogInfo:
        return cogInfo[suitName][3]
    return None

Suit2VariantChance = {'le': [0, 0, 0, 0, 0, 1],
}
Scale2Height = {3.55 / aSize: 3.55,
 4.125 / aSize: 5.28,
 4.25 / aSize: 5.63,
 4.35 / aSize: 6.39,
 4.5 / aSize: 6.71,
 5.25 / aSize: 6.95,
 5.75 / aSize: 7.61,
 6.5 / aSize: 7.45,
 7.0 / aSize: 8.95,
 7.125 / aSize: 8.27,
 3.35 / bSize: 5.0,
 3.75 / bSize: 5.24,
 4.35 / bSize: 6.39,
 4.375 / bSize: 6.17,
 4.4 / bSize: 5.95,
 4.5 / bSize: 5.41,
 4.75 / bSize: 5.98,
 5.65 / bSize: 7.9,
 6.5 / bSize: 8.58,
 2.5 / cSize: 3.25,
 3.5 / cSize: 4.65,
 3.6 / cSize: 4.77,
 4.0 / cSize: 4.81,
 4.5 / cSize: 5.41,
 4.75 / cSize: 6.4,
 5.3 / cSize: 6.97,
 6.75 / cSize: 8.23}
CogAScales = [3.55 / aSize,
 4.125 / aSize,
 4.25 / aSize,
 4.35 / aSize,
 4.5 / aSize,
 5.25 / aSize,
 5.75 / aSize,
 6.5 / aSize,
 7.0 / aSize,
 7.125 / aSize]
CogBScales = [3.35 / bSize,
 3.75 / bSize,
 4.35 / bSize,
 4.375 / bSize,
 4.4 / bSize,
 4.5 / bSize,
 4.75 / bSize,
 5.65 / bSize,
 6.5 / bSize]
CogCScales = [2.5 / cSize,
 3.5 / cSize,
 3.6 / cSize,
 4.0 / cSize,
 4.5 / cSize,
 4.75 / cSize,
 5.3 / cSize,
 6.75 / cSize,
]