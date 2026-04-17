#!/usr/bin/env python3
"""
TruthLens AI Scan - Master Setup & Installation Script
Handles complete setup for beginners
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_command(cmd):
    """Check if command is available"""
    return subprocess.run(['which' if platform.system() != 'Windows' else 'where', cmd],
                         capture_output=True).returncode == 0

def run_command(cmd, description=""):
    """Run shell command"""
    if description:
        print(f"{Colors.YELLOW}→ {description}{Colors.END}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print_error(f"Failed to run command: {e}")
        return False

def setup_backend():
    """Setup backend"""
    print_header("Setting Up Backend")
    
    os.chdir('backend')
    
    # Create virtual environment
    print_info("Creating Python virtual environment...")
    venv_name = 'venv'
    if not os.path.exists(venv_name):
        if not run_command(f'{sys.executable} -m venv {venv_name}', 'Creating virtual environment'):
            print_error("Failed to create virtual environment")
            return False
        print_success("Virtual environment created")
    else:
        print_info("Virtual environment already exists")
    
    # Activate and install dependencies
    if platform.system() == 'Windows':
        activate_cmd = f'{venv_name}\\Scripts\\activate.bat && pip install -r requirements.txt'
    else:
        activate_cmd = f'source {venv_name}/bin/activate && pip install -r requirements.txt'
    
    print_info("Installing Python dependencies (this may take a few minutes)...")
    if not run_command(activate_cmd, 'Installing dependencies'):
        print_error("Failed to install dependencies")
        return False
    print_success("Dependencies installed")
    
    # Create model
    print_info("Creating initial model...")
    if not run_command(f'{sys.executable} create_model.py', 'Initializing model'):
        print_error("Failed to create model")
        return False
    print_success("Model created")
    
    os.chdir('..')
    return True

def setup_frontend():
    """Setup frontend"""
    print_header("Setting Up Frontend")
    
    os.chdir('frontend')
    
    print_info("Installing Node.js dependencies (this may take a few minutes)...")
    if not run_command('npm install', 'Installing npm dependencies'):
        print_error("Failed to install npm dependencies")
        return False
    print_success("Dependencies installed")
    
    os.chdir('..')
    return True

def verify_setup():
    """Verify installation"""
    print_header("Verifying Setup")
    
    checks = {
        'Python': check_command('python') or check_command('python3'),
        'Node.js': check_command('node'),
        'npm': check_command('npm'),
    }
    
    all_ok = True
    for tool, available in checks.items():
        if available:
            print_success(f"{tool} is available")
        else:
            print_error(f"{tool} is NOT available")
            all_ok = False
    
    # Check directories
    required_dirs = [
        'frontend',
        'backend',
        'models',
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_success(f"Directory {dir_name}/ exists")
        else:
            print_error(f"Directory {dir_name}/ NOT found")
            all_ok = False
    
    return all_ok

def print_next_steps():
    """Print next steps"""
    print_header("Setup Complete! 🎉")
    print(f"{Colors.GREEN}TruthLens AI Scan is ready to run!{Colors.END}\n")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.END}\n")
    
    if platform.system() == 'Windows':
        print("1. Terminal 1 - Start Backend:")
        print(f"   {Colors.YELLOW}cd backend{Colors.END}")
        print(f"   {Colors.YELLOW}venv\\Scripts\\activate{Colors.END}")
        print(f"   {Colors.YELLOW}python app.py{Colors.END}\n")
        
        print("2. Terminal 2 - Start Frontend:")
        print(f"   {Colors.YELLOW}cd frontend{Colors.END}")
        print(f"   {Colors.YELLOW}npm run dev{Colors.END}\n")
    else:
        print("1. Terminal 1 - Start Backend:")
        print(f"   {Colors.YELLOW}cd backend{Colors.END}")
        print(f"   {Colors.YELLOW}source venv/bin/activate{Colors.END}")
        print(f"   {Colors.YELLOW}python app.py{Colors.END}\n")
        
        print("2. Terminal 2 - Start Frontend:")
        print(f"   {Colors.YELLOW}cd frontend{Colors.END}")
        print(f"   {Colors.YELLOW}npm run dev{Colors.END}\n")
    
    print("3. Open Browser:")
    print(f"   {Colors.YELLOW}http://localhost:3000{Colors.END}\n")
    
    print(f"{Colors.GREEN}Have fun detecting deepfakes! 🔍{Colors.END}\n")

def main():
    """Main setup function"""
    print_header("TruthLens AI Scan - Setup")
    
    print_info("This script will set up TruthLens AI Scan for local development")
    print_info("It will install all necessary dependencies\n")
    
    # Check prerequisites
    print_header("Checking Prerequisites")
    
    if not check_command('python') and not check_command('python3'):
        print_error("Python not found. Please install Python 3.8+")
        return False
    print_success("Python is available")
    
    if not check_command('node'):
        print_error("Node.js not found. Please install Node.js 16+")
        return False
    print_success("Node.js is available")
    
    if not check_command('npm'):
        print_error("npm not found. Please install npm")
        return False
    print_success("npm is available")
    
    # Setup
    print("\n")
    if not setup_backend():
        print_error("Backend setup failed")
        return False
    
    if not setup_frontend():
        print_error("Frontend setup failed")
        return False
    
    # Verify
    if not verify_setup():
        print_error("Some checks failed, but setup may still work")
    
    # Next steps
    print_next_steps()
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
