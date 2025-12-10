#!/usr/bin/env python3
"""
WiFi Purple - One-Click Install & Run
Tự động cài đặt mọi thứ và chạy ứng dụng
"""

import os
import sys
import subprocess
import time

def print_banner():
    print("""
🌐 WiFi Purple GUI - Auto Installer
=====================================
Tự động cài đặt và khởi động ứng dụng
=====================================
    """)

def check_root():
    """Kiểm tra quyền root"""
    if os.geteuid() != 0:
        print("Cần quyền root để cài đặt!")
        print("Vui lòng chạy: sudo python3 install_and_run.py")
        return False
    return True

def install_system_packages():
    """Cài đặt các package hệ thống cần thiết"""
    print("📦 Cài đặt system packages...")
    
    packages = [
        'python3-venv',
        'python3-pip',
        'python3-tk',
        'aircrack-ng',
        'hostapd',
        'dnsmasq',
        'wireless-tools',
        'net-tools',
        'iw'
    ]
    
    try:
        # Update package list
        print("Cập nhật package list...")
        subprocess.run(['apt', 'update'], check=True, capture_output=True)
        
        # Install packages
        for package in packages:
            print(f"📥 Cài đặt {package}...")
            subprocess.run(['apt', 'install', '-y', package], 
                         check=True, capture_output=True)
        
        print("Tất cả system packages đã được cài đặt!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Lỗi cài đặt packages: {e}")
        return False

def setup_python_env():
    """Setup Python virtual environment"""
    print(" Setup Python environment...")
    
    try:
        # Tạo venv nếu chưa có
        if not os.path.exists('venv'):
            print(" Tạo virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Cài đặt requirements
        print(" Cài đặt Python packages...")
        pip_path = os.path.join('venv', 'bin', 'pip')
        subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
        
        print(" Python environment đã sẵn sàng!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Lỗi setup Python: {e}")
        return False

def run_application():
    """Chạy ứng dụng"""
    print(" Khởi động WiFi Purple GUI...")
    
    try:
        python_path = os.path.join('venv', 'bin', 'python')
        subprocess.run([python_path, 'run.py'])
        
    except KeyboardInterrupt:
        print("\n Tạm biệt!")
    except Exception as e:
        print(f" Lỗi chạy ứng dụng: {e}")

def main():
    print_banner()
    
    # Kiểm tra quyền root
    if not check_root():
        sys.exit(1)
    
    print(" Bắt đầu quá trình cài đặt tự động...")
    
    # Cài đặt system packages
    if not install_system_packages():
        print(" Một số packages có thể chưa được cài đặt đầy đủ")
    
    # Setup Python environment
    if not setup_python_env():
        print(" Không thể setup Python environment")
        sys.exit(1)
    
    print(" Cài đặt hoàn tất!")
    print(" Sẵn sàng khởi động ứng dụng...")
    time.sleep(2)
    
    # Chạy ứng dụng
    run_application()

if __name__ == "__main__":
    main()