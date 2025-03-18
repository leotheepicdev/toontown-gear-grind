window-title Toontown: Gear Grind

audio-library-name p3openal_audio

load-display pandagl

screenshot-extension png

model-path /
model-cache-models #f
model-cache-textures #f
vfs-mount resources/phase_3.mf /
vfs-mount resources/phase_3.5.mf /
vfs-mount resources/phase_4.mf /
vfs-mount resources/phase_5.mf /
vfs-mount resources/phase_5.5.mf /
vfs-mount resources/phase_6.mf /
vfs-mount resources/phase_7.mf /
vfs-mount resources/phase_8.mf /
vfs-mount resources/phase_9.mf /
vfs-mount resources/phase_10.mf /
vfs-mount resources/phase_11.mf /
vfs-mount resources/phase_12.mf /
vfs-mount resources/phase_13.mf /
vfs-mount resources/phase_14.mf /
default-model-extension .bam

texture-anisotropic-degree 16

default-server-constants true
game-server game.geargrind.tech:6667
server-version test

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
want-game-tables true
want-chinese true
want-checkers true
want-findfour true
want-gardening true
want-instant-delivery true
server-data-folder backups/
building-data-backup-folder backups/buildings
props-buff-battles true
text-minfilter linear_mipmap_linear
want-system-responses false
want-discord-presence true
discord-client-id 518599273030352896
gc-save-all 0

# Gameserver (SSL/TLS):
ssl-mod dev
ssl-certs-folder ./lib/astron/certs/dev/

# Performance :
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
