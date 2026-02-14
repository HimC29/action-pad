import serial
import serial.tools.list_ports
import time
import json
import pyautogui
import subprocess
import arduino_funcs as af

def select_arduino_port():
    # Lists available serial ports and prompts the user to select one.
    # Get a list of available ports
    available_ports = [
        p for p in serial.tools.list_ports.comports()
        if p.description and p.description.lower() != "n/a"
    ]
    
    if not available_ports:
        print("No Action Pads found.")
        return None

    print("Available Action Pads:")
    # Display ports with an index number
    for i, port in enumerate(available_ports):
        # Using port.device for a reliable identifier
        print(f"{i + 1}: {port.device} - {port.description}")

    while True:
        try:
            # Prompt user for input
            choice = input("Port number: ")

            # Convert input to integer index
            port_index = int(choice) - 1

            # Validate the choice
            if 0 <= port_index < len(available_ports):
                selected_port = available_ports[port_index].device
                print(f"Selected port: {selected_port}")
                return selected_port
            else:
                print("Invalid input.")
        
        except ValueError:
            # Handle non-integer input
            print("Invalid input.")

def get_type_value(config):
    if "type" in config:
        type = config["type"]

    if type == "command":
        value = config["command"]
    elif type == "hotkey":
        value = config["keys"]
    elif type == "macro":
        value = config["actions"]
    elif type == "layer":
        value = config["target"]

    return [type, value]

def format_actions(type, value):
    if(type == "command"):
        return f"Command: {value}"
    
    if(type == "hotkey"):
        return f"Hotkey: {" + ".join(value)}"
    
    if(type == "macro"):
        formatted = "Macro:"
        for action in value:
            type_value = get_type_value(action)
            type = type_value[0]
            value = type_value[1]
            formatted += "\n"
            formatted += format_actions(type, value)
        return formatted
        
    if(type == "layer"):
        return f"Layer: {value}"

def do_command(type, value):
    try:
        if(type == "command"):
            subprocess.run(value, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        
        if(type == "hotkey"):
            pyautogui.hotkey(value)
            return True
        
        if(type == "macro"):
            for action in value:
                type_value = get_type_value(action)
                type = type_value[0]
                value = type_value[1]
                do_command(type, value)
            return True
            
        if(type == "layer"):
            return ["layer", value]

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("== Action Pad - Setup ==")
    print("Control actions on your device with a simple press of a button.\n")

    port = select_arduino_port()
    if(port == None): exit()
    try:
        af.set_arduino(serial.Serial(port=port, baudrate=9600, timeout=.1))
    except Exception as e:
        print(f"\nERROR: Could not connect to Action Pad\nDetails: {e}")
        exit()

    print("\nConnecting to Action Pad...")
    time.sleep(2)
    print("Successfully connected to Action Pad!")

    with open("config.json") as f:
        btn_configs = json.load(f)
        default_layer = btn_configs["active_layer"]
        layers = btn_configs["layers"]
        current_layer = default_layer

    while True:
        raw_btn = af.read_data()

        if raw_btn == None: continue

        btn_dur = raw_btn.split()
        btn = btn_dur[0]
        duration = btn_dur[1]

        if btn not in layers[current_layer]: continue

        if duration == "short":
            config = layers[current_layer][btn]
        elif duration == "long":
            config = layers[current_layer][btn]["long"]

        type_value = get_type_value(config)
        type = type_value[0]
        value = type_value[1]

        result = do_command(type, value)

        print()
        print(format_actions(type, value))

        if result == True or result == False: continue

        if result[0] == "layer":
            current_layer = result[1]

if(__name__ == "__main__"):
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit()