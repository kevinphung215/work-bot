@echo off
:: Batch script to automatically set up and run the Affidavit Generator
:: Checks for Python, installs if missing, installs dependencies, then runs the app

title Affidavit Generator Setup

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
    goto :CHECK_PACKAGES
) else (
    echo Python not found. Installing Python...
    goto :INSTALL_PYTHON
)

:INSTALL_PYTHON
:: Download and install Python with silent install and PATH addition
echo Downloading Python installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe', 'python_installer.exe')"

echo Installing Python (this may take a few minutes)...
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
del python_installer.exe

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install Python. Please install it manually from python.org
    pause
    exit /b 1
)

:CHECK_PACKAGES
:: Check and install required packages
echo Checking for required Python packages...
python -m pip install --upgrade pip >nul 2>&1
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages (flask, docxtpl, python-docx)...
    python -m pip install flask docxtpl python-docx
) else (
    echo Required packages already installed.
)

:: Run the application
echo Starting Affidavit Generator...
start python app.py
timeout /t 5 >nul
start http://127.0.0.1:5000/

echo The Affidavit Generator should now be running in your web browser.
echo Keep this window open while using the application.
pause