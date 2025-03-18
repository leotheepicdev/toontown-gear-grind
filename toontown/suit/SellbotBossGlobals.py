from panda3d.core import Point3, Vec3
from toontown.coghq import DistributedHealBarrel
from toontown.coghq import DistributedGagBarrel
BarrelDefs = {8000: {'type': DistributedHealBarrel.DistributedHealBarrel,
        'pos': Point3(15, 23, 0),
        'hpr': Vec3(-45, 0, 0),
        'rewardPerGrab': 50,
        'rewardPerGrabMax': 0},
 8001: {'type': DistributedGagBarrel.DistributedGagBarrel,
        'pos': Point3(15, -23, 0),
        'hpr': Vec3(-135, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 3,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0},
 8002: {'type': DistributedGagBarrel.DistributedGagBarrel,
        'pos': Point3(21, 20, 0),
        'hpr': Vec3(-45, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 4,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0},
 8003: {'type': DistributedGagBarrel.DistributedGagBarrel,
        'pos': Point3(21, -20, 0),
        'hpr': Vec3(-135, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 5,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0}}

def setBarrelAttr(barrel, entId):
    for defAttr, defValue in BarrelDefs[entId].items():
        setattr(barrel, defAttr, defValue)


BarrelsStartPos = (0, -36, -8)
BarrelsFinalPos = (0, -36, 0)
