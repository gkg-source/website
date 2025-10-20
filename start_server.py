#!/usr/bin/env python3
"""
Ghar Ka Guide Financial Platform - Startup Script
This script helps you start the Python backend server for your financial tools.
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
        'flask', 'flask-cors', 'pandas', 'numpy', 'scipy', 'yfinance'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
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

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Ghar Ka Guide Financial API Server...")
    
    try:
        # Start the Flask server
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🏠 Ghar Ka Guide Financial Platform")
    print("=" * 60)
    print("This script will start your Python backend server for:")
    print("• Investment Analysis & Portfolio Optimization")
    print("• Budget Optimization & Financial Planning")
    print("• AI Financial Assistant (Chatbot)")
    print("• Real-time Financial Calculations")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()

