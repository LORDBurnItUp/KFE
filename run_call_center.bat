@echo off
REM Run script for KFE Call Center

echo KFE Call Center - Professional AI Assistant
echo ==============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

REM Run setup test
echo.
echo Running system check...
python src\test_setup.py

if %errorlevel% equ 0 (
    echo.
    echo Launching Call Center...
    echo.
    python src\call_center_assistant.py
) else (
    echo.
    echo Setup verification failed. Please fix the issues above.
    pause
    exit /b 1
)

pause
