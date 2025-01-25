# Automated Mac Workflows

This repository provides automation scripts using Python to interact with Mac applications (e.g., WeChat). It includes:

- PyAutoGUI-based automation.  
- A CLI (wechat_cli.py) for scheduling and sending WeChat messages
- A GUI (wechat_gui.py) for scheduling and sending WeChat messages.  

## Requirements

1. macOS with Python 3.x installed.
2. Accessibility and Screen Recording permissions enabled for Python (necessary for PyAutoGUI to control the mouse/keyboard and read the screen).
   - Go to System Settings → Privacy & Security → Accessibility. Add your IDE (or Terminal if running Python directly).
   - Also in System Settings → Privacy & Security → Screen & System Audio Recording. Add your IDE or Terminal here.
3. Internet connection for installing required packages.
4. Additional Python packages listed in [requirements.txt](./requirements.txt).

## Usage

1. Install dependencies:  
   `pip install -r requirements.txt`
2. Run the GUI/CLI Code
   - GUI: `python wechat_gui.py`
   - CLI: `python wechat_cli.py "Friend Name" "Message" --repeat 5 --schedule 08:40` repeat and schedule are optional arguments. 
