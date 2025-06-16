import os

def auto_run():
    script_path = os.getcwd() + "\\" + "flask_server.pyw"
    startup_dir = os.getenv('APPDATA')  + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    bat_path = startup_dir + "\\script.bat"
    with open(bat_path, "w") as bat_file:
        bat_file.write(f'start "" pythonw "{script_path}"')


