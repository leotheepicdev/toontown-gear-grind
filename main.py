import os, sys, builtins

currentDirectory = os.getcwd() + 'sdcard/game'
builtins.currentDirectory = currentDirectory

sys.path.append(currentDirectory + '/')
sys.path.append(currentDirectory + '/resources')

from toontown.toonbase import ToontownStart