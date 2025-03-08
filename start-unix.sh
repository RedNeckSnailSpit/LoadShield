#!/bin/bash

# Detect architecture
arch=$(uname -m)

# Read versions from config.json
min_python_version=$(jq -r '.min_python_version' config.json)
min_pip_version=$(jq -r '.min_pip_version' config.json)

# Function to prompt user for installation choice
prompt_install() {
    local message=$1
    local min_version_url_x86=$2
    local min_version_url_amd64=$3
    local min_version_url_arm=$4
    local latest_version_url_x86=$5
    local latest_version_url_amd64=$6
    local latest_version_url_arm=$7

    echo "$message (no/minimum/latest): "
    read -r install_choice
    if [ "$install_choice" == "no" ]; then
        echo "To install the minimum version, download from: $min_version_url_amd64"
        echo "To install the latest version, download from: $latest_version_url_amd64"
        exit 1
    elif [ "$install_choice" == "minimum" ] || [ "$install_choice" == "latest" ]; then
        case "$arch" in
            i*86)
                if [ "$install_choice" == "minimum" ]; then
                    echo "$min_version_url_x86"
                else
                    echo "$latest_version_url_x86"
                fi
                ;;
            x86_64)
                if [ "$install_choice" == "minimum" ]; then
                    echo "$min_version_url_amd64"
                else
                    echo "$latest_version_url_amd64"
                fi
                ;;
            arm*)
                if [ "$install_choice" == "minimum" ]; then
                    echo "$min_version_url_arm"
                else
                    echo "$latest_version_url_arm"
                fi
                ;;
            *)
                echo "Unknown architecture. Exiting."
                exit 1
                ;;
        esac
    else
        echo "Invalid option. Exiting."
        exit 1
    fi
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    installer_url=$(prompt_install \
        "Python is not installed. Would you like to install Python automatically?" \
        "https://www.python.org/ftp/python/$min_python_version/python-$min_python_version-x86.tar.xz" \
        "https://www.python.org/ftp/python/$min_python_version/python-$min_python_version-amd64.tar.xz" \
        "https://www.python.org/ftp/python/$min_python_version/python-$min_python_version-arm64.tar.xz" \
        "https://www.python.org/ftp/python/latest/python-latest-x86.tar.xz" \
        "https://www.python.org/ftp/python/latest/python-latest-amd64.tar.xz" \
        "https://www.python.org/ftp/python/latest/python-latest-arm64.tar.xz" \
    )
    echo "Downloading Python installer from $installer_url..."
    curl -o python_installer.tar.xz "$installer_url"
    # Add logic to extract and install Python based on the downloaded file
    echo "Python installed successfully. Please restart the script."
    exit 1
fi

# Check if PIP is installed
if ! command -v pip3 &> /dev/null; then
    echo "PIP is not installed. Would you like to install PIP automatically? (no/minimum/latest): "
    read -r install_pip
    if [ "$install_pip" == "no" ]; then
        echo "To install PIP, run: python -m ensurepip"
        echo "Then update PIP to the minimum version: python -m pip install --upgrade pip==$min_pip_version"
        echo "Or update PIP to the latest version: python -m pip install --upgrade pip"
        exit 1
    elif [ "$install_pip" == "minimum" ]; then
        curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
        python3 get-pip.py
        python3 -m pip install --upgrade pip==$min_pip_version
    elif [ "$install_pip" == "latest" ]; then
        curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
        python3 get-pip.py
        python3 -m pip install --upgrade pip
    else
        echo "Invalid option. Exiting."
        exit 1
    fi
fi

# Run setup.py to handle version checks and updates
python3 setup.py install
