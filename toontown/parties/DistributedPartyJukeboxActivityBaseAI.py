from direct.directnotify import DirectNotifyGlobal

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI


class DistributedPartyJukeboxActivityBaseAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyJukeboxActivityBaseAI')

    def __init__(self, air, parent, activity):
        DistributedPartyActivityAI.__init__(self, air, parent, activity)
        self.music = PartyGlobals.PhaseToMusicData
        self.currentToon = 0
        self.owners = []
        self.queue = []
        self.paused = False
        self.playing = False

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.accept('fireworks-started-%s' % self.getPartyDoId(), self.handleFireworksStarted)
        self.accept('fireworks-finished-%s' % self.getPartyDoId(), self.handleFireworksFinished)

    def delete(self):
        taskMgr.remove(self.uniqueName('play-song'))
        taskMgr.remove(self.uniqueName('remove-toon'))
        self.ignoreAll()
        DistributedPartyActivityAI.delete(self)

    def setNextSong(self, song):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        phase = self.music.get(song[0])
        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to set song without using the jukebox!')
            return

        if not phase:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon supplied invalid phase for song!')
            return

        if song[1] not in phase:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon supplied invalid song name!')
            return

        if avId in self.owners:
            self.queue[self.owners.index(avId)] = song
        else:
            self.queue.append(song)
            self.owners.append(avId)

        for avId in self.toonsPlaying:
            self.sendUpdateToAvatarId(avId, 'setSongInQueue', [song])

        if self.paused:
            return

        if not self.playing:
            self.d_setSongPlaying([0, ''], 0)
            taskMgr.remove(self.uniqueName('play-song'))
            self.playSong()

    def d_setSongPlaying(self, details, owner):
        self.sendUpdate('setSongPlaying', [details, owner])

    def queuedSongsRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.owners:
            index = self.owners.index(avId)
        else:
            index = -1

        self.sendUpdateToAvatarId(avId, 'queuedSongsResponse', [self.queue, index])

    def moveHostSongToTopRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.currentToon:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Toon tried to set song without using the jukebox!')
            return

        party = self.air.doId2do.get(self.parent)
        if not party:
            return

        hostId = party.hostId
        if avId != hostId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to move the host\'s song to the top!')
            return

        if hostId not in self.owners:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Host tried to move non-existent song to the top of the queue!')
            return

        index = self.owners.index(hostId)
        self.owners.remove(hostId)
        song = self.queue.pop(index)
        self.owners.insert(0, hostId)
        self.queue.insert(0, song)
        for avId in self.toonsPlaying:
            self.sendUpdateToAvatarId(avId, 'moveHostSongToTop', [])

    def playSong(self, task = None):
        if self.paused:
            return

        if not self.queue:
            self.d_setSongPlaying([13, 'party_original_theme.ogg'], 0)
            self.playing = False
            taskMgr.doMethodLater(self.music[13]['party_original_theme.ogg'][1], self.pauseSong,
                                  self.uniqueName('play-song'))
            if task:
                return task.done
            else:
                return

        self.playing = True
        details = self.queue.pop(0)
        owner = self.owners.pop(0)
        songInfo = self.music[details[0]][details[1]]
        self.d_setSongPlaying(details, owner)
        taskMgr.doMethodLater(songInfo[1] * PartyGlobals.getMusicRepeatTimes(songInfo[1]), self.pauseSong,
                              self.uniqueName('play-song'))

        if task:
            return task.done

    def pauseSong(self, task):
        self.d_setSongPlaying([0, ''], 0)
        taskMgr.doMethodLater(PartyGlobals.MUSIC_GAP, self.playSong, self.uniqueName('play-song'))
        return task.done

    def toonJoinRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if self.currentToon:
            self.sendUpdateToAvatarId(avId, 'joinRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if avId in self.toonsPlaying:
            return

        self.currentToon = avId
        taskMgr.doMethodLater(PartyGlobals.JUKEBOX_TIMEOUT, self.removeToon, self.uniqueName('remove-toon'))
        self.toonsPlaying.append(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def toonExitRequest(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.currentToon:
            return

        if avId not in self.toonsPlaying:
            return

        taskMgr.remove(self.uniqueName('remove-toon'))
        self.currentToon = 0
        self.toonsPlaying.remove(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def toonExitDemand(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        if avId != self.currentToon:
            return

        if avId not in self.toonsPlaying:
            return

        taskMgr.remove(self.uniqueName('remove-toon'))
        self.currentToon = 0
        self.toonsPlaying.remove(avId)
        self.b_setToonsPlaying(self.toonsPlaying)

    def removeToon(self, task):
        if not self.currentToon:
            return

        if self.currentToon not in self.toonsPlaying:
            return

        self.toonsPlaying.remove(self.currentToon)
        self.b_setToonsPlaying(self.toonsPlaying)
        self.currentToon = 0
        return task.done

    def handleFireworksStarted(self):
        taskMgr.remove(self.uniqueName('play-song'))
        self.paused = True
        self.d_setSongPlaying([0, ''], 0)

    def handleFireworksFinished(self):
        self.paused = False
        self.playSong()
