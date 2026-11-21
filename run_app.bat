@echo off
cd /d "%~dp0"
python TTS_app.py
echo.
echo Program finished or crashed. Read the messages above.
pause