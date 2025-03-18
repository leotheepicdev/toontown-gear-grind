window-title Toontown: Gear Grind

screenshot-extension png

audio-library-name p3openal_audio

model-path ./resources/
default-model-extension .bam

texture-anisotropic-degree 16

default-server-constants true
game-server 127.0.0.1:6667
server-version test

dc-file config/dclass/geargrind.dc

want-do-live-updates true

whitelist-chat-enabled true

want-magic-words TRUE

active-holidays 60, 61, 62, 63, 64, 65, 66

want-cogdominiums true
want-all-minigames true

#cogdo-game crane
cogdo-ratio 0.25

want-dev false

want-code-redemption true
want-parties true
want-game-tables false
want-chinese true
want-checkers true
want-findfour true
want-gardening true
want-instant-delivery true
server-data-folder backups/
building-data-backup-folder backups/buildings
dailycatch-data-backup-folder backups/dailycatch
props-buff-battles true
text-minfilter linear_mipmap_linear
want-system-responses false
want-discord-presence false
discord-client-id 0
gc-save-all 0

# Gameserver (SSL/TLS):
ssl-mod dev
ssl-certs-folder ./lib/astron/certs/dev/

# Performance:
hardware-animated-vertices #t
sync-video #f
smooth-lag 0.2
smooth-prediction-lag 0.0
framebuffer-multisample 0
framebuffer-stencil 0
support-stencil 0
multisamples 0
garbage-collect-states-rate 0.5

# Debug
assert-abort 1
