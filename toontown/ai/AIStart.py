from panda3d.core import NodePath, loadPrcFile, loadPrcFileData
from panda3d.core import ConfigVariableInt, ConfigVariableString

for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]

class game:
    name = 'toontown'
    process = 'server'

import builtins
builtins.game = game

from otp.ai.AIBaseGlobal import taskMgr

import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('--base-channel', help='The base channel that the server may use.')
parser.add_argument('--max-channels', help='The number of channels the server may use.')
parser.add_argument('--stateserver', help="The control channel of this AI's designated State Server.")
parser.add_argument('--district-name', help="What this AI Server's district will be named.")
parser.add_argument('--want-random-invasions', help="Do we want random cog invasions to occur?")
parser.add_argument('--want-invasions-only', help="Do we want invasions to occur all the time?")
parser.add_argument('--astron-ip', help= " The IP address of the Astron Message Director to connect to.")
parser.add_argument('--eventlogger-ip', help = "The IP address of the Astron Event Logger to log to.")
parser.add_argument('config', nargs = '*', default = ['config/general.prc', 'config/server.prc'], help = "PRC file(s) to load.")
args = parser.parse_args()

for prc in args.config:
    loadPrcFile(prc)

localconfig = ''

if 'PYCHARM_HOSTED' in os.environ:
    isPyCharm = True
else:
    isPyCharm = False

if args.base_channel:
    localconfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels:
    localconfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver:
    localconfig += 'air-stateserver %s\n' % args.stateserver
if args.district_name:
    localconfig += 'district-name %s\n' % args.district_name
if isPyCharm or int(args.want_random_invasions) == 1:
    wantRandomInvasions = True
else:
    wantRandomInvasions = False
if isPyCharm or int(args.want_invasions_only) == 1:
    isInvasionsOnly = True
else:
    isInvasionsOnly = False
if args.astron_ip:
    localconfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip:
    localconfig += 'eventlog-host %s\n' % args.eventlogger_ip
    
loadPrcFileData('Command-line', localconfig)

from toontown.ai.AIRepository import AIRepository
simbase.air = AIRepository(ConfigVariableInt('air-base-channel', 401000000).value, ConfigVariableInt('air-stateserver', 4002).value, ConfigVariableString('district-name', 'Sillyville').value, wantRandomInvasions, isInvasionsOnly)

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

    simbase.air.writeServerEvent('ai-exception', avId = avId, accId = accId, exception = traceback)

    raise