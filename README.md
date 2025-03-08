# LoadShield Script

This project is designed to alert users to upcoming load shedding events and optionally shut down the system before load shedding to prevent hardware damage. It ensures that the required Python and PIP versions are installed and up-to-date, and also supports the use of virtual environments.

## Prerequisites

- Python 3.10.11 or higher
- PIP 25.0.1 or higher

## Supported Platforms

- Windows 10/11
- Unix-based systems with supported package managers:
  - `apt-get` (Debian-based systems)
  - `yum` (CentOS, Red Hat)
  - `dnf` (Fedora)
  - `pacman` (Arch Linux)
  - `zypper` (openSUSE)

## APIs Used

- [Loadshedding API by Douglas Spear](https://loadshedding.apis.thespear.dev)
- [EskomSePush API](https://eskomsepush.gumroad.com/l/api)

## Usage

### Windows 10/11

1. **Clone or download the project.**
2. **Open Command Prompt or PowerShell.**
3. **Navigate to the project directory.**
4. **Run the start script:**

   `start-windows.bat [--use-venv]`

   - `--use-venv`: Optional argument to use a virtual environment.

### Unix-based systems (Linux, macOS)

1. **Clone or download the project.**
2. **Open Terminal.**
3. **Navigate to the project directory.**
4. **Make the start script executable:**
   1. `chmod +x start-unix.sh`
   2. If you encounter permission issues, you may need to use `sudo`:
      - `sudo chmod +x start-unix.sh`
5. **Run the start script:**
   - `./start-unix.sh [--use-venv]`
   - `--use-venv`: Optional argument to use a virtual environment.

## Start Script Functionality

1. **Check Python Installation:**
   - If Python is not installed, offer to install it automatically.
   - If Python is installed, check if the version meets the minimum required version.
   - The start scripts will handle version checks and updates if necessary.

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

## Credits

See the [CREDITS](CREDITS.md) file for a list of contributors and acknowledgments.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE.md) file for more details.

****