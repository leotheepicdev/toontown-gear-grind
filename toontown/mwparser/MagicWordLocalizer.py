CharacterNames = [
    'Mickey',
    'Goofy',
    'Minnie',
    'Donald',
    'Pluto',
    'Chip',
    'Dale'
]

MagicianName = 'Magician {0}'

ErrorNoTarget = 'Unable to find target!'
ErrorTargetSelf = 'You can only target yourself!'
ErrorTargetOther = 'You can only target others!'
ErrorWordNotFound = 'This Magic Word does not exist!'
ErrorNotEnoughArgs = 'Not enough arguments!' # TODO: show arg types
ErrorWrongArgs = 'Arguments are invalid!' # TODO: show arg types
ErrorAccessTooLow = 'Your access level is not high enough to perform this Magic Word.'
ErrorTargetHigherAccess = 'This Toon has a higher access level than you!'
WordClose = 'This Magic Word does not exist! Did you mean {}?'

ResponseCode2String = {
 0: ErrorNoTarget,
 1: ErrorTargetSelf,
 2: ErrorTargetOther,
 3: ErrorNotEnoughArgs,
 4: ErrorWrongArgs,
 5: ErrorWordNotFound,
 6: ErrorAccessTooLow,
 7: ErrorTargetHigherAccess,
 8: WordClose
 }