#!/bin/bash

# Function to compare versions
version_ge() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" == "$2" ]
}

# Detect package manager
PACKAGE_MANAGER="unknown"
if command -v apt-get &> /dev/null; then
    PACKAGE_MANAGER="apt-get"
    PYTHON_INSTALL_CMD="sudo apt-get install -y python3"
elif command -v yum &> /dev/null; then
    PACKAGE_MANAGER="yum"
    PYTHON_INSTALL_CMD="sudo yum install -y python3"
elif command -v dnf &> /dev/null; then
    PACKAGE_MANAGER="dnf"
    PYTHON_INSTALL_CMD="sudo dnf install -y python3"
elif command -v pacman &> /dev/null; then
    PACKAGE_MANAGER="pacman"
    PYTHON_INSTALL_CMD="sudo pacman -Syu python"
elif command -v zypper &> /dev/null; then
    PACKAGE_MANAGER="zypper"
    PYTHON_INSTALL_CMD="sudo zypper install -y python3"
fi

# Read config.ini for minimum version requirements
MIN_PYTHON_VERSION=$(grep -oP 'min_python_version\s*=\s*\K.*' config.ini)
MIN_PIP_VERSION=$(grep -oP 'min_pip_version\s*=\s*\K.*' config.ini)

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Would you like to install Python automatically? (no/minimum/latest)"
    read -r install_python
    if [ "$install_python" == "no" ]; then
        echo "To install the minimum version, run: $PYTHON_INSTALL_CMD"
        echo "To install the latest version, run: $PYTHON_INSTALL_CMD"
        exit 1
    elif [ "$install_python" == "minimum" ]; then
        $PYTHON_INSTALL_CMD
    elif [ "$install_python" == "latest" ]; then
        $PYTHON_INSTALL_CMD
    else
        echo "Invalid option. Exiting."
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python3 -V 2>&1 | awk '{print $2}')
if ! version_ge "$PYTHON_VERSION" "$MIN_PYTHON_VERSION"; then
    echo "Python version $PYTHON_VERSION is installed. Minimum required version is $MIN_PYTHON_VERSION."
    if [ "$PACKAGE_MANAGER" != "unknown" ]; then
        echo "Would you like to update Python? (no/minimum/latest)"
        read -r update_python
        if [ "$update_python" == "no" ]; then
            echo "To update Python to the minimum version, run: $PYTHON_INSTALL_CMD"
            echo "To update Python to the latest version, run: $PYTHON_INSTALL_CMD"
            exit 1
        elif [ "$update_python" == "minimum" ]; then
            $PYTHON_INSTALL_CMD
        elif [ "$update_python" == "latest" ]; then
            $PYTHON_INSTALL_CMD
        else
            echo "Invalid option. Exiting."
            exit 1
        fi
    else
        echo "Unknown package manager. Please update Python manually."
        exit 1
    fi
fi

# Check if PIP is installed
if ! command -v pip3 &> /dev/null; then
    echo "PIP3 is not installed. Please install PIP3 to continue."
    exit 1
fi

# Check PIP version
PIP_VERSION=$(pip3 -V | awk '{print $2}')
if ! version_ge "$PIP_VERSION" "$MIN_PIP_VERSION"; then
    echo "PIP version $PIP_VERSION is installed. Minimum required version is $MIN_PIP_VERSION."
    echo "Would you like to update PIP? (no/minimum/latest)"
    read -r update_pip
    if [ "$update_pip" == "no" ]; then
        echo "To update PIP to the minimum version, run: python3 -m pip install --upgrade pip==\"$MIN_PIP_VERSION\""
        echo "To update PIP to the latest version, run: python3 -m pip install --upgrade pip"
        exit 1
    elif [ "$update_pip" == "minimum" ]; then
        python3 -m pip install --upgrade pip=="$MIN_PIP_VERSION"
    elif [ "$update_pip" == "latest" ]; then
        python3 -m pip install --upgrade pip
    else
        echo "Invalid option. Exiting."
        exit 1
    fi
fi

# Check if --use-venv argument is provided
use_venv=false
for arg in "$@"; do
    if [ "$arg" == "--use-venv" ]; then
        use_venv=true
        break
    fi
done

# Setup virtual environment if required
if [ "$use_venv" == "true" ]; then
    if [ ! -d "loadshield" ]; then
        echo "Creating virtual environment..."
        python3 -m venv loadshield
    fi

    echo "Activating virtual environment..."
    source loadshield/bin/activate
fi

# Install requirements
pip3 install -r requirements.txt

# Run main.py
python3 main.py

# Deactivate virtual environment if used
if [ "$use_venv" == "true" ]; then
    deactivate
fi
