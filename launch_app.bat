@echo off


REM Set the path to the Python executable within the virtual environment
set VENV_PATH=venv\Scripts\python.exe

REM Check if the virtual environment exists
if not exist venv (
    REM Create virtual environment
    python -m venv venv

    REM Activate the virtual environment
    call venv\Scripts\activate

    REM Install dependencies
    pip install -r requirements.txt

    REM Deactivate the virtual environment
    deactivate
)

REM Run your Python script
%VENV_PATH% ui_main.py
