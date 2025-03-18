from panda3d.core import PStatClient, Thread

from direct.directnotify import DirectNotifyGlobal
from direct.stdpy import threading

from toontown.toonbase import ToontownInjectorGlobals
from toontown.toonbase.ToontownInjectorSettings import ToontownInjectorSettings

import atexit, subprocess, psutil, sys, os, wx

DEFAULT_TEXT = ''
DEFAULT_IMPORTS = ''

class CustomDialog(wx.Dialog):

    def __init__(self, parent, caption, title, inputMethod):
        wx.Dialog.__init__(self, parent, -1, title)

        self.text = wx.StaticText(self, -1, caption)
        self.input = inputMethod(self)
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.text, 0, wx.ALL, 5)
        self.sizer.Add(self.input, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.buttons, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(self.sizer)
        self.input.SetFocus()
        self.Centre()

class ListDialog(CustomDialog):

    def __init__(self, parent, caption, title, choices):
        CustomDialog.__init__(self, parent, caption, title, lambda self: wx.ListBox(self, choices=sorted(choices)))

class InputDialog(CustomDialog):

    def __init__(self, parent, caption, title):
        CustomDialog.__init__(self, parent, caption, title, lambda self: wx.TextCtrl(self))

    def getInput(self):
        return self.input.GetValue()

class ToontownInjector:
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownInjector')

    def __init__(self):
        self.snippets = ToontownInjectorSettings('snippets.json')
        self.app = wx.App(redirect=False)
        self.frame = wx.Frame(None, title=ToontownInjectorGlobals.InjectorTitle, size=(635, 325), style=wx.SYSTEM_MENU | wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.RESIZE_BORDER)
        self.panel = wx.Panel(self.frame)

        self.buttonPanel = wx.Panel(self.panel)
        self.checkboxPanel = wx.Panel(self.panel)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.checkboxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.injectBox = wx.TextCtrl(parent=self.panel, style=wx.TE_MULTILINE | wx.TE_RICH2)
        self.injectButton = wx.Button(parent=self.buttonPanel, size=(100, 50), label=ToontownInjectorGlobals.InjectorInject)
        self.injectAiButton = wx.Button(parent=self.buttonPanel, size=(100, 50), label=ToontownInjectorGlobals.InjectorInjectAI)
        self.saveButton = wx.Button(parent=self.buttonPanel, size=(100, 50), label=ToontownInjectorGlobals.InjectorSave)
        self.loadButton = wx.Button(parent=self.buttonPanel, size=(100, 50), label=ToontownInjectorGlobals.InjectorLoad)
        self.removeButton = wx.Button(parent=self.buttonPanel, size=(100, 50), label=ToontownInjectorGlobals.InjectorRemove)
        self.pstatsBox = wx.CheckBox(parent=self.checkboxPanel, label=ToontownInjectorGlobals.InjectorPStats)

        self.injectBox.SetLabel(DEFAULT_TEXT)
        self.injectBox.Bind(wx.EVT_KEY_DOWN, self.__keyDown)
        self.injectButton.Bind(wx.EVT_BUTTON, self.__inject)
        self.injectAiButton.Bind(wx.EVT_BUTTON, lambda event: self.__inject(event, True))
        self.saveButton.Bind(wx.EVT_BUTTON, self.__save)
        self.loadButton.Bind(wx.EVT_BUTTON, self.__load)
        self.removeButton.Bind(wx.EVT_BUTTON, self.__remove)
        self.pstatsBox.Bind(wx.EVT_CHECKBOX, self.__pstats)

        self.addToSizer(self.buttonSizer, self.injectButton, self.injectAiButton, self.saveButton, self.loadButton, self.removeButton)
        self.addToSizer(self.checkboxSizer, self.pstatsBox)

        self.sizer.Add(self.checkboxPanel, 0, wx.ALIGN_CENTER)
        self.sizer.Add(self.injectBox, 1, wx.EXPAND)
        self.sizer.Add(self.buttonPanel, 0, wx.ALIGN_CENTER)

        self.buttonPanel.SetSizer(self.buttonSizer)
        self.panel.SetSizer(self.sizer)
        self.frame.SetMinSize((635, 325))
        self.frame.Show()

        atexit.register(self.__pstatCleanup)
        threading.Thread(target=self.app.MainLoop).start()

    def addToSizer(self, sizer, *args):
        for i, arg in enumerate(args):
            if i:
                sizer.AddSpacer(30)

            sizer.Add(arg)

    def info(self, parent, message, caption, icon=wx.ICON_INFORMATION, buttons=wx.OK):
        return wx.MessageDialog(parent, message, caption, buttons | icon).ShowModal() == wx.ID_YES

    def chooseSnippet(self, caption):
        dialog = ListDialog(self.frame, caption, ToontownInjectorGlobals.InjectorTitle, self.snippets.keys())

        if dialog.ShowModal() == wx.ID_OK:
            return dialog.input.GetStringSelection()

    def reloadSnippets(self):
        self.snippets.read()

    def saveSnippet(self, name, content):
        self.snippets[name] = content

    def getPandaDirectory(self):
        return os.sep.join(sys.path[1].split(os.sep)[:-2])

    def getPStatsPath(self):
        return os.path.join(self.getPandaDirectory(), 'bin', 'pstats')

    def getProcesses(self, name):
        return [process for process in psutil.process_iter() if process.name().startswith(name)]

    def __keyDown(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.injectBox.WriteText(' ' * 4)
        else:
            event.Skip()

    def __inject(self, event, ai=False):
        injection = DEFAULT_IMPORTS + self.injectBox.GetValue()

        if ai:
            if hasattr(base, 'cr') and base.cr.timeManager:
                base.cr.timeManager.inject(injection)
            else:
                self.notify.warning(ToontownInjectorGlobals.InjectorAIUnavailable)
        else:
            exec(injection, globals())

    def __save(self, event):
        dialog = InputDialog(self.frame, ToontownInjectorGlobals.InjectorSaveQuestion, ToontownInjectorGlobals.InjectorTitle)

        if dialog.ShowModal() != wx.ID_OK:
            return

        input = dialog.getInput()
        snippet = self.injectBox.GetValue()

        if not input or not snippet:
            self.info(dialog, ToontownInjectorGlobals.InjectorNotSaved, ToontownInjectorGlobals.InjectorOops, wx.ICON_WARNING)
            return
        elif input in self.snippets and not self.info(dialog, ToontownInjectorGlobals.InjectorSnippetExists, ToontownInjectorGlobals.InjectorOops, wx.ICON_WARNING, wx.YES_NO):
            return

        self.snippets[input] = snippet
        self.info(dialog, ToontownInjectorGlobals.InjectorSaved % input, ToontownInjectorGlobals.InjectorOhYea)

    def __load(self, event):
        input = self.chooseSnippet(ToontownInjectorGlobals.InjectorLoadQuestion)

        if not input or (self.injectBox.GetValue() and not self.info(self.frame, ToontownInjectorGlobals.InjectorOverwriteWarning, ToontownInjectorGlobals.InjectorOops, wx.ICON_WARNING, wx.YES_NO)):
            return

        self.injectBox.SetValue(self.snippets[input])
        self.info(self.frame, ToontownInjectorGlobals.InjectorLoaded % input, ToontownInjectorGlobals.InjectorOhYea)

    def __remove(self, event):
        input = self.chooseSnippet(ToontownInjectorGlobals.InjectorRemoveQuestion)

        if not input or not self.info(self.frame, ToontownInjectorGlobals.InjectorRemoveWarning % input, ToontownInjectorGlobals.InjectorOops, wx.ICON_WARNING, wx.YES_NO):
            return

        del self.snippets[input]
        self.info(self.frame, ToontownInjectorGlobals.InjectorRemoved % input, ToontownInjectorGlobals.InjectorOhYea)

    def __pstats(self, event):
        box = event.GetEventObject()
        box.Disable()

        if box.GetValue():
            if not self.getProcesses('pstats'):
                subprocess.Popen([self.getPStatsPath()])

            PStatClient.connect()
        else:
            PStatClient.disconnect()

            for process in self.getProcesses('pstats'):
                process.kill()

        taskMgr.doMethodLater(1, lambda task: box.Enable(), 'enableElement-%d' % id(box))

    def __pstatCleanup(self):
        if self.pstatsBox.GetValue():
            for process in self.getProcesses('pstats'):
                process.kill()
