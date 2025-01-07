@echo off
title Presence System
REM Navigate to the project directory
cd /d %~dp0

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run the main.py file
pip install -r requirements.txt
python main.py
