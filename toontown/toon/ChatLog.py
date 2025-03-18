from direct.gui.DirectGui import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals

class ChatLog(DirectFrame):
    VISIBLE_MSG_COUNT = 5

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopLeft, relief=None, pos=(0.9, 0, -0.2))
        self.initialiseoptions(ChatLog)
        self.chatlog = DirectScrolledList(parent=self,
            decButton_relief = None,
            incButton_relief = None,
            itemFrame_geom =(loader.loadModel('phase_3/models/gui/toon_council').find('**/scroll')),
            itemFrame_relief = None,
            itemFrame_geom_scale = (0.35, 0.25, 0.35),
            itemFrame_geom_color = (1, 1, 1, 0.8),
            items = [],
            numItemsVisible = self.VISIBLE_MSG_COUNT,
            forceHeight = 0.1)
        self.title = DirectLabel(parent=self.chatlog, relief=None, text=OTPLocalizer.GlobalChatLogName, text_font=ToontownGlobals.getSignFont(), text_fg=(0.3, 0.3, 0.7, 1), text_scale=0.05, text_pos=(0, 0.125))
        self.setBin('gui-popup', 100)

    def cleanup(self):
        self.title.destroy()
        del self.title
        self.chatlog.destroy()
        del self.chatlog

    def show(self):
        DirectFrame.show(self)
        self.accept('wheel_up-up', self.scroll, [-1])
        self.accept('wheel_down-up', self.scroll, [1])

    def hide(self):
        DirectFrame.hide(self)
        self.ignore('wheel_up-up')
        self.ignore('wheel_down-up')

    def log(self, name, msg, color='toonblue'):
        msg = DirectLabel(relief=None, text='\x01' + color + '\x01%s:\x02 %s' % (name, msg), text_scale=0.035, text_pos=(0, 0.05), text_wordwrap=22)
        self.chatlog.addItem(msg)
        self.chatlog.scrollTo(len(self.chatlog['items']) - 1)

    def scroll(self, value):
        if hasattr(self, 'chatlog'):
            index = self.chatlog.getSelectedIndex()
            self.chatlog.scrollTo(index + value)