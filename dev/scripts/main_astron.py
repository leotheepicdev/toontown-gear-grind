import os, sys

os.chdir('../../lib/astron')

linux = ['linux', 'linux2']

if sys.platform in linux:
    os.system('./astrond-linux --loglevel info config/astrond.yml')
elif sys.platform == 'win32':
    os.system('astrond.exe --loglevel info --pretty config/astrond.yml')
elif sys.platform == 'darwin':
    os.system('./astrond-darwin -loglevel info config/astrond.yml')