# LoadShield Script

This project provides a way to manage Python script execution across different platforms, ensuring that the required Python and PIP versions are installed and up-to-date. It also supports the use of virtual environments.

## Prerequisites

- Python 3.10.11 or higher
- PIP 25.0.1 or higher

## Supported Platforms

- Windows
- Unix-based systems with supported package managers:
  - `apt-get` (Debian-based systems)
  - `yum` (CentOS, Red Hat)
  - `dnf` (Fedora)
  - `pacman` (Arch Linux)
  - `zypper` (openSUSE)

## Usage

### Windows

1. **Clone or download the project.**
2. **Open Command Prompt or PowerShell.**
3. **Navigate to the project directory.**
4. **Run the start script:**

   `
   start-windows.bat [--use-venv]
   `

   - **`--use-venv`**: Optional argument to use a virtual environment.

### Unix-based systems

1. **Clone or download the project.**
2. **Open Terminal.**
3. **Navigate to the project directory.**
4. **Make the start script executable:**

   `
   chmod +x start-unix.sh
   `

5. **Run the start script:**

   `
   ./start-unix.sh [--use-venv]
   `

   - **`--use-venv`**: Optional argument to use a virtual environment.

## Script Functionality

1. **Check Python Installation:**
   - If Python is not installed, offer to install it automatically.
   - If Python is installed, check if the version meets the minimum required version.

2. **Check PIP Installation:**
   - If PIP is not installed, prompt the user to install it manually.
   - If PIP is installed, check if the version meets the minimum required version.

3. **Set Up Virtual Environment (Optional):**
   - If the `--use-venv` argument is provided, the script will set up and activate a virtual environment named `loadshield`.

4. **Install Requirements:**
   - Install the required Python packages specified in `requirements.txt`.

5. **Run the Main Script:**
   - Execute `main.py`.

6. **Deactivate Virtual Environment (Optional):**
   - If a virtual environment was used, deactivate it after `main.py` finishes execution.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

