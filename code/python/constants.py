"""Constants used throughout the Action Pad application."""

# Version
VERSION = "1.2.0"

# ANSI color codes
COLORS = {
    'CYAN': '\033[96m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'BOLD': '\033[1m',
    'DIM': '\033[2m',
    'RESET': '\033[0m'
}

# Action types
ACTION_COMMAND = "command"
ACTION_HOTKEY = "hotkey"
ACTION_MACRO = "macro"
ACTION_TOGGLE = "toggle"
ACTION_LAYER = "layer"

VALID_ACTION_TYPES = (ACTION_COMMAND, ACTION_HOTKEY, ACTION_MACRO, ACTION_TOGGLE, ACTION_LAYER)

# Action type icons
TYPE_ICONS = {
    ACTION_COMMAND: '⚡',
    ACTION_HOTKEY: '⌨️',
    ACTION_MACRO: '🔗',
    ACTION_LAYER: '📂',
    ACTION_TOGGLE: '🔄'
}
