from direct.interval.IntervalGlobal import *
from direct.showbase import Audio3DManager
from . import BasicEntities
import random

class AmbientSound(BasicEntities.NodePathEntity):

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.initSound()

    def destroy(self):
        self.destroySound()
        BasicEntities.NodePathEntity.destroy(self)

    def initSound(self):
        if not self.enabled:
            return
        if self.soundPath == '':
            return
        self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)
        self.audioManager.setDropOffFactor(0.05)
        self.sound = self.audioManager.loadSfx(self.soundPath)
        if self.sound is None:
            return
        self.audioManager.attachSoundToObject(self.sound, self)
        self.sound.setLoop(True)
        self.sound.setVolume(self.volume)
        self.sound.play()

    def destroySound(self):
        if hasattr(self, 'soundIval'):
            self.soundIval.pause()
            del self.soundIval
        if hasattr(self, 'sound'):
            self.audioManager.detachSound(self.sound)
            del self.sound
        self.audioManager.disable()

    if __dev__:

        def attribChanged(self, *args):
            self.destroySound()
            self.initSound()
