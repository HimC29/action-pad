"""Action resolution and execution logic."""

import subprocess
import pyautogui
from constants import (
    ACTION_COMMAND, ACTION_HOTKEY, ACTION_MACRO, 
    ACTION_TOGGLE, ACTION_LAYER, VALID_ACTION_TYPES
)

def get_action(btn, states, btn_data):
    """Extract action data from button configuration."""
    action_type = btn["type"]
    if action_type == ACTION_COMMAND:
        return btn["command"]
    if action_type == ACTION_HOTKEY:
        return btn["keys"]
    if action_type == ACTION_MACRO:
        return btn["actions"]
    if action_type == ACTION_TOGGLE:
        return btn["on"] if not states["btn_toggle"][btn_data["btn"]] else btn["off"]
    if action_type == ACTION_LAYER:
        return btn["target"]
    raise ValueError(f"Unsupported action type: {action_type}")

def resolve_action(btn_data, states, btn_configs):
    """Resolve button press to an action based on current state."""
    layer = btn_configs["layers"][states["current_layer"]]
    btn_id = btn_data["btn"]
    
    if btn_id not in layer:
        return None

    btn = layer[btn_id]

    # Pick long action if duration is long and defined
    selected = btn["long"] if btn_data["duration"] == "long" and "long" in btn else btn

    action_type = selected.get("type")
    if not action_type:
        raise ValueError(f"Button {btn_id} has no type defined")
    if action_type not in VALID_ACTION_TYPES:
        raise ValueError(f"Unsupported action type: {action_type}")

    # Handle toggle buttons by picking on/off
    if action_type == ACTION_TOGGLE:
        if not ("on" in selected and "off" in selected):
            raise ValueError(f"Toggle button {btn_id} missing 'on' or 'off' action")
        inner = selected["on"] if not states["btn_toggle"][btn_id] else selected["off"]
        return {
            "type": inner["type"],
            "action": get_action(inner, states, btn_data),
            "toggle": True
        }

    return {
        "type": selected["type"],
        "action": get_action(selected, states, btn_data),
        "toggle": False
    }

def execute_action(action_and_type, states, btn_data):
    """Execute the resolved action."""
    action_type = action_and_type["type"]
    action = action_and_type["action"]

    if action_type == ACTION_COMMAND:
        subprocess.run(action, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return None
    
    if action_type == ACTION_HOTKEY:
        pyautogui.hotkey(action)
        return None
    
    if action_type == ACTION_MACRO:
        for sub_action in action:
            execute_action(
                {
                    "type": sub_action["type"],
                    "action": get_action(sub_action, states, btn_data)
                },
                states,
                btn_data
            )
        return None
    
    if action_type == ACTION_LAYER:
        return {"new_layer": action}
    
    return None
