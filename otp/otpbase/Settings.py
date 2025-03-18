import json, os, collections, sys

class Settings(collections.MutableMapping):
    if sys.platform == 'android':
        SETTINGS_FILENAME = currentDirectory + '/user/settings.json'
    else:
        SETTINGS_FILENAME = 'user/settings.json'

    GL = 'pandagl'
    DX7 = 'pandadx7'
    DX8 = 'pandadx8'
    DX9 = 'pandadx9'

    # TODO: make the json remove any setting keys that are not in the default settings

    def __init__(self):
        self.settings = {}

        self.readSettings()

    def getDefaultSettings(self):
        return {'windowedMode': True,
        'music': True,
        'sfx': True,
        'toonChatSounds': True,
        'musicVolume': 1,
        'sfxVolume': 1,
        'resolutionDimensions': [800, 600],
        'acceptingNewFriends': True,
        'acceptingNonFriendWhispers': True,
        'embeddedMode': False,
        'frameRateMeter': False,
        'wantWhitelist': True,
        'automaticErrorReporting': True,
        'retroAspectRatio': False,
        'oldNametagColors': False,
        'wantDisclaimer': True,
        'streamerSupport': True,
        'wantDirectX': False,
        'wantDaylight': True}

    def doSavedSettingsExist(self):
        return os.path.exists(self.SETTINGS_FILENAME)

    def readSettings(self):
        if not self.doSavedSettingsExist():
            self.writeSettings(useDefaultSettings=1)
        else:
            self.settings = json.load(open(self.SETTINGS_FILENAME, 'r'))

    def writeSettings(self, useDefaultSettings=False):
        with open(self.SETTINGS_FILENAME, 'w') as file:
            if useDefaultSettings:
                settings = self.getDefaultSettings()
            else:
                settings = self.settings
            json.dump(settings, file, sort_keys=1, indent=4, separators=[',', ': '])
            self.settings = settings

    def setDisplayDriver(self, api):
        # TODO
        pass

    def __setitem__(self, key, value):
        self.settings[key] = value
        self.writeSettings()

    def __delitem__(self, key):
        try:
            del self.settings[key]
            self.writeSettings()
        except:
            pass

    def __getitem__(self, key):
        if key not in self.settings:
            value = self.getDefaultSettings()[key]
            self.settings[key] = value
        return self.settings[key]

    def __iter__(self):
        return iter(self.settings)

    def __len__(self):
        return len(self.settings)