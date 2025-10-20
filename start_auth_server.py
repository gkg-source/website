#!/usr/bin/env python3
"""
Ghar Ka Guide Authentication Server - Startup Script
This script starts the authentication server for user login/signup functionality.
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'bcrypt', 'PyJWT'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'bcrypt':
                __import__('bcrypt')
            elif package == 'PyJWT':
                __import__('jwt')
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def start_auth_server():
    """Start the authentication server"""
    print("\n🔐 Starting Ghar Ka Guide Authentication Server...")
    
    try:
        # Start the authentication server
        subprocess.run([sys.executable, 'auth_api.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Authentication server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting authentication server: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🔐 Ghar Ka Guide Authentication Server")
    print("=" * 60)
    print("This script will start your authentication server for:")
    print("• User Registration & Login")
    print("• JWT Token Management")
    print("• Profile Management")
    print("• Secure Authentication")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    print("\n📦 Checking authentication dependencies...")
    if not check_dependencies():
        return
    
    # Start server
    start_auth_server()

if __name__ == "__main__":
    main()

