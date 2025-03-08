@echo off

REM Detect architecture
set "arch="
for /f "tokens=2 delims==" %%A in ('wmic OS get OSArchitecture /value 2^>nul') do (
    set "arch=%%A"
)

REM Read versions from config.json
for /f "delims=" %%A in ('powershell -Command "Get-Content config.json | ConvertFrom-Json"') do (
    if "%%A"=="    " echo Minimum Python Version: %%A
    if "%%A"=="    " echo Minimum PIP Version: %%A
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Would you like to install Python automatically? (no/minimum/latest):
    set /p "install_python="
    if /i "%install_python%"=="no" (
        echo You can download Python here: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        if /i "%install_python%"=="minimum" (
            if /i "%arch%"=="32-bit" (
                set "installer_url=https://www.python.org/ftp/python/%min_python_version%/python-%min_python_version%.exe"
            ) else if /i "%arch%"=="64-bit" (
                set "installer_url=https://www.python.org/ftp/python/%min_python_version%/python-%min_python_version%-amd64.exe"
            ) else if /i "%arch%"=="ARM" (
                set "installer_url=https://www.python.org/ftp/python/%min_python_version%/python-%min_python_version%-arm64.exe"
            ) else (
                echo Unknown architecture: %arch%. Exiting.
                pause
                exit /b 1
            )
        ) else if /i "%install_python%"=="latest" (
            if /i "%arch%"=="32-bit" (
                set "installer_url=https://www.python.org/ftp/python/latest/python-latest.exe"
            ) else if /i "%arch%"=="64-bit" (
                set "installer_url=https://www.python.org/ftp/python/latest/python-latest-amd64.exe"
            ) else if /i "%arch%"=="ARM" (
                set "installer_url=https://www.python.org/ftp/python/latest/python-latest-arm64.exe"
            ) else (
                echo Unknown architecture: %arch%. Exiting.
                pause
                exit /b 1
            )
        ) else (
            echo Invalid option. Exiting.
            pause
            exit /b 1
        )

        REM Download and install Python
        echo Downloading Python installer from %installer_url%...
        powershell -Command "Invoke-WebRequest -Uri %installer_url% -OutFile python_installer.exe"

        echo Installing Python silently...
        python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

        echo Python installed successfully. Please restart the script.
        pause
        exit /b 1
    )
)

REM Check if PIP is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo PIP is not installed. Would you like to install PIP automatically? (no/minimum/latest):
    set /p "install_pip="
    if /i "%install_pip%"=="no" (
        echo To install PIP, run: python -m ensurepip
        echo Then update PIP to the minimum version: python -m pip install --upgrade pip==%min_pip_version%
        echo Or update PIP to the latest version: python -m pip install --upgrade pip
        pause
        exit /b 1
    ) else if /i "%install_pip%"=="minimum" (
        python -m pip install --upgrade pip==%min_pip_version%
    ) else if /i "%install_pip%"=="latest" (
        python -m pip install --upgrade pip
    ) else (
        echo Invalid option. Exiting.
        pause
        exit /b 1
    )
)

REM Run setup.py to handle version checks and updates
python setup.py install

pause
