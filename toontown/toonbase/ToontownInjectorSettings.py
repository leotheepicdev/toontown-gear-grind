import json, os

class ToontownInjectorSettings:

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)

        return {}

    def write(self, store):
        with open(self.filename, 'w') as file:
            json.dump(store, file, sort_keys=True, indent=2, separators=(',', ': '))
