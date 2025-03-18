from . import Playground

class RRHPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def enter(self, requestStatus):
        self.loader.hood.setFog()
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)
        self.loader.hood.setNoFog()
