from panda3d.core import loadPrcFile, loadPrcFileData
from panda3d.core import ConfigVariableInt, ConfigVariableString

class game:
    name = 'uberDog'
    process = 'server'

import builtins, os
builtins.game = game

from otp.ai.AIBaseGlobal import taskMgr

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base-channel', help='The base channel that the server may use.')
parser.add_argument('--max-channels', help='The number of channels the server may use.')
parser.add_argument('--stateserver', help='The control channel of this UberDOGs designated State Server.')
parser.add_argument('--astron-ip', help='The IP address of the Astron Message Director to connect to.')
parser.add_argument('--eventlogger-ip', help='The IP address of the Astron Event Logger to log to.')
parser.add_argument('config', nargs='*', default = ['config/general.prc', 'config/server.prc'], help='PRC file(s) to load.')
args = parser.parse_args()

for prc in args.config:
    loadPrcFile(prc)
    
if os.path.isfile('config/production.prc'):
    loadPrcFile('config/production.prc')

localconfig = ''

if args.base_channel:
    localconfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels:
    localconfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver:
    localconfig += 'air-stateserver %s\n' % args.stateserver
if args.astron_ip:
    localconfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip: 
    localconfig += 'eventlog-host %s\n' % args.eventlogger_ip

loadPrcFileData('Command-line', localconfig)

from toontown.uberdog.UDRepository import UDRepository

simbase.air = UDRepository(ConfigVariableInt('air-base-channel', 1000000).value, ConfigVariableInt('air-stateserver', 4002).value)

host = ConfigVariableString('air-connect', '127.0.0.1').value
port = 7101

if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)

simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    avId = simbase.air.getAvatarIdFromSender()
    accId = simbase.air.getAccountIdFromSender()

    from direct.showbase import PythonUtil

    traceback = PythonUtil.describeException()

    simbase.air.writeServerEvent('uberdog-exception', avId, accId, traceback)

    raise