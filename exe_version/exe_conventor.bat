@echo off
pip install -r requirements.txt
pyinstaller --noconsole --onefile flask_server.py
pyinstaller --noconsole --onefile --add-data "dist\flask_server.exe;." tic_tac_toe.py
copy dist\tic_tac_toe.exe .
rmdir /S /Q dist
rmdir /S /Q build
del flask_server.spec
del tic_tac_toe.spec
echo finished!

pause