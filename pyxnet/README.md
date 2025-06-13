# Tic Tac Toe Backdoor

This is a stealth backdoor project disguised as a simple **Tic Tac Toe** game.  
While the game is running in the foreground, a hidden reverse shell is activated in the background.

## Features

- Fun Tic Tac Toe game in the front
- Hidden Flask-based CMD control panel in the background
- Connects to the cloud using **Serveo.net**
- If Serveo is unavailable, it automatically falls back to **localhost.run**
- Sends the attacker (you) a link to the web interface via email
- Adds itself to the **Windows startup folder**, so it runs on every boot
- Comes in both `.py` and `.exe` versions
- Includes a `.bat` script for easy `.exe` creation

> **For educational and ethical use only!**  
> Running unauthorized backdoors on others' machines is **illegal**.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ilaygershon/tic-tac-toe-backdoor.git
cd tic-tac-toe-backdoor
pip install -r requirements.txt
```

> **If you're using `tic_tac_toe.exe`, you can run it directly without installing dependencies.**

---

## Running the Project

### Option 1: Run the Python version
```bash
# Set the destination email for receiving the command panel link.
python set_email.py 
python tic_tac_toe.py 
```

### Option 2: Run the compiled `.exe` version

```bash
python setup.py
```
Follow the instructions and it will create the exe file for you.

---

## Converting Python to EXE

`.bat` script is included to easily generate `.exe` files using **PyInstaller**.

### Run it like this:

```bash
exe_convertor.bat
```

It will:
- Install required packages
- Convert `flask_server.py` and `tic_tac_toe.py` into `.exe`
- Move the executables into the right place
- Clean up build files

> **Note:** `setup.py` automatically runs this `.bat` file for you.

---

## Notes

- **Only works on Windows**
- The program ensures persistence by copying itself to the startup folder
- A command-line interface is exposed via Flask and hosted using a reverse tunnel (Serveo or Localhost.run)
- The generated command panel is accessible from anywhere and sent to your email
    

---

## Author

Created by [Ilay Gershon](https://github.com/Ilaygershon)
