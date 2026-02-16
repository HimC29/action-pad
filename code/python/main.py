"""Action Pad - Your physical shortcut to digital productivity."""

import serial
import time
import arduino_funcs as af
from config import load_config, create_states
from actions import resolve_action, execute_action
from ui import (
    print_header, select_arduino_port, print_connection_status,
    print_ready, format_action_display, print_layer_switch, print_error
)

def get_btn_data():
    """Read and parse button data from Arduino."""
    raw_btn_data = af.read_data()
    if raw_btn_data is None:
        return None

    btn_data = raw_btn_data.split()
    return {
        "btn": btn_data[0],
        "duration": btn_data[1]
    }

def main():
    """Main application loop."""
    print_header()

    port = select_arduino_port()
    if port is None:
        exit()
    
    try:
        af.set_arduino(serial.Serial(port=port, baudrate=9600, timeout=.1))
    except Exception as e:
        print_connection_status(success=False, error=e)
        exit()

    print_connection_status(success=True)
    time.sleep(2)
    print_ready()

    btn_configs = load_config()
    states = create_states(btn_configs)

    while True:
        btn_data = get_btn_data()
        if btn_data is None:
            continue
        
        try:
            action_and_type = resolve_action(btn_data, states, btn_configs)
            if action_and_type is None:
                continue
            
            if action_and_type["toggle"]:
                states["btn_toggle"][btn_data["btn"]] = not states["btn_toggle"][btn_data["btn"]]
            
            result = execute_action(action_and_type, states, btn_data)
            print(format_action_display(action_and_type))

            if result and "new_layer" in result:
                states["current_layer"] = result["new_layer"]
                print_layer_switch(result["new_layer"])

        except ValueError as e:
            print_error(e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit()
