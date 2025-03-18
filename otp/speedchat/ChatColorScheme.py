from .ColorSpace import *

class ChatColorScheme:

    def __init__(self, frameColor = None, textDisabledColor = (0.4, 0.4, 0.4), alpha = 0.95):

        def scaleColor(color, s):
            y, u, v = rgb2yuv(*color)
            return yuv2rgb(y * s, u, v)

        def scaleIfNone(color, srcColor, s):
            if color is not None:
                return color
            else:
                return scaleColor(srcColor, s)
            return

        self.__frameColor = frameColor
        if self.__frameColor is None:
            h, s, v = rgb2hsv(*arrowColor)
            self.__frameColor = hsv2rgb(h, 0.2 * s, v)
        h, s, v = rgb2hsv(*self.__frameColor)
        self.__frameColor = hsv2rgb(h, 0.5 * s, v)
        self.__textColor = (0, 0, 0)
        self.__textDisabledColor = textDisabledColor
        self.__alpha = alpha
        
    def getFrameColor(self):
        return self.__frameColor
        
    def getRolloverColor(self):
        return None

    def getPressedColor(self):
        return self.__pressedColor

    def getTextColor(self):
        return self.__textColor

    def getTextDisabledColor(self):
        return self.__textDisabledColor

    def getAlpha(self):
        return self.__alpha

    def __str__(self):
        members = ('frameColor', 'pressedColor', 'textColor', 'textDisabledColor', 'alpha')
        result = ''
        for member in members:
            result += '%s = %s' % (member, self.__dict__['_%s__%s' % (self.__class__.__name__, member)])
            if member is not members[-1]:
                result += '\n'

        return result

    def __repr__(self):
        return str(self)
