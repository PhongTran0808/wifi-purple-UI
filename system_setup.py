#!/usr/bin/env python3
"""
System Setup Module - Tự động cài đặt và cấu hình hệ thống
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

class SystemSetup:
    def __init__(self):
        self.required_tools = [
            'aircrack-ng',
            'airmon-ng', 
            'airodump-ng',
            'aireplay-ng',
            'hostapd',
            'dnsmasq',
            'mdk3',
            'bully'
        ]
        
        self.python_packages = [
            'customtkinter>=5.2.0',
            'Pillow>=10.0.0',
            'colorama>=0.4.6'
        ]
        
        self.setup_log = []
    
    def log(self, message, level="INFO"):
        """Log setup messages"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.setup_log.append(log_entry)
        print(log_entry)
    
    def check_root(self):
        """Kiểm tra quyền root"""
        if os.geteuid() != 0:
            self.log("Cần quyền root để cài đặt. Vui lòng chạy với sudo!", "ERROR")
            return False
        return True
    
    def update_system(self):
        """Cập nhật hệ thống"""
        self.log("Đang cập nhật danh sách package...")
        try:
            subprocess.run(['apt', 'update'], check=True, capture_output=True)
            self.log("Cap nhat thanh cong")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Loi cap nhat: {e}", "ERROR")
            return False
    
    def install_system_tools(self):
        """Cài đặt các công cụ hệ thống cần thiết"""
        self.log("Đang cài đặt các công cụ WiFi hacking...")
        
        # Cài đặt aircrack-ng suite và additional tools
        packages = [
            'aircrack-ng',
            'hostapd', 
            'dnsmasq',
            'mdk3',
            'bully',
            'wireless-tools',
            'net-tools',
            'iw',
            'nmap',
            'wireshark',
            'tshark',
            'whois',
            'dnsutils',
            'curl',
            'wget'
        ]
        
        for package in packages:
            try:
                self.log(f"Đang cài đặt {package}...")
                subprocess.run(['apt', 'install', '-y', package], 
                             check=True, capture_output=True)
                self.log(f"{package} da cai dat")
            except subprocess.CalledProcessError:
                self.log(f"Loi cai dat {package}", "WARNING")
        
        return True
    
    def install_python_packages(self):
        """Cài đặt Python packages"""
        self.log("Đang cài đặt Python packages...")
        
        for package in self.python_packages:
            try:
                self.log(f"Đang cài đặt {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                             check=True, capture_output=True)
                self.log(f"{package} da cai dat")
            except subprocess.CalledProcessError:
                self.log(f"Loi cai dat {package}", "WARNING")
        
        return True
    
    def detect_wifi_interfaces(self):
        """Tự động phát hiện WiFi interfaces"""
        self.log("Đang phát hiện WiFi interfaces...")
        
        try:
            # Sử dụng iwconfig để tìm wireless interfaces
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            interfaces = []
            
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line:
                    interface = line.split()[0]
                    interfaces.append(interface)
            
            if interfaces:
                self.log(f"Tim thay WiFi interfaces: {', '.join(interfaces)}")
                return interfaces[0]  # Trả về interface đầu tiên
            else:
                self.log("Khong tim thay WiFi interface, su dung wlan0 mac dinh", "WARNING")
                return "wlan0"
                
        except Exception as e:
            self.log(f"Loi phat hien interface: {e}", "ERROR")
            return "wlan0"
    
    def setup_monitor_mode(self, interface):
        """Tự động setup monitor mode"""
        self.log(f"Đang setup monitor mode cho {interface}...")
        
        try:
            # Kill các process có thể can thiệp
            subprocess.run(['airmon-ng', 'check', 'kill'], 
                         capture_output=True, check=False)
            
            # Bật monitor mode
            result = subprocess.run(['airmon-ng', 'start', interface], 
                                  capture_output=True, text=True)
            
            if 'monitor mode enabled' in result.stdout.lower():
                monitor_interface = f"{interface}mon"
                self.log(f"Monitor mode da bat: {monitor_interface}")
                return monitor_interface
            else:
                self.log("Co the monitor mode chua bat hoan toan", "WARNING")
                return f"{interface}mon"
                
        except Exception as e:
            self.log(f"Loi setup monitor mode: {e}", "ERROR")
            return f"{interface}mon"
    
    def create_output_directories(self):
        """Tạo các thư mục output cần thiết"""
        self.log("Đang tạo thư mục output...")
        
        directories = [
            '/tmp/wifi-purple',
            '/tmp/wifi-purple/handshakes',
            '/tmp/wifi-purple/scans',
            '/tmp/wifi-purple/logs'
        ]
        
        for directory in directories:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                self.log(f"Tao thu muc: {directory}")
            except Exception as e:
                self.log(f"Loi tao thu muc {directory}: {e}", "ERROR")
    
    def update_config(self, wifi_interface, monitor_interface):
        """Cập nhật file config với thông tin hệ thống"""
        self.log("Đang cập nhật config...")
        
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            # Cập nhật interface
            config['settings']['default_interface'] = wifi_interface
            config['settings']['monitor_interface'] = monitor_interface
            config['settings']['output_path'] = '/tmp/wifi-purple'
            
            # Thêm system info
            config['system'] = {
                'auto_setup_completed': True,
                'setup_timestamp': time.time(),
                'detected_interface': wifi_interface,
                'monitor_interface': monitor_interface
            }
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            self.log("Config da duoc cap nhat")
            return True
            
        except Exception as e:
            self.log(f"Loi cap nhat config: {e}", "ERROR")
            return False
    
    def verify_installation(self):
        """Kiểm tra cài đặt"""
        self.log("Dang kiem tra cai dat...")
        
        # Kiểm tra tools
        missing_tools = []
        for tool in self.required_tools:
            try:
                subprocess.run(['which', tool], check=True, capture_output=True)
                self.log(f"{tool} co san")
            except subprocess.CalledProcessError:
                missing_tools.append(tool)
                self.log(f"{tool} khong tim thay", "WARNING")
        
        if missing_tools:
            self.log(f"Mot so tools thieu: {', '.join(missing_tools)}", "WARNING")
        else:
            self.log("Tat ca tools da san sang")
        
        return len(missing_tools) == 0
    
    def run_full_setup(self):
        """Chạy toàn bộ quá trình setup"""
        self.log("=== BẮT ĐẦU SETUP HỆ THỐNG ===")
        
        # Kiểm tra quyền root
        if not self.check_root():
            return False
        
        # Cập nhật hệ thống
        if not self.update_system():
            self.log("Tiếp tục mà không cập nhật...", "WARNING")
        
        # Cài đặt system tools
        self.install_system_tools()
        
        # Cài đặt Python packages
        self.install_python_packages()
        
        # Phát hiện WiFi interface
        wifi_interface = self.detect_wifi_interfaces()
        
        # Setup monitor mode
        monitor_interface = self.setup_monitor_mode(wifi_interface)
        
        # Tạo thư mục
        self.create_output_directories()
        
        # Cập nhật config
        self.update_config(wifi_interface, monitor_interface)
        
        # Kiểm tra cài đặt
        success = self.verify_installation()
        
        self.log("=== HOÀN THÀNH SETUP ===")
        
        if success:
            self.log(" Setup thành công! Hệ thống sẵn sàng sử dụng.")
        else:
            self.log(" Setup hoàn thành với một số cảnh báo.", "WARNING")
        
        return success
    
    def quick_check(self):
        """Kiểm tra nhanh hệ thống có sẵn sàng không"""
        try:
            # Kiểm tra config
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            if config.get('system', {}).get('auto_setup_completed'):
                return True
            
            return False
        except:
            return False

def auto_setup_if_needed():
    """Tự động setup nếu cần thiết"""
    setup = SystemSetup()
    
    if not setup.quick_check():
        print(" Hệ thống chưa được setup. Đang tự động cài đặt...")
        return setup.run_full_setup()
    else:
        print(" Hệ thống đã sẵn sàng")
        return True

if __name__ == "__main__":
    setup = SystemSetup()
    setup.run_full_setup()