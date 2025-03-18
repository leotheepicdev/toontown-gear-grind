from panda3d.core import NodePath, loadPrcFile, loadPrcFileData
import sys, os

if sys.platform == 'android':
    os.environ['TOONTOWN_PLAYTOKEN'] = 'dev'
    os.environ['TOONTOWN_GAMESERVER'] = 'game.geargrind.tech:6667'

for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]

if __debug__:
    if sys.platform != 'android':
        loadPrcFile('config/general.prc')
    else:
        loadPrcFile('config/android.prc')

if not os.path.exists('user/'):
    os.makedirs('user/')

from otp.otpbase.Settings import Settings

import builtins
builtins.Settings = Settings()

if builtins.Settings['wantDirectX']:
    loadPrcFileData('', 'load-display pandadx9')

class game:
    name = 'toontown'
    process = 'client'

builtins.game = game()
import time
import os
import sys
import random
import builtins
try:
    launcher
except:
    from toontown.launcher.ToontownDummyLauncher import ToontownDummyLauncher
    launcher = ToontownDummyLauncher()
    builtins.launcher = launcher

if __debug__ and '--debug-injector' in sys.argv:
    try:
        import wx
    except:
        print('Failed to start injector - wx module missing!')
    else:
        try:
            import psutil
        except:
            print('Failed to start injector - psutil module missing!')
        else:
            from toontown.toonbase.ToontownInjector import ToontownInjector
            print('Starting injector...')
            builtins.injector = ToontownInjector()

from panda3d.core import VirtualFileSystem, Multifile, Filename

# Content packs system.
vfs = VirtualFileSystem.getGlobalPtr()

if sys.platform == 'android':
    CONTENT_PACK_PATH = currentDirectory + '/resources/contentpacks'
else:
    CONTENT_PACK_PATH = 'resources/contentpacks'

# Ensure the directory exists:
if not os.path.exists(CONTENT_PACK_PATH):
    os.makedirs(CONTENT_PACK_PATH)

for root, _, filenames in os.walk(CONTENT_PACK_PATH):
    for filename in filenames:
        if not filename.endswith('.mf'):
            continue

        filename = os.path.join(root, filename).replace('\\', '/')

        mf = Multifile()
        mf.openReadWrite(Filename(filename))

        if not __debug__:
            vfs.mount(mf, Filename('resources/'), 0)
        else:
            vfs.mount(mf, Filename('/'), 0)

launcher.setRegistry('EXIT_PAGE', 'normal')

print('ToontownStart: Starting the game.')
from panda3d.core import *
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
from direct.gui import DirectGuiGlobals
builtins.FADE_SORT_INDEX = DirectGuiGlobals.FADE_SORT_INDEX
builtins.NO_FADE_SORT_INDEX = DirectGuiGlobals.NO_FADE_SORT_INDEX
print('ToontownStart: setting default font')
from . import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from . import ToonBase
ToonBase.ToonBase()

if builtins.Settings['retroAspectRatio']:
    base.setAspectRatio(1.33)

if base.win == None:
    print('Unable to open window; aborting.')
    sys.exit()

from toontown.login.ToontownLoginScreen import ToontownLoginScreen
loginScreen = ToontownLoginScreen()
loginScreen.fsm.request('intro')

autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun and launcher.isDummy() and (not Thread.isTrueThreads() or __name__ in ['__main__', 'toontown.toonbase.ToontownStart']):
    try:
        base.run()
    except SystemExit:
        raise
    except:
        if __debug__:
            from direct.showbase import PythonUtil
            print(PythonUtil.describeException())
        else:
            import traceback
            traceback.print_exc()
        raise
