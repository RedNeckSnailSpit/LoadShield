import os
import sys
import json
import subprocess
import platform
from setuptools import setup, find_packages

def load_config():
    with open("config.json") as config_file:
        return json.load(config_file)

def check_version(current_version, min_version):
    return tuple(map(int, current_version.split('.'))) >= tuple(map(int, min_version.split('.')))

def update_python_windows(min_version):
    print("Would you like to update Python? (no/minimum/latest)")
    update_choice = input().lower()
    if update_choice == 'no':
        print(f"To update manually, download the minimum version here: https://www.python.org/ftp/python/{min_version}/python-{min_version}-amd64.exe")
        print("Or download the latest version here: https://www.python.org/ftp/python/latest/python-latest-amd64.exe")
        sys.exit(1)
    elif update_choice in ('minimum', 'latest'):
        if update_choice == 'minimum':
            version = min_version
        else:
            version = "latest"
        installer_url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
        subprocess.run(['powershell', '-Command', f'Invoke-WebRequest -Uri {installer_url} -OutFile python_installer.exe'])
        subprocess.run(['python_installer.exe', '/quiet', 'InstallAllUsers=1', 'PrependPath=1'])
        print("Python updated successfully. Please restart the setup.")
        sys.exit(1)
    else:
        print("Invalid option. Exiting.")
        sys.exit(1)

def update_pip_windows(min_version):
    print("Updating PIP...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', f'pip=={min_version}'])

def update_python_unix(min_version):
    package_manager = detect_package_manager()
    if package_manager == "unknown":
        print("Unknown package manager. Please update Python manually.")
        sys.exit(1)
    print("Would you like to update Python? (no/minimum/latest)")
    update_choice = input().lower()
    if update_choice == 'no':
        print(f"To update manually, use your package manager to install Python {min_version} or higher.")
        sys.exit(1)
    elif update_choice in ('minimum', 'latest'):
        command = get_update_command(package_manager, "python3", update_choice, min_version)
        os.system(command)
        print("Python updated successfully. Please restart the setup.")
        sys.exit(1)
    else:
        print("Invalid option. Exiting.")
        sys.exit(1)

def update_pip_unix(min_version):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', f'pip=={min_version}'])

def detect_package_manager():
    if os.system("command -v apt-get > /dev/null 2>&1") == 0:
        return "apt-get"
    elif os.system("command -v yum > /dev/null 2>&1") == 0:
        return "yum"
    elif os.system("command -v dnf > /dev/null 2>&1") == 0:
        return "dnf"
    elif os.system("command -v pacman > /dev/null 2>&1") == 0:
        return "pacman"
    elif os.system("command -v zypper > /dev/null 2>&1") == 0:
        return "zypper"
    else:
        return "unknown"

def get_update_command(package_manager, package, update_choice, min_version):
    if package_manager in ("apt-get", "yum", "dnf"):
        if update_choice == 'minimum':
            return f"sudo {package_manager} install -y {package}={min_version}"
        else:
            return f"sudo {package_manager} install -y {package}"
    elif package_manager == "pacman":
        return f"sudo pacman -Syu {package}"
    elif package_manager == "zypper":
        return f"sudo zypper install -y {package}"
    else:
        return ""

# Load configuration
config = load_config()
min_python_version = config["min_python_version"]
min_pip_version = config["min_pip_version"]

# Check Python version
current_python_version = platform.python_version()
if not check_version(current_python_version, min_python_version):
    print(f"Python {min_python_version} or higher is required.")
    if platform.system() == "Windows":
        update_python_windows(min_python_version)
    else:
        update_python_unix(min_python_version)

# Check PIP version
try:
    import pip
    current_pip_version = pip.__version__
    if not check_version(current_pip_version, min_pip_version):
        print(f"PIP {min_pip_version} or higher is required.")
        if platform.system() == "Windows":
            update_pip_windows(min_pip_version)
        else:
            update_pip_unix(min_pip_version)
except ImportError:
    print("PIP is not installed. Updating PIP...")
    update_pip_unix(min_pip_version)

setup(
    name="LoadShield",
    version="0.1.0",
    author="Douglas Spear",
    author_email="douglas@thespear.dev",
    description="An app that notifies users of upcoming load shedding events and automatically shuts down the system if the user is not present, ensuring safety and preventing hardware damage.",
    url="https://github.com/RedNeckSnailSpit/LoadShield",
    packages=find_packages(),
    install_requires=[
        "requests==2.25.1",
        "Flask==2.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
