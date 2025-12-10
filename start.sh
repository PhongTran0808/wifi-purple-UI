#!/bin/bash

# WiFi Purple GUI Startup Script
# Tự động cài đặt và khởi động ứng dụng

echo "🌐 WiFi Purple GUI - Auto Setup & Start"
echo "======================================"

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Cần quyền root để chạy. Vui lòng sử dụng sudo!"
    echo "Sử dụng: sudo ./start.sh"
    exit 1
fi

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được cài đặt!"
    echo "Cài đặt: sudo apt install python3 python3-pip"
    exit 1
fi

# Tạo virtual environment nếu chưa có
if [ ! -d "venv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt virtual environment
echo "🔄 Kích hoạt virtual environment..."
source venv/bin/activate

# Cài đặt Python dependencies
echo "📚 Cài đặt Python packages..."
pip install -r requirements.txt

# Chạy ứng dụng với auto setup
echo "🚀 Khởi động WiFi Purple GUI..."
python3 run.py

echo "👋 Cảm ơn bạn đã sử dụng WiFi Purple!"