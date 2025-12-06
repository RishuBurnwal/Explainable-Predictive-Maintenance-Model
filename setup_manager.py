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
import hashlib
import requests
from pathlib import Path
from urllib.parse import urljoin

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
        self.github_repo_url = "https://api.github.com/repos/RishuBurnwal/Explainable-Predictive-Maintenance-Model"
        
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
            
            # Ask if user wants to open in browser
            try:
                open_browser = input(f"{Colors.OKCYAN}Open backend in browser? (y/N): {Colors.ENDC}").strip().lower()
                if open_browser in ['y', 'yes']:
                    self.print_info("Opening backend in browser...")
                    webbrowser.open("http://localhost:5000")
                    self.print_success("Browser tab opened!")
            except:
                pass
                
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
            self.print_info("Frontend running at: http://localhost:8080")
            time.sleep(2)  # Give server time to start
            
            # Ask if user wants to open in browser
            try:
                open_browser = input(f"{Colors.OKCYAN}Open frontend in browser? (y/N): {Colors.ENDC}").strip().lower()
                if open_browser in ['y', 'yes']:
                    self.print_info("Opening frontend in browser...")
                    webbrowser.open("http://localhost:8080")
                    self.print_success("Browser tab opened!")
            except:
                pass
                
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
        self.print_info("   - Frontend UI: http://localhost:8080")
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

    def calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of a file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.print_error(f"Error calculating hash for {file_path}: {e}")
            return None

    def get_github_file_list(self):
        """Get list of files from GitHub repository"""
        try:
            # Get the default branch
            repo_response = requests.get(self.github_repo_url)
            if repo_response.status_code != 200:
                self.print_error("Failed to access repository information")
                return None
                
            default_branch = repo_response.json().get("default_branch", "main")
            
            # Get file tree
            tree_url = f"{self.github_repo_url}/git/trees/{default_branch}?recursive=1"
            response = requests.get(tree_url)
            
            if response.status_code == 200:
                tree = response.json().get("tree", [])
                # Filter only files (not directories)
                files = [item for item in tree if item.get("type") == "blob"]
                return files
            else:
                self.print_error(f"Failed to fetch file list from GitHub: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error fetching file list from GitHub: {e}")
            return None

    def download_file_from_github(self, file_path):
        """Download a file from GitHub"""
        try:
            # First try to get the default branch
            try:
                repo_response = requests.get(self.github_repo_url)
                if repo_response.status_code == 200:
                    default_branch = repo_response.json().get("default_branch", "main")
                else:
                    default_branch = "main"
            except:
                default_branch = "main"
            
            raw_url = f"https://raw.githubusercontent.com/RishuBurnwal/Explainable-Predictive-Maintenance-Model/{default_branch}/{file_path}"
            response = requests.get(raw_url)
            
            if response.status_code == 200:
                local_file_path = self.project_root / file_path
                # Create directories if they don't exist
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(local_file_path, "wb") as f:
                    f.write(response.content)
                return True
            else:
                self.print_error(f"Failed to download {file_path}: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error downloading {file_path}: {e}")
            return False

    def update_from_github(self):
        """Update missing or outdated files from GitHub"""
        self.print_info("Checking for updates from GitHub...")
        
        # Check if git is available
        git_available = self.run_command(["git", "--version"])[0]
        if git_available:
            self.print_info("Git detected. Using git pull for updates...")
            return self.update_via_git()
        
        # If git is not available, use manual file comparison
        self.print_info("Git not detected. Using manual file comparison...")
        
        github_files = self.get_github_file_list()
        if not github_files:
            self.print_error("Could not retrieve file list from GitHub")
            return False
            
        files_updated = 0
        files_added = 0
        
        for github_file in github_files:
            file_path = github_file.get("path", "")
            # Skip directories
            if not file_path or file_path.endswith("/"):
                continue
                
            local_file_path = self.project_root / file_path
            
            # If file doesn't exist locally, download it
            if not local_file_path.exists():
                self.print_info(f"Downloading missing file: {file_path}")
                if self.download_file_from_github(file_path):
                    files_added += 1
                continue
                
            # If file exists, compare content by downloading and comparing
            temp_file_path = local_file_path.with_suffix(local_file_path.suffix + ".tmp")
            try:
                if self.download_file_from_github(file_path):
                    # Compare file content
                    local_hash = self.calculate_file_hash(local_file_path)
                    temp_hash = self.calculate_file_hash(temp_file_path)
                    
                    if temp_hash and temp_hash != local_hash:
                        self.print_info(f"Updating outdated file: {file_path}")
                        # Replace local file with downloaded version
                        temp_file_path.rename(local_file_path)
                        files_updated += 1
                    else:
                        # Clean up temp file if no update needed
                        temp_file_path.unlink(missing_ok=True)
            except Exception as e:
                self.print_error(f"Error comparing {file_path}: {e}")
                if temp_file_path.exists():
                    temp_file_path.unlink(missing_ok=True)
        
        self.print_success(f"Update complete! Added {files_added} files, updated {files_updated} files.")
        return True

    def update_via_git(self):
        """Update using git pull"""
        try:
            self.print_info("Fetching latest changes...")
            success, stdout, stderr = self.run_command(["git", "fetch"], cwd=self.project_root)
            if not success:
                self.print_error(f"Failed to fetch: {stderr}")
                return False
                
            self.print_info("Pulling latest changes...")
            success, stdout, stderr = self.run_command(["git", "pull"], cwd=self.project_root)
            if success:
                self.print_success("Repository updated successfully!")
                print(stdout)
                return True
            else:
                self.print_error(f"Failed to pull updates: {stderr}")
                return False
        except Exception as e:
            self.print_error(f"Error during git update: {e}")
            return False

    def show_main_menu(self):
        """Show the main menu - now automatically detects platform"""
        # Auto-detect platform and go directly to options menu
        self.platform = platform.system().lower()
        self.show_options_menu()

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
{Colors.OKCYAN}6.{Colors.ENDC} Check System Requirements
{Colors.OKCYAN}7.{Colors.ENDC} Update from GitHub
{Colors.OKCYAN}0.{Colors.ENDC} Exit

Choose option (0-7): """

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
                self.check_system_requirements()
            elif choice == "7":
                self.update_from_github()
            elif choice == "0":
                self.print_info("Goodbye!")
                sys.exit(0)
            else:
                self.print_error("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

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