from panda3d.core import *

_speech_balloon_3d = None

def setSpeechBalloon3d(speech_balloon_3d):
    global _speech_balloon_3d
    _speech_balloon_3d = speech_balloon_3d

def getSpeechBalloon3d():
    return _speech_balloon_3d

_global_nametag_scale = 1.0

def setGlobalNametagScale(global_nametag_scale):
    global _global_nametag_scale
    _global_nametag_scale = global_nametag_scale

def getGlobalNametagScale():
    return _global_nametag_scale

_camera = NodePath()

def setCamera(camera):
    global _camera
    _camera = camera

def getCamera():
    return _camera

_master_nametags_active = True

def setMasterNametagsActive(master_nametags_active):
    global _master_nametags_active
    _master_nametags_active = master_nametags_active

def getMasterNametagsActive():
    return _master_nametags_active

_min_2d_alpha = 0.0

def setMin2dAlpha(min_2d_alpha):
    global _min_2d_alpha
    global _margin_prop_seq
    _min_2d_alpha = min_2d_alpha
    _margin_prop_seq += 1

def getMin2dAlpha():
    return _min_2d_alpha

_arrow_color = [
    Vec4(1.0, 0.40000001, 0.2, 1.0),
    Vec4(1.0, 0.40000001, 0.2, 1.0),
    Vec4(1.0, 0.40000001, 0.2, 1.0),
    Vec4(1.0, 0.40000001, 0.2, 1.0),
    Vec4(0.30000001, 0.60000002, 1.0, 1.0),
    Vec4(0.55000001, 0.55000001, 0.55000001, 1.0),
    Vec4(0.30000001, 0.60000002, 1.0, 1.0),
    Vec4(0.30000001, 0.69999999, 0.30000001, 1.0),
    Vec4(0.30000001, 0.30000001, 0.69999999, 1.0)
]

def getArrowColor(index, isRetro = False):
    if isRetro:
        if index in (7, 8):
            index = 0

    return _arrow_color[index]

_mouse_watcher = None

def setMouseWatcher(mouse_watcher):
    global _mouse_watcher
    _mouse_watcher = mouse_watcher

def getMouseWatcher():
    return _mouse_watcher

_master_arrows_on = True

def setMasterArrowsOn(master_arrows_on):
    global _master_arrows_on
    _master_arrows_on = master_arrows_on

def getMasterArrowsOn():
    return _master_arrows_on

_toon = NodePath()

def setToon(toon):
    global _toon
    _toon = toon

def getToon():
    return _toon

_master_nametags_visible = True

def setMasterNametagsVisible(master_nametags_visible):
    global _master_nametags_visible
    _master_nametags_visible = master_nametags_visible

def getMasterNametagsVisible():
    return _master_nametags_visible

_thought_balloon_2d = None

def setThoughtBalloon2d(thought_balloon_2d):
    global _thought_balloon_2d
    _thought_balloon_2d = thought_balloon_2d

def getThoughtBalloon2d():
    return _thought_balloon_2d

_max_2d_alpha = 0.6

def setMax2dAlpha(max_2d_alpha):
    global _max_2d_alpha
    global _margin_prop_seq
    _max_2d_alpha = max_2d_alpha
    _margin_prop_seq += 1

def getMax2dAlpha():
    return _max_2d_alpha

_onscreen_chat_forced = False

def setOnscreenChatForced(onscreen_chat_forced):
    global _onscreen_chat_forced
    _onscreen_chat_forced = onscreen_chat_forced

def getOnscreenChatForced():
    return _onscreen_chat_forced

_nametag_card = NodePath()

def setNametagCard(nametag_card, nametag_card_frame):
    global _nametag_card
    global _nametag_card_frame
    _nametag_card = nametag_card
    _nametag_card_frame = nametag_card_frame

def getNametagCard():
    return _nametag_card

_nametag_card_frame = Vec4(0, 0, 0, 0)

def getNametagCardFrame():
    return _nametag_card_frame

_rollover_sound = None

def setRolloverSound(rollover_sound):
    global _rollover_sound
    _rollover_sound = rollover_sound


def getRolloverSound():
    return _rollover_sound


_speech_balloon_2d = None


def setSpeechBalloon2d(speech_balloon_2d):
    global _speech_balloon_2d
    _speech_balloon_2d = speech_balloon_2d

def getSpeechBalloon2d():
    return _speech_balloon_2d

_text_node = TextNode('nametag')

def getTextNode():
    return _text_node

_click_sound = None

def setClickSound(click_sound):
    global _click_sound
    _click_sound = click_sound

def getClickSound():
    return _click_sound

_quit_button = [NodePath(), NodePath(), NodePath(), NodePath()]

def setQuitButton(state, quit_button):
    global _quit_button
    _quit_button[state] = quit_button

def getQuitButton(state):
    return _quit_button[state]

_arrow_model = NodePath()

def setArrowModel(arrow_model):
    global _arrow_model
    _arrow_model = arrow_model

def getArrowModel():
    return _arrow_model

_thought_balloon_3d = None

def setThoughtBalloon3d(thought_balloon_3d):
    global _thought_balloon_3d
    _thought_balloon_3d = thought_balloon_3d

def getThoughtBalloon3d():
    return _thought_balloon_3d

_name_bg = [
    # CCNormal
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCNoChat
    Vec4(1, 1, 1, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCNonPlayer
    Vec4(1, 1, 1, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCSuit
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCToonBuilding
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCSuitBuilding
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCHouseBuilding
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCSpeedChat
    Vec4(1, 1, 1, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # CCFreeChat
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5)
]

def getNameBg(color_code, state):
    return _name_bg[4 * color_code + state]

_player_name_bg = [
    # Regular
    Vec4(0.8, 0.8, 0.8, 0.5),
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.8, 0.8, 0.8, 0.5),

    # Sort of Dark
    Vec4(0.4, 0.4, 0.4, 0.6),
    Vec4(0.8, 0.8, 0.8, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.4, 0.4, 0.4, 0.5),

    # Dark
    Vec4(0.2, 0.2, 0.2, 0.6),
    Vec4(0.8, 0.8, 0.8, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0.2, 0.2, 0.2, 0.5),
    
    # Really Dark
    Vec4(0, 0, 0, 0.6),
    Vec4(0.8, 0.8, 0.8, 0.6),
    Vec4(1, 1, 1, 1),
    Vec4(0, 0, 0, 0.5),
]
    
def getPlayerNameBg(nametag_color, state):
    return _player_name_bg[4 * nametag_color + state]

# State 0: Ready (Same as 4)
# State 0: Depressed
# State 3: Rollover
# State 4: Inactive (Same as 1)

_player_name_fg = [
    # Default Blue
    Vec4(0.3, 0.3, 0.7, 1),
    
    # Beta Blue
    Vec4(0, 0, 1, 1),
    
    # Red
    Vec4(0.85, 0, 0, 1),
    
    # Pink
    Vec4(0.85, 0.61, 0.75, 1),
 
    # Purple
    Vec4(0.54, 0.28, 0.75, 1),
 
    # Green
    Vec4(0, 0.8, 0, 1),
    
    # Orange
    Vec4(0.99, 0.48, 0.16, 1),
    
    # Yellow
    Vec4(0.99, 0.89, 0.32, 1),
    
    # Slate Blue
    Vec4(0.46, 0.37, 0.82, 1),
    
    # Icy Blue
    Vec4(0.67, 0.92, 1, 1),
    
    # Light Blue
    Vec4(0.43, 0.9, 0.83, 1),
    
    # Aqua
    Vec4(0.34, 0.82, 0.95, 1),
    
    # Regular Blue
    Vec4(0.19, 0.56, 0.77, 1),
    
    # Steel Blue
    Vec4(0.325, 0.407, 0.601, 1),
    
    # Maroon
    Vec4(0.71, 0.23, 0.43, 1),

    # Lavender
    Vec4(0.72, 0.47, 0.85, 1),
    
    # Hot Pink
    Vec4(0.99, 0.25, 0.39, 1),
    
    # Ruby
    Vec4(0.88, 0.07, 0.37, 1),
    
    # Black
    Vec4(0.1, 0.1, 0.1, 1),
    
    # White
    Vec4(0.95, 0.95, 0.95, 1),

    # Silver 
    Vec4(0.74, 0.75, 0.76, 1),
    
    # Gray
    Vec4(0.50196078431, 0.50196078431, 0.50196078431, 1),
    
    # Brown
    Vec4(0.64, 0.35, 0.26, 1),
    
    # Golden Yellow
    Vec4(1, 0.91, 0, 1),
    
    # Metallic Gold
    Vec4(0.831, 0.686, 0.2157, 1),
]

def getPlayerNameFg(nametag_color):
    return _player_name_fg[nametag_color]

NAMETAG_COLOR_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
NAMETAG_COLOR_LEN = 25
NAMETAG_PANEL_COLOR_LEN = 4

_page_button = [NodePath(), NodePath(), NodePath(), NodePath()]

def setPageButton(state, page_button):
    global _page_button
    _page_button[state] = page_button

def getPageButton(state):
    return _page_button[state]

_name_fg = [
    # CCNormal
    Vec4(0, 0, 1, 1),
    Vec4(0.5, 0.5, 1, 1),
    Vec4(0.5, 0.5, 1, 1),
    Vec4(0.3, 0.3, 0.7, 1),

    # CCNoChat
    Vec4(0.8, 0.4, 0, 1),
    Vec4(1, 0.5, 0.5, 1),
    Vec4(1, 0.5, 0, 1),
    Vec4(0.6, 0.4, 0.2, 1),

    # CCNonPlayer
    Vec4(0.8, 0.4, 0, 1),
    Vec4(1, 0.5, 0.5, 1),
    Vec4(1, 0.5, 0, 1),
    Vec4(0.6, 0.4, 0.2, 1),

    # CCSuit
    Vec4(0, 0, 0, 1),
    Vec4(1, 1, 1, 1),
    Vec4(0.5, 0.5, 0.5, 1),
    Vec4(0.2, 0.2, 0.2, 1),

    # CCToonBuilding
    Vec4(0, 0, 0, 1),
    Vec4(1, 1, 1, 1),
    Vec4(0.5, 0.5, 0.5, 1),
    Vec4(0.3, 0.6, 1, 1),

    # CCSuitBuilding
    Vec4(0, 0, 0, 1),
    Vec4(1, 1, 1, 1),
    Vec4(0.5, 0.5, 0.5, 1),
    Vec4(0.55, 0.55, 0.55, 1),

    # CCHouseBuilding
    Vec4(0, 0, 0, 1),
    Vec4(1, 1, 1, 1),
    Vec4(0.5, 0.5, 0.5, 1),
    Vec4(0.3, 0.6, 1, 1),

    # CCSpeedChat
    Vec4(0, 0.6, 0.2, 1),
    Vec4(0, 0.6, 0.2, 1),
    Vec4(0, 1, 0.5, 1),
    Vec4(0.1, 0.4, 0.2, 1),

    # CCFreeChat
    Vec4(0.3, 0.3, 0.7, 1),
    Vec4(0.2, 0.2, 0.5, 1),
    Vec4(0.5, 0.5, 1, 1),
    Vec4(0.3, 0.3, 0.7, 1)
]

def getNameFg(color_code, state, isRetro = False):
    if isRetro:
        if color_code in (1, 2):
            color_code = 7
        elif color_code == 7:
            color_code = 1

    return _name_fg[4 * color_code + state]

def getNameWordwrap():
    return 7.5

_card_pad = Vec4(0.1, 0.1, 0.1, 0)

def getCardPad():
    return _card_pad

_whisper_colors = [
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.6, 0.8, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.4, 0.8, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.6, 0.8, 0.6))
    ],
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.6, 0.8, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.4, 0.8, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.6, 0.8, 0.6))
    ],
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.3, 0.6, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.4, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.3, 0.6, 0.6))
    ],
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.3, 0.6, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.4, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.8, 0.3, 0.6, 0.6))
    ],
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.6, 0.8, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.4, 1.0, 1.0, 0.4)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.3, 0.8, 0.3, 0.6))
    ],
    [
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.97, 0.43, 0.1, 0.6)),
        (Vec4(1.0, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.98, 0.6, 0.38, 0.6)),
        (Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.97, 0.43, 0.1, 0.6))
    ]
]

def getWhisperFg(color_code, state):
    return Vec4(_whisper_colors[color_code][state][0])

def getWhisperBg(color_code, state):
    return Vec4(_whisper_colors[color_code][state][1])

_balloon_modulation_color = Vec4(1.0, 1.0, 1.0, 1.0)

def setBalloonModulationColor(balloon_modulation_color):
    global _balloon_modulation_color
    _balloon_modulation_color = balloon_modulation_color

def getBalloonModulationColor():
    return _balloon_modulation_color

def getChatFg(color_code, state):
    return [Vec4(0.0, 0.0, 0.0, 1.0),
            Vec4(1.0, 0.5, 0.5, 1.0),
            Vec4(0.0, 0.6, 0.6, 1.0),
            Vec4(0.0, 0.0, 0.0, 1.0)][state]

def getChatBg(color_code, state):
    return [Vec4(1.0, 1.0, 1.0, 1.0),
            Vec4(1.0, 1.0, 1.0, 1.0),
            Vec4(1.0, 1.0, 1.0, 1.0),
            Vec4(1.0, 1.0, 1.0, 1.0)][state]

_margin_prop_seq = 0
_default_qt_color = Vec4(0.8, 0.8, 1, 1)
_balloon_text_origin = Point3(1.0, 0, 2.0)
