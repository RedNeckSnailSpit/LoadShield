@echo off

REM Enable delayed expansion for version comparison
setlocal EnableDelayedExpansion

REM Read minimum versions from config.ini
for /F "tokens=*" %%A in ('powershell -Command "(Get-Content config.ini | Select-String -Pattern 'min_python_version').Matches.Groups[1].Value"') do set MIN_PYTHON_VERSION=%%A
for /F "tokens=*" %%A in ('powershell -Command "(Get-Content config.ini | Select-String -Pattern 'min_pip_version').Matches.Groups[1].Value"') do set MIN_PIP_VERSION=%%A

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Would you like to install Python automatically? (no/minimum/latest):
    set /p "install_python="
    if /i "!install_python!"=="no" (
        echo Download the minimum version here: https://www.python.org/ftp/python/%MIN_PYTHON_VERSION%/python-%MIN_PYTHON_VERSION%-amd64.exe
        echo Download the latest version here: https://www.python.org/ftp/python/latest/python-latest-amd64.exe
        pause
        exit /b 1
    ) else if /i "!install_python!"=="minimum" (
        set "installer_url=https://www.python.org/ftp/python/%MIN_PYTHON_VERSION%/python-%MIN_PYTHON_VERSION%-amd64.exe"
    ) else if /i "!install_python!"=="latest" (
        set "installer_url=https://www.python.org/ftp/python/latest/python-latest-amd64.exe"
    ) else (
        echo Invalid option. Exiting.
        pause
        exit /b 1
    )

    REM Download and install Python
    echo Downloading Python installer from !installer_url!...
    powershell -Command "Invoke-WebRequest -Uri !installer_url! -OutFile python_installer.exe"

    echo Installing Python silently...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    echo Python installed successfully. Please restart the script.
    pause
    exit /b 1
)

REM Function to compare versions
set "version_ge="
for /F "tokens=*" %%A in ('powershell -Command "$current_version = [version]::new('%PYTHON_VERSION%'); $min_version = [version]::new('%MIN_PYTHON_VERSION%'); $current_version -ge $min_version"') do set version_ge=%%A
if "!version_ge!" neq "True" (
    echo Your current Python version is %PYTHON_VERSION%. Minimum required version is %MIN_PYTHON_VERSION%.
    set /p "update_python=Would you like to update Python automatically? (no/minimum/latest): "
    if /i "!update_python!"=="no" (
        echo Download the minimum version here: https://www.python.org/ftp/python/%MIN_PYTHON_VERSION%/python-%MIN_PYTHON_VERSION%-amd64.exe
        echo Download the latest version here: https://www.python.org/ftp/python/latest/python-latest-amd64.exe
        pause
        exit /b 1
    ) else if /i "!update_python!"=="minimum" (
        set "installer_url=https://www.python.org/ftp/python/%MIN_PYTHON_VERSION%/python-%MIN_PYTHON_VERSION%-amd64.exe"
    ) else if /i "!update_python!"=="latest" (
        set "installer_url=https://www.python.org/ftp/python/latest/python-latest-amd64.exe"
    ) else (
        echo Invalid option. Exiting.
        pause
        exit /b 1
    )

    REM Download and install Python
    echo Downloading Python installer from !installer_url!...
    powershell -Command "Invoke-WebRequest -Uri !installer_url! -OutFile python_installer.exe"

    echo Installing Python silently...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    echo Python updated successfully. Please restart the script.
    pause
    exit /b 1
)

REM Check if PIP is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo PIP is not installed. Please install PIP to continue.
    pause
    exit /b 1
)

REM Check PIP version
for /F "tokens=2 delims= " %%A in ('pip -V') do set PIP_VERSION=%%A
for /F "tokens=*" %%A in ('powershell -Command "$current_version = [version]::new('%PIP_VERSION%'); $min_version = [version]::new('%MIN_PIP_VERSION%'); $current_version -ge $min_version"') do set version_ge=%%A
if "!version_ge!" neq "True" (
    echo PIP version %PIP_VERSION% is installed. Minimum required version is %MIN_PIP_VERSION%.
    set /p "update_pip=Would you like to update PIP? (no/minimum/latest): "
    if /i "!update_pip!"=="no" (
        echo To update PIP to the minimum version, run: python -m pip install --upgrade pip==%MIN_PIP_VERSION%
        echo To update PIP to the latest version, run: python -m pip install --upgrade pip
        pause
        exit /b 1
    ) else if /i "!update_pip!"=="minimum" (
        python -m pip install --upgrade pip==%MIN_PIP_VERSION%
    ) else if /i "!update_pip!"=="latest" (
        python -m pip install --upgrade pip
    ) else (
        echo Invalid option. Exiting.
        pause
        exit /b 1
    )
)

REM Check if --use-venv argument is provided
set "use_venv="
for %%A in (%*) do (
    if "%%A"=="--use-venv" (
        set "use_venv=true"
    )
)

REM Setup virtual environment if required
if defined use_venv (
    if not exist loadshield (
        echo Creating virtual environment...
        python -m venv loadshield
    )

    echo Activating virtual environment...
    call loadshield\Scripts\activate.bat
)

REM Install requirements
pip install -r requirements.txt

REM Run main.py
python main.py

REM Deactivate virtual environment if used
if defined use_venv (
    deactivate
)

pause
