"""UI functions for Action Pad TUI."""

import serial.tools.list_ports
from constants import COLORS, TYPE_ICONS, ACTION_HOTKEY, ACTION_MACRO

def print_header():
    """Display the application header."""
    from constants import VERSION
    print(f"\n{COLORS['BOLD']}{COLORS['CYAN']}⚡ Action Pad{COLORS['RESET']} {COLORS['DIM']}v{VERSION}{COLORS['RESET']}")
    print(f"{COLORS['DIM']}Your physical shortcut to digital productivity{COLORS['RESET']}")

def select_arduino_port():
    """List available serial ports and prompt user to select one."""
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

def print_connection_status(success=True, error=None):
    """Print connection status messages."""
    if success:
        print(f"\n{COLORS['YELLOW']}⟳ Connecting to Action Pad...{COLORS['RESET']}")
    else:
        print(f"\n{COLORS['RED']}✗ Connection failed: {error}{COLORS['RESET']}")

def print_ready():
    """Print ready message."""
    print(f"{COLORS['GREEN']}✓ Connected! Ready for input.{COLORS['RESET']}\n")
    print(f"{COLORS['DIM']}{'─' * 50}{COLORS['RESET']}")

def format_action_display(action_and_type):
    """Format action for display in TUI."""
    action = action_and_type["action"]
    action_type = action_and_type["type"]
    
    icon = TYPE_ICONS.get(action_type, '•')
    
    if action_type == ACTION_HOTKEY:
        action_str = ' + '.join(action) if isinstance(action, list) else str(action)
    elif action_type == ACTION_MACRO:
        steps = []
        for sub in action:
            if sub['type'] == ACTION_HOTKEY:
                keys = ' + '.join(sub['keys']) if isinstance(sub['keys'], list) else str(sub['keys'])
                steps.append(f"⌨️  {keys}")
            elif sub['type'] == 'command':
                steps.append(f"⚡ {sub['command']}")
        action_str = f"{len(action)} actions\n  {COLORS['DIM']}" + f"\n  ".join(steps) + COLORS['RESET']
    else:
        action_str = str(action)
    
    return f"{COLORS['BLUE']}{icon} {COLORS['BOLD']}{action_type.upper()}{COLORS['RESET']} {COLORS['DIM']}→{COLORS['RESET']} {COLORS['CYAN']}{action_str}{COLORS['RESET']}"

def print_layer_switch(layer_name):
    """Print layer switch notification."""
    print(f"{COLORS['MAGENTA']}📂 Switched to layer: {COLORS['BOLD']}{layer_name}{COLORS['RESET']}")

def print_error(error):
    """Print error message."""
    print(f"{COLORS['RED']}✗ Error: {error}{COLORS['RESET']}")
