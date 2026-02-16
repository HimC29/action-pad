<div align="center">

# ⚡ Action Pad

### Your Physical Shortcut to Digital Productivity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

**Transform a simple Arduino keypad into a powerful productivity tool that executes commands, hotkeys, and macros at the press of a button.**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#%EF%B8%8F-demo) • [Configuration](#%EF%B8%8F-configuration) • [Contributing](#-contributing)

</div>

---

## 👁️ Demo

<div style="display: flex; align-items: center; justify-content: center; gap: 40px;">
  <img src="assets/demo.gif" alt="Action Pad Demo" width="600"/>
  <p style="max-width: 350px; margin: 0; font-weight: bold;">
    A button that executes the command <code>google-chrome & code</code> to open the browser and VS Code, improving efficiency.
  </p>
</div>

---

## ✨ Features

<table>
<tr>
<td>

✅ **Custom Button Actions**  
Assign commands, hotkeys, or macros to each button

✅ **Multi-Layer Support**  
Expand functionality without adding hardware

✅ **Short & Long Press**  
Double your actions with press duration detection

✅ **Command Execution**  
Run any terminal command instantly

</td>
<td>

✅ **Hotkey Automation**  
Trigger complex key combinations effortlessly

✅ **Macro Chaining**  
Combine multiple actions into workflows

✅ **Plug & Play**  
Auto-detects Arduino devices

✅ **JSON Configuration**  
Easy-to-edit, human-readable config

</td>
</tr>
</table>

---

## 🤔 Why Action Pad?

As developers, designers, and power users, we constantly switch between applications, execute repetitive commands, and trigger the same hotkey combinations dozens of times a day. **Action Pad was born from frustration with this inefficiency.**

### The Problem
- ⏱️ Repetitive keyboard shortcuts slow you down
- 🧠 Remembering complex key combinations is mentally taxing
- 💻 Context switching breaks your flow
- 🔄 Running the same terminal commands over and over is tedious

### The Solution
**A physical, programmable button pad that puts your most-used actions at your fingertips.** One button press can:
- Launch your entire development environment
- Copy text and send a notification
- Switch between different workflow "modes"
- Execute complex multi-step macros

It's like having a custom control panel for your digital life. 🎮

---

## 🚀 Quick Start

### Prerequisites

- Arduino board (Uno, Nano, Mega, etc.)
- 4x4 matrix keypad (or any compatible keypad)
- Python 3.6+
- Arduino IDE

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/HimC29/action-pad.git
cd action-pad
```

**2. Install Python dependencies**
```bash
pip install pyserial pyautogui
```

**3. Wire your keypad to Arduino**  
Connect keypad pins to Arduino digital pins (see [Wiring Guide](#-wiring-guide))

**4. Upload Arduino code**
- Open `/code/arduino/main/main.ino` in Arduino IDE
- Select your board and port
- Click Upload ⬆️

**5. Configure your buttons**
```bash
# Edit config.json to customize button actions
nano config.json  # or use your favorite editor
```

**6. Launch Action Pad**
```bash
# Linux/macOS
./launch.sh

# Windows
launch.bat
```

**7. Select your Arduino from the menu and start pressing buttons! 🎉**

---

## 🔌 Wiring Guide

Matrix keypads typically have 7-8 pins that connect to Arduino digital pins.

### Connection Steps

1. **Connect all keypad pins to Arduino digital pins**
2. **Check your keypad's datasheet** for the correct pin order (or experiment!)
3. **Update the Arduino code** if your mapping differs from the example

### Example Pin Mapping (4x4 Keypad)

```
Keypad Pin  →  Arduino Pin
─────────────────────────
Pin 1       →  D2
Pin 2       →  D3
Pin 3       →  D4
Pin 4       →  D5
Pin 5       →  D6
Pin 6       →  D7
Pin 7       →  D8
Pin 8       →  D9
```

<!-- TODO: Add wiring diagram image -->
<!-- Suggested: Create a Fritzing diagram or photo of your setup -->
<!-- Example: ![Wiring Diagram](docs/wiring-diagram.png) -->

> 💡 **Tip:** Different keypads may have different pin configurations. If buttons don't respond correctly, try adjusting the pin assignments in `/code/arduino/main/main.ino`.

---

## ⚙️ Configuration

Action Pad uses a simple JSON file to define button behaviors. Edit `config.json` to customize your setup.

### Configuration Structure

```json
{
    "active_layer": "default",
    "layers": {
        "default": {
            "btn1": { /* button config */ }
        }
    }
}
```

- **`active_layer`** - The layer that loads on startup
- **`layers`** - Contains all your layer definitions

### Button Action Types

#### 🔹 Hotkey
Trigger keyboard shortcuts

```json
"btn1": {
    "type": "hotkey",
    "keys": ["ctrl", "c"],
    "long": {
        "type": "hotkey",
        "keys": ["ctrl", "v"]
    }
}
```

#### 🔹 Command
Execute terminal commands

```json
"btn2": {
    "type": "command",
    "command": "google-chrome"
}
```

#### 🔹 Macro
Chain multiple actions together

```json
"btn3": {
    "type": "macro",
    "actions": [
        {
            "type": "hotkey",
            "keys": ["ctrl", "c"]
        },
        {
            "type": "command",
            "command": "notify-send 'Copied!'"
        }
    ]
}
```

#### 🔹 Layer Switch
Change to a different button layout

```json
"btn16": {
    "type": "layer",
    "target": "code-mode"
}
```

### Complete Example

<details>
<summary>Click to expand full config.json example</summary>

```json
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
            "btn16": {
                "type": "layer",
                "target": "default"
            }
        }
    }
}
```

</details>

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**!

### How to Contribute

1. **Fork the Project**
2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Ideas

- 🎨 Add new action types (mouse movements, delays, conditionals)
- 🖥️ Build a GUI configuration tool
- 📚 Improve documentation and examples
- 🐛 Report bugs and suggest features via [Issues](https://github.com/HimC29/action-pad/issues)

---

## 🌟 Contributors

Thanks to everyone who has contributed to Action Pad!

<a href="https://github.com/HimC29/action-pad/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HimC29/action-pad" />
</a>

Want to see your name here? Check out the [Contributing](#-contributing) section!

---

## 🗺️ Roadmap

- [ ] Additional action types (mouse control, delays, conditionals)
- [ ] Web-based GUI configuration tool
- [ ] Support for ESP32 and Raspberry Pi Pico
- [ ] Profile switching for different workflows
- [ ] Cloud sync for configurations
- [ ] Mobile companion app

Have an idea? [Open an issue](https://github.com/HimC29/action-pad/issues) and let's discuss!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

**TL;DR:** You can use, modify, and distribute this project freely. Just keep the original license notice.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- **[Arduino](https://www.arduino.cc/)** - The hardware platform that makes this possible
- **[pyserial](https://pypi.org/project/pyserial/)** - Python serial communication library
- **[pyautogui](https://pypi.org/project/PyAutoGUI/)** - GUI automation for Python

---

<div align="center">

### ⭐ Star this repo if you find it useful!

**Made with ❤️ by [HimC29](https://github.com/HimC29)**

[Report Bug](https://github.com/HimC29/action-pad/issues) • [Request Feature](https://github.com/HimC29/action-pad/issues) • [Discussions](https://github.com/HimC29/action-pad/discussions)

</div>
