# Future updates

# Delay for macro
# Holding (repeats something until release)
    # for example:
        # holding down a button that keeps increasing brightness until release
# Text (Type out text)
# Open app (Previously users had to use commands)
# Focus (Focus onto apps instead of opening it)

import serial
import serial.tools.list_ports
import time
import json
import pyautogui
import subprocess
import arduino_funcs as af

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

def select_arduino_port():
    available_ports = [
        p for p in serial.tools.list_ports.comports()
        if p.description and p.description.lower() != "n/a"
    ]
    
    if not available_ports:
        print(f"{COLORS['RED']}✗ No Action Pads found.{COLORS['RESET']}")
        return None

    box_width = 47
    print(f"\n{COLORS['CYAN']}┌─ Available Action Pads ─────────────────────┐{COLORS['RESET']}")
    for i, port in enumerate(available_ports):
        content = f" {i + 1}: {port.device} - {port.description}"
        padding = box_width - len(content) - 1
        print(f"{COLORS['CYAN']}│{COLORS['RESET']}{COLORS['BOLD']}{i + 1}{COLORS['RESET']}: {COLORS['GREEN']}{port.device}{COLORS['RESET']} {COLORS['DIM']}- {port.description}{COLORS['RESET']}{' ' * padding}{COLORS['CYAN']}│{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}└─────────────────────────────────────────────┘{COLORS['RESET']}")

    while True:
        try:
            choice = input(f"\n{COLORS['YELLOW']}❯{COLORS['RESET']} Select port number: ")
            port_index = int(choice) - 1

            if 0 <= port_index < len(available_ports):
                selected_port = available_ports[port_index].device
                print(f"{COLORS['GREEN']}✓ Selected: {selected_port}{COLORS['RESET']}")
                return selected_port
            else:
                print(f"{COLORS['RED']}✗ Invalid selection{COLORS['RESET']}")
        
        except ValueError:
            print(f"{COLORS['RED']}✗ Please enter a number{COLORS['RESET']}")

def create_states(btn_configs):
    current_layer = btn_configs["active_layer"]

    btn_toggle = {}
    for i in range(16):
        btn_toggle[f"btn{i + 1}"] = False

    return {
        "current_layer": current_layer,
        "btn_toggle": btn_toggle
    }

def get_btn_data():
    raw_btn_data = af.read_data()
    if raw_btn_data == None: return None

    btn_data = raw_btn_data.split()
    return {
        "btn": btn_data[0],
        "duration": btn_data[1]
    }

def get_action(btn, states, btn_data):
        action_type = btn["type"]
        if action_type == "command":
            return btn["command"]
        if action_type == "hotkey":
            return btn["keys"]
        if action_type == "macro":
            return btn["actions"]
        if action_type == "toggle":
            if states["btn_toggle"][btn_data["btn"]] == False:
                return btn["on"]
            else:
                return btn["off"]
        if action_type == "layer":
            return btn["target"]
        raise ValueError(f"Unsupported action type: {action_type}")

# btn_data
# "btn"
# "duration"

# states
# "current_layer"
# "btn_toggle"

# btn_configs is the whole json
def resolve_action(btn_data, states, btn_configs):
    layer = btn_configs["layers"][states["current_layer"]]
    btn_id = btn_data["btn"]
    if btn_id not in layer:
        return

    btn = layer[btn_id]

    # Pick long action if duration is long and defined
    if btn_data["duration"] == "long" and "long" in btn:
        selected = btn["long"]
    else:
        selected = btn

    action_type = selected.get("type")
    if not action_type:
        raise ValueError(f"Button {btn_id} has no type defined")
    if action_type not in ("command", "hotkey", "macro", "toggle", "layer"):
        raise ValueError(f"Unsupported action type: {action_type}")

    # Handle toggle buttons by picking on/off
    if action_type == "toggle":
        if not ("on" in selected and "off" in selected):
            raise ValueError(f"Toggle button {btn_id} missing 'on' or 'off' action")
        # Decide which inner action to run
        inner = selected["on"] if not states["btn_toggle"][btn_id] else selected["off"]
        # Return the inner action instead
        return {
            "type": inner["type"],
            "action": get_action(inner, states, btn_data),
            "toggle": True
        }

    # Non-toggle buttons
    return {
        "type": selected["type"],
        "action": get_action(selected, states, btn_data),
        "toggle": False
    }

# action looks something like this
# {'type': 'command', 'action': 'google-chrome'}
def execute_action(action_and_type, states, btn_data):
    action_type = action_and_type["type"]
    action = action_and_type["action"]

    if action_type == "command":
        subprocess.run(action, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    if action_type == "hotkey":
        pyautogui.hotkey(action)
        return True  
    if action_type == "macro":
        for sub_action in action:
            execute_action(
                {
                    "type": sub_action["type"],
                    "action": get_action(sub_action, states, btn_data)
                },
                states,
                btn_data
            )
        return True
    if action_type == "layer":
        return {"new_layer": action}
    
def pretty_action_and_type(action_and_type):
    action = action_and_type["action"]
    action_type = action_and_type["type"]
    
    type_icons = {
        'command': '⚡',
        'hotkey': '⌨️',
        'macro': '🔗',
        'layer': '📂',
        'toggle': '🔄'
    }
    icon = type_icons.get(action_type, '•')
    
    if action_type == 'hotkey':
        action_str = ' + '.join(action) if isinstance(action, list) else str(action)
    elif action_type == 'macro':
        steps = []
        for sub in action:
            if sub['type'] == 'hotkey':
                keys = ' + '.join(sub['keys']) if isinstance(sub['keys'], list) else str(sub['keys'])
                steps.append(f"⌨️  {keys}")
            elif sub['type'] == 'command':
                steps.append(f"⚡ {sub['command']}")
        action_str = f"{len(action)} actions\n  {COLORS['DIM']}" + f"\n  ".join(steps) + COLORS['RESET']
    else:
        action_str = str(action)
    
    return f"{COLORS['BLUE']}{icon} {COLORS['BOLD']}{action_type.upper()}{COLORS['RESET']} {COLORS['DIM']}→{COLORS['RESET']} {COLORS['CYAN']}{action_str}{COLORS['RESET']}"

def main():
    print(f"\n{COLORS['BOLD']}{COLORS['CYAN']}⚡ Action Pad{COLORS['RESET']} {COLORS['DIM']}v1.2.0{COLORS['RESET']}")
    print(f"{COLORS['DIM']}Your physical shortcut to digital productivity{COLORS['RESET']}")

    port = select_arduino_port()
    if(port == None): exit()
    try:
        af.set_arduino(serial.Serial(port=port, baudrate=9600, timeout=.1))
    except Exception as e:
        print(f"\n{COLORS['RED']}✗ Connection failed: {e}{COLORS['RESET']}")
        exit()

    print(f"\n{COLORS['YELLOW']}⟳ Connecting to Action Pad...{COLORS['RESET']}")
    time.sleep(2)
    print(f"{COLORS['GREEN']}✓ Connected! Ready for input.{COLORS['RESET']}\n")
    print(f"{COLORS['DIM']}{'─' * 50}{COLORS['RESET']}")

    with open("config.json") as f:
        btn_configs = json.load(f)

    # "current_layer"
    # "btn_toggle"
    states = create_states(btn_configs)

    while True:
        btn_data = get_btn_data()
        if btn_data == None: continue
        try:
            action_and_type = resolve_action(btn_data, states, btn_configs)
            if action_and_type == None:
                continue
            if action_and_type["toggle"] == True:
                states["btn_toggle"][btn_data["btn"]] = not states["btn_toggle"][btn_data["btn"]]        
            result = execute_action(action_and_type, states, btn_data)
            
            print(pretty_action_and_type(action_and_type))

            if result == True: continue

            if "new_layer" in result:
                states["current_layer"] = result["new_layer"]
                print(f"{COLORS['MAGENTA']}📂 Switched to layer: {COLORS['BOLD']}{result['new_layer']}{COLORS['RESET']}")

        except ValueError as e:
            print(f"{COLORS['RED']}✗ Error: {e}{COLORS['RESET']}")
    # states["btn_toggle"][btn_id] to get curr btn

if(__name__ == "__main__"):
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit()
