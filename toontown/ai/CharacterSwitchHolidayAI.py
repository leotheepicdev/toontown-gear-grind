from . HolidayBaseAI import HolidayBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify

from toontown.toonbase import TTLocalizer, ToontownGlobals

# Normal character imports
from toontown.classicchars.DistributedMickeyAI import DistributedMickeyAI
from toontown.classicchars.DistributedDaisyAI import DistributedDaisyAI
from toontown.classicchars.DistributedMinnieAI import DistributedMinnieAI
from toontown.classicchars.DistributedPlutoAI import DistributedPlutoAI
from toontown.classicchars.DistributedDonaldAI import DistributedDonaldAI
from toontown.classicchars.DistributedGoofySpeedwayAI import DistributedGoofySpeedwayAI
from toontown.classicchars.DistributedChipAI import DistributedChipAI
from toontown.classicchars.DistributedDaleAI import DistributedDaleAI

# Halloween character imports
from toontown.classicchars.DistributedVampireMickeyAI import DistributedVampireMickeyAI
from toontown.classicchars.DistributedSockHopDaisyAI import DistributedSockHopDaisyAI
from toontown.classicchars.DistributedWitchMinnieAI import DistributedWitchMinnieAI
from toontown.classicchars.DistributedWesternPlutoAI import DistributedWesternPlutoAI
from toontown.classicchars.DistributedFrankenDonaldAI import DistributedFrankenDonaldAI
from toontown.classicchars.DistributedSuperGoofyAI import DistributedSuperGoofyAI
from toontown.classicchars.DistributedPoliceChipAI import DistributedPoliceChipAI
from toontown.classicchars.DistributedJailbirdDaleAI import DistributedJailbirdDaleAI

switchAprilFools = {
    TTLocalizer.Mickey: DistributedDaisyAI,
    TTLocalizer.Daisy : DistributedMickeyAI,
    TTLocalizer.Minnie: DistributedPlutoAI,
    TTLocalizer.Pluto : DistributedMinnieAI,
    TTLocalizer.Donald : DistributedGoofySpeedwayAI,
    TTLocalizer.Goofy : DistributedDonaldAI,
}

switchHalloween = {
    TTLocalizer.Mickey: DistributedVampireMickeyAI,
    TTLocalizer.Daisy : DistributedSockHopDaisyAI,
    TTLocalizer.Minnie: DistributedWitchMinnieAI,
    TTLocalizer.Pluto : DistributedWesternPlutoAI,
    TTLocalizer.Donald : DistributedFrankenDonaldAI,
    TTLocalizer.Goofy : DistributedSuperGoofyAI,
}

switchRollback = {
    TTLocalizer.Mickey: DistributedMickeyAI,
    TTLocalizer.Daisy : DistributedDaisyAI,
    TTLocalizer.Minnie: DistributedMinnieAI,
    TTLocalizer.Pluto : DistributedPlutoAI,
    TTLocalizer.Donald : DistributedDonaldAI,
    TTLocalizer.Goofy : DistributedGoofySpeedwayAI,
}

class CharacterSwitchHolidayAI(HolidayBaseAI):
    notify = directNotify.newCategory('CharacterSwitchHolidayAI')

    def __init__(self, air, holidayId):
        HolidayBaseAI.__init__(self, air, holidayId)

    def start(self):
        HolidayBaseAI.start(self)
        # Let the classic characters know that
        # they need to transition soon.
        for hood in self.air.hoods:
            if hasattr(hood, 'classicChar'):
                hood.classicChar.transitionCostume()
            elif hasattr(hood, 'classicChars') and self.holidayId in (ToontownGlobals.HALLOWEEN_COSTUMES, ToontownGlobals.SPOOKY_COSTUMES):
                # Special case for Chip 'n Dale.
                self.switchChipDale(hood)

    def stop(self):
        HolidayBaseAI.stop(self)
        for hood in self.air.hoods:
            if hasattr(hood, 'classicChar'):
                self.rollbackCharacter(hood, hood.classicChar)
            elif hasattr(hood, 'classicChars') and self.holidayId in (ToontownGlobals.HALLOWEEN_COSTUMES, ToontownGlobals.SPOOKY_COSTUMES):
                # Special case for Chip 'n Dale.
                self.switchChipDale(hood, True)

    def triggerSwitch(self, curWalkNode, char):
        # Called by a classic character when the transition process has started.
        if not self.getRunningState():
            # Don't do anything if the holiday's not even running.
            self.notify.warning('triggerSwitch called by {} even though the holiday is not running!'.format(char))
            return

        # Get the character's Zone ID.
        zoneId = char.zoneId
        # Get the classic character that we want to switch with.
        if self.holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            # April Fools costumes.
            switchCChar = switchAprilFools.get(char.getName())
        elif self.holidayId in (ToontownGlobals.HALLOWEEN_COSTUMES, ToontownGlobals.SPOOKY_COSTUMES):
            # Halloween costumes.
            switchCChar = switchHalloween.get(char.getName())
        else:
            self.notify.warning('Unknown holiday: {}'.format(self.holidayId))

        if not switchCChar:
            self.notify.warning('Don\'t know who to switch for {}!'.format(char))
            return

        # Loop through the AIR's hoods untill we get the right one.
        for hood in self.air.hoods:
            if hood.zoneId == zoneId:
                break

        # Fade into obscurity, like Oswald the Lucky Rabbit.
        char.fadeAway()
        # Delete the character from existance. Er-, I mean obscurity.
        char.requestDelete()
        # Let the hood know.
        hood.removeDistObj(char)

        # Load up our new replacement character to take it's place.
        hood.classicChar = switchCChar(self.air)
        # Now we generate...
        hood.classicChar.generateWithRequired(hood.zoneId)
        # Place the character to the node that the previous character was in.
        hood.classicChar.walk.setCurNode(curWalkNode)
        # Start...
        hood.classicChar.start()
        # And lastly, let the hood know its existance.
        hood.addDistObj(hood.classicChar)

    def rollbackCharacter(self, hood, char):
        # Rollback to the default character since the holiday has ended.
        if char.getName() == TTLocalizer.DonaldDock:
            return

        if self.holidayId == ToontownGlobals.APRIL_FOOLS_COSTUMES:
            if not char.diffPath:
                # If the character's not using a different path, then its safe to assume that this character's
                # haven't changed yet, so let's not do anything.
                char.transitionToCostume = 0
                return

            rollbackChar = switchAprilFools.get(char.getName())
        else:
            rollbackChar = switchRollback.get(char.getName())

        if not rollbackChar:
            self.notify.warning('Don\'t know who to rollback for {}!'.format(char))
            return

        # Fade into obscurity, like Oswald the Lucky Rabbit.
        char.fadeAway()
        # Delete the character from existance. Er-, I mean obscurity.
        char.requestDelete()
        # Let the hood know.
        hood.removeDistObj(char)

        # Load up the original character to take it's place.
        hood.classicChar = rollbackChar(self.air)
        # Now we generate...
        hood.classicChar.generateWithRequired(hood.zoneId)
        # Start...
        hood.classicChar.start()
        # And lastly, let the hood know its existance.
        hood.addDistObj(hood.classicChar)

    def switchChipDale(self, hood, rollback = False):
        # Special function for Chip 'n Dale for Halloween.
        for char in hood.classicChars:
            char.fadeAway()
            char.requestDelete()
            hood.removeDistObj(char)

        hood.classicChars = []

        # Generate Chip
        if not rollback:
            chip = DistributedPoliceChipAI(self.air)
        else:
            chip = DistributedChipAI(self.air)
        chip.generateWithRequired(hood.zoneId)
        chip.start()
        hood.addDistObj(chip)
        hood.classicChars.append(chip)

        # Generate Dale
        if not rollback:
            dale = DistributedJailbirdDaleAI(self.air, chip.doId)
        else:
            dale = DistributedDaleAI(self.air, chip.doId)
        dale.generateWithRequired(hood.zoneId)
        dale.start()
        hood.addDistObj(dale)
        hood.classicChars.append(dale)
        chip.setDaleId(dale.doId)
