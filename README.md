# Action Pad

[![Action Pad](https://img.shields.io/badge/Action-Pad-f97316?style=for-the-badge)](https://himc29.github.io/action-pad/) ![Productivity & Convenience](https://img.shields.io/badge/Productivity-Convenience-3b82f6?style=for-the-badge) ![MIT License](https://img.shields.io/badge/License-MIT-6b7280?style=for-the-badge)

An easy DIY Arduino button pad that lets you trigger commands, hotkeys, and macros to boost productivity and workflow efficiency.

---

## Features

- **Custom Button Actions** - Assign each button to run commands, hotkeys, or macros.
- **Layer Support** - Switch between layers to expand the number of available actions without adding more buttons.
- **Short & Long Press Detection** - Trigger different actions depending on how long a button is pressed.
- **Command Execution** - Run terminal commands directly from your button pad.
- **Hotkey Support** - Trigger single or multiple key combinations instantly.
- **Macro System** - Chain multiple actions together for more advanced workflows.
- **Plug & Play Setup** - Automatically detects connected Arduino devices.
- **Fully Configurable** - Edit button behavior easily through a JSON config file.

---

## How to start using

1. Clone this repository
    ```
    git clone https://github.com/HimC29/action-pad
    ```

1. Wire the keypad to the Arduino
[Click here to see wiring](#wiring)

1. Upload the code to the Arduino.
Open Arduino IDE and open the file at [/code/arduino/main/main.ino](/code/arduino/main/main.ino)
(You might have to change the code to match your keypad)

1. Edit [config.json](/config.json) to change what each button does.
[Learn how](#how-to-change-button-configurations)

1. Run [launch.sh](/launch.sh) on Linux/mac, [launch.bat](/launch.bat) on Windows.  
   > Make sure you have Python 3 and dependencies installed:
   > - pyserial
   > - pyautogui

1. Navigate through the TUI to connect to the Arduino and start executing actions.
[Learn how](#navigating-the-action-pad-tui)

---

## Navigating the Action Pad TUI

1. After you run [launch.sh](/launch.sh) / [launch.bat](/launch.bat), it will ask you to choose a Serial port that your device is connected to:
    ```
    == Action Pad - Setup ==
    Control actions on your device with a simple press of a button.

    Available Action Pads:
    1: /dev/ttyACM1 - ttyACM1
    ```
    Choose the correct Serial port by typing in the number at the left side and hitting enter.

1. Wait for it to connect to the Arduino.

1. Once it says `Successfully connected to Action Pad!`, you can start pressing buttons to execute actions.

1. Change what each button does in config.json, or use the sample configs.
(Stop and rerun [launch.sh](/launch.sh) / [launch.bat](/launch.bat) after changing)

---

## Wiring

Keypads have multiple pins that connect to the Arduino’s digital pins. The exact number of pins depends on your keypad (commonly 7 or 8).

### How to Connect
1. Connect all keypad pins to Arduino digital pins.
1. The exact pin order may differ between keypads, so check your keypad’s datasheet or just keep trying until you figure it out (that's what I did with mine).
1. If your keypad mapping doesn’t match the example in the Arduino code, update the pin assignments in the code to match your hardware.

### Example Mapping
> - Pin 1 → D2
> - Pin 2 → D3
> - Pin 3 → D4
> - Pin 4 → D5
> - Pin 5 → D6
> - Pin 6 → D7
> - Pin 7 → D8
> - Pin 8 → D9

> Tip: Even if your keypad has 7 pins, the same concept applies. Just connect all pins to digital pins and update the Arduino code if needed.

---

## How to change button configurations

To change the configuration on what each button does, change it in [config.json](/config.json).

### Format

1. Top level
    ```
    {
        "active_layer": "name-of-layer",
        "layers": { ... }
    }
    ```
    - **"active_layer"** - Which layer the pad starts on. (Change name-of-layer to your layer name)
    - **"layers"** - Contains all the layers you define.

1. Layers
A layer is basically a “mode” with its own set of button configurations.
    ```
    "name-of-layer": {
        "btn1": { ... },
        "btn2": { ... },
        "btn5": { ... },
        "btn16": { ... }
    }
    ```
    - **"btn1" - "btn16"** - These are the names of the buttons. You can check what are they in the [Arduino code](/code/arduino/main/main.ino).
    - **"properties"** - Each button has a type propertie that declares the type of action the button does. They also have another property that depends on the type which declares what it is the exact action the button needs to do.

1. Button Types
Your pad supports 4 main types: (as of Version 1.0)
    - **"hotkey"**
        ```
        btn1": {
            "type": "hotkey",
            "keys": ["ctrl", "c"],
            "long": {
                "type": "hotkey",
                "keys": ["ctrl", "v"]
            }
        }
        ```
        - **The "type" attribute** - The type is "hotkey", which shows that this button will execute a sequence of keys which is shown under the "keys" attribute. This applies to other buttons as well.
        - **The "keys" attribute** - This stores the key sequence that executes when the button is pressed.
        - **The "long" attribute** - Optional, an extra action (hotkey in this situation) to run when the button is long-pressed. (This can be used for any button and any type)
    - **"command"**
        ```
        "btn2": {
            "type": "command",
            "command": "google-chrome",
        }
        ```
        - **The "command" attribute** - This stores information about what command to run when the button is pressed.
    - **"macro"**
        ```
        "btn5": {
            "type": "macro",
            "actions": [
                {
                    "type": "hotkey",
                    "keys": ["ctrl", "c"]
                },
                {
                    "type": "command",
                    "command": "notify-send --app-name='System' 'Copied text!'"
                }
            ]
        }
        ```
        - **The "actions" attribute** - This stores information about what action to run when pressed. Actions inside a macro follow the same format as individual button types.
    - **"layer"**
        ```
        "btn16": {
            "type": "layer",
            "target": "code-mode"
        }
        ```
        - **"target"** - This changes the current layer to the layer stated inside this attribute.

1. Example
    ```
    {
        "active_layer": "default",
        "layers": {
            "default": {
                "btn1": {
                    "type": "macro",
                    "actions": [
                        {
                            "type": "hotkey",
                            "keys": ["ctrl", "c"]
                        },
                        {
                            "type": "command",
                            "command": "notify-send --app-name='System' 'Copied text!'"
                        }
                    ],
                    "long": {
                        "type": "macro",
                        "actions": [
                            {
                                "type": "hotkey",
                                "keys": ["ctrl", "v"]
                            },
                            {
                                "type": "command",
                                "command": "notify-send --app-name='System' 'Pasted text!'"
                            }
                        ]
                    }
                },
                "btn2": {
                    "type": "command",
                    "command": "google-chrome",
                    "long": {
                        "type": "command",
                        "command": "firefox"
                    }
                },
                "btn16": {
                    "type": "layer",
                    "target": "code-mode"
                }
            },
            "code-mode": {
                "btn1": {
                    "type": "command",
                    "command": "google-chrome & code"
                },
                "btn4": {
                    "type": "macro",
                    "actions": [
                        {
                            "type": "hotkey",
                            "keys": ["ctrl", "c"]
                        },
                        {
                            "type": "command",
                            "command": "notify-send --app-name='System' 'Copied text!'"
                        }
                    ],
                    "long": {
                        "type": "macro",
                        "actions": [
                            {
                                "type": "hotkey",
                                "keys": ["ctrl", "v"]
                            },
                            {
                                "type": "command",
                                "command": "notify-send --app-name='System' 'Pasted text!'"
                            }
                        ]
                    }
                },
                "btn16": {
                    "type": "layer",
                    "target": "default"
                }
            }
        }
    }
    ```

## Contributing

Want to make Action Pad better? Contributions are welcome!  

---

## Future Plans

- More types to make Action Pad more user friendly (Currently only a few types are supported; most of the time you may need to use a command for certain actions.)
- Add a proper GUI on another branch

---

## License

MIT License – feel free to use and modify Action Pad.

---

## Credits / Third-Party Assets

- [Arduino](https://www.arduino.cc/) – Hardware platform used for the button pad
- [pyserial](https://pypi.org/project/pyserial/) – Python library for serial communication
- [pyautogui](https://pypi.org/project/PyAutoGUI/) – Python library for GUI automation