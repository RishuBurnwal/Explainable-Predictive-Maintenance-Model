#!/usr/bin/env python3
"""
Explainable Predictive Maintenance - Universal Setup Manager
A unified setup script for both Windows and Linux platforms
"""

import os
import sys
import subprocess
import platform
import json
import time
import webbrowser
from pathlib import Path

class Colors:
    """Console colors for better output formatting"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SetupManager:
    def __init__(self):
        self.platform = platform.system().lower()
        self.project_root = Path(__file__).parent.absolute()
        self.frontend_path = self.project_root / "FrontEnd"
        self.backend_path = self.project_root / "Backend"
        
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Explainable Predictive Maintenance                        ║
║                         Universal Setup Manager                             ║
║                                                                              ║
║               Platform: {self.platform.capitalize().ljust(20)}                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
        print(banner)

    def print_colored(self, message, color=Colors.OKGREEN):
        """Print colored message"""
        print(f"{color}{message}{Colors.ENDC}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

    def print_success(self, message):
        """Print success message"""
        print(f"{Colors.OKGREEN}[SUCCESS] {message}{Colors.ENDC}")

    def print_info(self, message):
        """Print info message"""
        print(f"{Colors.OKBLUE}[INFO] {message}{Colors.ENDC}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Colors.WARNING}[WARNING] {message}{Colors.ENDC}")

    def run_command(self, command, cwd=None, shell=True):
        """Execute a system command"""
        try:
            if isinstance(command, list):
                result = subprocess.run(command, cwd=cwd, shell=shell, 
                                      capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(command, cwd=cwd, shell=shell, 
                                      capture_output=True, text=True, check=True)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)

    def check_python(self):
        """Check if Python is installed"""
        success, stdout, stderr = self.run_command([sys.executable, "--version"])
        if success:
            version = stdout.strip()
            self.print_success(f"Python found: {version}")
            return True
        else:
            self.print_error("Python not found or not working properly")
            return False

    def check_node(self):
        """Check if Node.js is installed"""
        success, stdout, stderr = self.run_command(["node", "--version"], shell=True)
        if success:
            version = stdout.strip()
            self.print_success(f"Node.js found: {version}")
            return True
        else:
            self.print_error("Node.js not found. Please install Node.js 16+ from https://nodejs.org/")
            self.print_warning("After installation, restart your terminal and try again.")
            return False

    def check_npm(self):
        """Check if npm is installed"""
        success, stdout, stderr = self.run_command(["npm", "--version"], shell=True)
        if success:
            version = stdout.strip()
            self.print_success(f"npm found: {version}")
            return True
        else:
            self.print_error("npm not found")
            self.print_warning("npm comes with Node.js. Please install Node.js from https://nodejs.org/")
            return False

    def create_venv(self):
        """Create Python virtual environment"""
        venv_path = self.backend_path / "venv"
        
        if venv_path.exists():
            self.print_info("Virtual environment already exists")
            return True
            
        self.print_info("Creating Python virtual environment...")
        success, stdout, stderr = self.run_command([
            sys.executable, "-m", "venv", str(venv_path)
        ], cwd=self.backend_path)
        
        if success:
            self.print_success("Virtual environment created successfully")
            return True
        else:
            self.print_error(f"Failed to create virtual environment: {stderr}")
            return False

    def get_activate_command(self):
        """Get the activation command for the virtual environment"""
        venv_path = self.backend_path / "venv"
        if self.platform == "windows":
            return str(venv_path / "Scripts" / "activate.bat")
        else:
            return f"source {venv_path / 'bin' / 'activate'}"

    def install_python_deps(self):
        """Install Python dependencies"""
        self.print_info("Installing Python dependencies...")
        
        venv_path = self.backend_path / "venv"
        if self.platform == "windows":
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"
        
        # Upgrade pip first
        success, stdout, stderr = self.run_command([
            str(pip_exe), "install", "--upgrade", "pip"
        ], cwd=self.backend_path)
        
        if not success:
            self.print_warning("Failed to upgrade pip, continuing anyway...")
        
        # Install requirements
        success, stdout, stderr = self.run_command([
            str(pip_exe), "install", "-r", "requirements.txt"
        ], cwd=self.backend_path)
        
        if success:
            self.print_success("Python dependencies installed successfully")
            return True
        else:
            self.print_error(f"Failed to install Python dependencies: {stderr}")
            return False

    def install_node_deps(self):
        """Install Node.js dependencies"""
        self.print_info("Installing Node.js dependencies...")
        
        success, stdout, stderr = self.run_command([
            "npm", "install"
        ], cwd=self.frontend_path)
        
        if success:
            self.print_success("Node.js dependencies installed successfully")
            return True
        else:
            self.print_error(f"Failed to install Node.js dependencies: {stderr}")
            return False

    def start_backend(self):
        """Start the backend server in a new window"""
        self.print_info("Starting backend server in new window...")
        
        try:
            if self.platform == "windows":
                # Use dedicated backend window batch file
                window_batch_file = self.project_root / "start_backend_window.bat"
                if window_batch_file.exists():
                    # Start backend in new window using dedicated batch file
                    subprocess.Popen([
                        "cmd", "/c", "start", "cmd", "/k", str(window_batch_file)
                    ], shell=True)
                else:
                    # Fallback to original method
                    batch_file = self.backend_path / "start_server.bat"
                    if batch_file.exists():
                        subprocess.Popen([
                            "cmd", "/c", "start", "cmd", "/k", 
                            f"cd /d {self.backend_path} && {batch_file}"
                        ], shell=True)
                    else:
                        # Direct Python execution in new window
                        venv_path = self.backend_path / "venv"
                        python_exe = venv_path / "Scripts" / "python.exe"
                        subprocess.Popen([
                            "cmd", "/c", "start", "cmd", "/k",
                            f"cd /d {self.backend_path} && {python_exe} app.py"
                        ], shell=True)
            else:
                # Linux/macOS - use terminal/gnome-terminal/xterm
                shell_script = self.backend_path / "start_server.sh"
                if shell_script.exists():
                    # Try different terminal emulators
                    terminal_commands = [
                        ["gnome-terminal", "--", "bash", str(shell_script)],
                        ["xterm", "-e", "bash", str(shell_script)],
                        ["terminal", "-e", "bash", str(shell_script)],
                    ]
                    for cmd in terminal_commands:
                        try:
                            subprocess.Popen(cmd, cwd=self.backend_path)
                            break
                        except FileNotFoundError:
                            continue
                    else:
                        # Fallback to background process
                        subprocess.Popen(["bash", str(shell_script)], cwd=self.backend_path)
                else:
                    # Fallback to direct Python execution
                    venv_path = self.backend_path / "venv"
                    python_exe = venv_path / "bin" / "python"
                    subprocess.Popen([str(python_exe), "app.py"], cwd=self.backend_path)
            
            self.print_success("Backend server started in new window!")
            self.print_info("Backend running at: http://localhost:5000")
            time.sleep(2)  # Give server time to start
            return True
            
        except Exception as e:
            self.print_error(f"Failed to start backend server: {e}")
            return False

    def start_frontend(self):
        """Start the frontend development server in a new window"""
        self.print_info("Starting frontend development server in new window...")
        
        try:
            # Check if npm is available
            npm_check = subprocess.run(["npm", "--version"], 
                                     capture_output=True, text=True, shell=True)
            if npm_check.returncode != 0:
                self.print_error("npm not found. Please install Node.js from https://nodejs.org/")
                return False
            
            # Check if node_modules exists
            node_modules = self.frontend_path / "node_modules"
            if not node_modules.exists():
                self.print_info("Installing frontend dependencies...")
                install_result = subprocess.run(["npm", "install"], 
                                               cwd=self.frontend_path, shell=True)
                if install_result.returncode != 0:
                    self.print_error("Failed to install frontend dependencies")
                    return False
            
            # Start the development server in a new window
            if self.platform == "windows":
                # Use dedicated frontend window batch file
                window_batch_file = self.project_root / "start_frontend_window.bat"
                if window_batch_file.exists():
                    # Start frontend in new window using dedicated batch file
                    subprocess.Popen([
                        "cmd", "/c", "start", "cmd", "/k", str(window_batch_file)
                    ], shell=True)
                else:
                    # Fallback to direct command
                    subprocess.Popen([
                        "cmd", "/c", "start", "cmd", "/k",
                        f"cd /d {self.frontend_path} && npm run dev"
                    ], shell=True)
            else:
                # Linux/macOS - use terminal emulators
                terminal_commands = [
                    ["gnome-terminal", "--", "bash", "-c", f"cd {self.frontend_path} && npm run dev"],
                    ["xterm", "-e", f"cd {self.frontend_path} && npm run dev"],
                    ["terminal", "-e", f"cd {self.frontend_path} && npm run dev"],
                ]
                for cmd in terminal_commands:
                    try:
                        subprocess.Popen(cmd)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    # Fallback to background process
                    subprocess.Popen(["npm", "run", "dev"], cwd=self.frontend_path, shell=True)
            
            self.print_success("Frontend development server started in new window!")
            self.print_info("Frontend running at: http://localhost:5173")
            time.sleep(2)  # Give server time to start
            return True
            
        except FileNotFoundError:
            self.print_error("Node.js/npm not found. Please install Node.js from https://nodejs.org/")
            self.print_info("After installing Node.js, restart your terminal and try again.")
            return False
        except Exception as e:
            self.print_error(f"Failed to start frontend server: {e}")
            return False

    def start_both_servers(self):
        """Start both frontend and backend servers simultaneously"""
        self.print_info("Starting both frontend and backend servers...")
        print()
        
        # Start backend first
        self.print_info("Starting backend server...")
        backend_success = self.start_backend()
        
        if not backend_success:
            self.print_error("Failed to start backend server. Aborting.")
            return False
        
        # Wait a moment for backend to initialize
        self.print_info("Waiting for backend to initialize...")
        time.sleep(3)
        
        # Start frontend
        self.print_info("Starting frontend server...")
        frontend_success = self.start_frontend()
        
        if not frontend_success:
            self.print_error("Backend started but frontend failed to start.")
            return False
        
        # Final success message
        print()
        self.print_success("Both servers started successfully!")
        print()
        self.print_info("Available services:")
        self.print_info("   - Backend API: http://localhost:5000")
        self.print_info("   - Frontend UI: http://localhost:5173")
        print()
        
        # Option to open both in browser
        try:
            open_browser = input(f"{Colors.OKCYAN}Open both services in browser? (y/N): {Colors.ENDC}").strip().lower()
            if open_browser in ['y', 'yes']:
                self.print_info("Opening services in browser...")
                webbrowser.open("http://localhost:5000")
                time.sleep(1)
                webbrowser.open("http://localhost:5173")
                self.print_success("Browser tabs opened!")
        except KeyboardInterrupt:
            print()
            
        return True

    def test_api(self):
        """Test the API endpoints"""
        self.print_info("Testing API endpoints...")
        
        try:
            # Run the test script
            venv_path = self.backend_path / "venv"
            if self.platform == "windows":
                python_exe = venv_path / "Scripts" / "python.exe"
            else:
                python_exe = venv_path / "bin" / "python"
            
            success, stdout, stderr = self.run_command([
                str(python_exe), "test_api.py"
            ], cwd=self.backend_path)
            
            if success:
                self.print_success("API tests completed successfully!")
                print(stdout)
                return True
            else:
                self.print_error(f"API tests failed: {stderr}")
                print(stdout)
                return False
                
        except Exception as e:
            self.print_error(f"Failed to run API tests: {e}")
            return False

    def complete_setup(self):
        """Run complete setup process"""
        self.print_info("Running complete setup process...")
        
        steps = [
            ("Checking Python installation", self.check_python),
            ("Checking Node.js installation", self.check_node),
            ("Checking npm installation", self.check_npm),
            ("Creating virtual environment", self.create_venv),
            ("Installing Python dependencies", self.install_python_deps),
            ("Installing Node.js dependencies", self.install_node_deps),
        ]
        
        for step_name, step_func in steps:
            self.print_info(f"Step: {step_name}")
            if not step_func():
                self.print_error(f"Setup failed at step: {step_name}")
                return False
            print()
        
        self.print_success("Complete setup finished successfully!")
        self.print_info("You can now use other options to start frontend, backend, or test API")
        return True

    def installation_guide(self):
        """Show installation guide"""
        guide = f"""
{Colors.HEADER}{Colors.BOLD}Installation Guide{Colors.ENDC}

{Colors.OKBLUE}Prerequisites:{Colors.ENDC}
1. Python 3.8+ (Download from: https://python.org)
2. Node.js 16+ (Download from: https://nodejs.org)
3. Git (Download from: https://git-scm.com)

{Colors.OKBLUE}Platform-specific notes:{Colors.ENDC}

{Colors.BOLD}Windows:{Colors.ENDC}
- Make sure Python and Node.js are added to PATH
- You may need to run as Administrator for some operations
- Use PowerShell or Command Prompt

{Colors.BOLD}Linux/macOS:{Colors.ENDC}
- Make sure you have build tools installed
- On Ubuntu/Debian: sudo apt install python3-venv python3-dev build-essential
- On macOS: Install Xcode Command Line Tools

{Colors.OKBLUE}Quick Start:{Colors.ENDC}
1. Select 'Complete Setup' to install all dependencies
2. Select 'Start Backend' to run the API server
3. Select 'Start Frontend' to run the web interface
4. Select 'Test API' to verify everything is working

{Colors.OKBLUE}Manual Setup:{Colors.ENDC}
Backend:
  cd Backend
  python -m venv venv
  {self.get_activate_command()}
  pip install -r requirements.txt
  python app.py

Frontend:
  cd FrontEnd
  npm install
  npm run dev

{Colors.OKBLUE}Troubleshooting:{Colors.ENDC}
- If you get permission errors, try running as administrator/sudo
- If ports are busy, check if services are already running
- For Node.js issues, try clearing npm cache: npm cache clean --force
- For Python issues, try recreating the virtual environment
"""
        print(guide)

    def show_main_menu(self):
        """Show the main menu"""
        while True:
            self.print_banner()
            
            menu = f"""
{Colors.OKBLUE}{Colors.BOLD}Select Platform:{Colors.ENDC}
{Colors.OKCYAN}1.{Colors.ENDC} Windows
{Colors.OKCYAN}2.{Colors.ENDC} Linux
{Colors.OKCYAN}3.{Colors.ENDC} Auto-detect ({self.platform.capitalize()})
{Colors.OKCYAN}4.{Colors.ENDC} Exit

Choose option (1-4): """

            choice = input(menu).strip()
            
            if choice == "1":
                self.platform = "windows"
                self.show_options_menu()
            elif choice == "2":
                self.platform = "linux"
                self.show_options_menu()
            elif choice == "3":
                self.show_options_menu()
            elif choice == "4":
                self.print_info("Goodbye!")
                sys.exit(0)
            else:
                self.print_error("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def show_options_menu(self):
        """Show the options menu"""
        while True:
            # Refresh platform detection
            self.platform = platform.system().lower()
            self.print_banner()
            self.print_info(f"Platform: {self.platform.capitalize()}")
            
            menu = f"""
{Colors.OKBLUE}{Colors.BOLD}Available Options:{Colors.ENDC}
{Colors.OKCYAN}1.{Colors.ENDC} Start Frontend Development Server
{Colors.OKCYAN}2.{Colors.ENDC} Start Backend API Server
{Colors.OKCYAN}3.{Colors.ENDC} Run Both Frontend & Backend
{Colors.OKCYAN}4.{Colors.ENDC} Test API Endpoints
{Colors.OKCYAN}5.{Colors.ENDC} Complete Setup (Install Dependencies)
{Colors.OKCYAN}6.{Colors.ENDC} Installation Guide
{Colors.OKCYAN}7.{Colors.ENDC} Open Frontend in Browser
{Colors.OKCYAN}8.{Colors.ENDC} Open Backend API in Browser
{Colors.OKCYAN}9.{Colors.ENDC} Check System Requirements
{Colors.OKCYAN}10.{Colors.ENDC} Back to Platform Selection
{Colors.OKCYAN}0.{Colors.ENDC} Exit

Choose option (0-10): """

            choice = input(menu).strip()
            
            if choice == "1":
                self.start_frontend()
            elif choice == "2":
                self.start_backend()
            elif choice == "3":
                self.start_both_servers()
            elif choice == "4":
                self.test_api()
            elif choice == "5":
                self.complete_setup()
            elif choice == "6":
                self.installation_guide()
            elif choice == "7":
                self.print_info("Opening frontend in browser...")
                webbrowser.open("http://localhost:5173")
            elif choice == "8":
                self.print_info("Opening backend API in browser...")
                webbrowser.open("http://localhost:5000")
            elif choice == "9":
                self.check_system_requirements()
            elif choice == "10":
                break
            elif choice == "0":
                self.print_info("Goodbye!")
                sys.exit(0)
            else:
                self.print_error("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

    def check_system_requirements(self):
        """Check system requirements"""
        self.print_info("Checking system requirements...")
        print()
        
        # Check Python
        python_ok = self.check_python()
        
        # Check Node.js
        node_ok = self.check_node()
        
        # Check npm
        npm_ok = self.check_npm()
        
        # Check Git
        git_success, git_stdout, _ = self.run_command(["git", "--version"], shell=True)
        if git_success:
            self.print_success(f"Git found: {git_stdout.strip()}")
        else:
            self.print_warning("Git not found (optional but recommended)")
        
        # Check project structure
        frontend_exists = self.frontend_path.exists()
        backend_exists = self.backend_path.exists()
        
        if frontend_exists:
            self.print_success("Frontend directory found")
            # Check if node_modules exists
            node_modules = self.frontend_path / "node_modules"
            if node_modules.exists():
                self.print_success("Frontend dependencies installed")
            else:
                self.print_warning("Frontend dependencies not installed (will install automatically)")
        else:
            self.print_error("Frontend directory not found")
            
        if backend_exists:
            self.print_success("Backend directory found")
            # Check if venv exists
            venv_path = self.backend_path / "venv"
            if venv_path.exists():
                self.print_success("Python virtual environment found")
            else:
                self.print_warning("Python virtual environment not found (will create automatically)")
        else:
            self.print_error("Backend directory not found")
        
        # Summary
        print()
        if python_ok and node_ok and npm_ok and frontend_exists and backend_exists:
            self.print_success("All requirements met! You can proceed with setup.")
        else:
            self.print_warning("Some requirements are missing.")
            if not node_ok or not npm_ok:
                self.print_info("Please install Node.js from: https://nodejs.org/")
                self.print_info("Check NODEJS_INSTALLATION_GUIDE.md for detailed instructions")
            self.print_info("Run system check again after installing missing requirements")

def main():
    """Main entry point"""
    try:
        manager = SetupManager()
        manager.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}An error occurred: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
