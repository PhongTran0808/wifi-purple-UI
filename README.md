# 🌐 WiFi Purple GUI

Giao diện đồ họa cho công cụ kiểm tra bảo mật WiFi với tính năng tự động cài đặt.

## ✨ Tính năng

- 🔍 **Scan WiFi**: Quét và hiển thị mạng WiFi xung quanh
- 💥 **Deauth Attack**: Tấn công ngắt kết nối thiết bị
- 👥 **Evil Twin**: Tạo Access Point giả mạo
- 🤝 **Handshake Capture**: Bắt gói handshake WPA/WPA2
- ⚙️ **Auto Setup**: Tự động cài đặt và cấu hình hệ thống
- 📖 **Help**: Hướng dẫn chi tiết các tính năng

## 🚀 Cài đặt & Chạy (Một lệnh duy nhất)

### Cách 1: Auto Install (Khuyến nghị)
```bash
sudo python3 install_and_run.py
```

### Cách 2: Script khởi động
```bash
chmod +x start.sh
sudo ./start.sh
```

### Cách 3: Thủ công
```bash
# 1. Cài đặt system packages
sudo apt update
sudo apt install -y aircrack-ng hostapd dnsmasq python3-venv python3-pip

# 2. Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Cài đặt Python packages
pip install -r requirements.txt

# 4. Chạy ứng dụng
sudo venv/bin/python3 run.py
```

## 📋 Yêu cầu hệ thống

- **OS**: Kali Linux / Ubuntu / Debian
- **Python**: 3.8+
- **Quyền**: Root (sudo)
- **WiFi**: Adapter hỗ trợ monitor mode

## 🔧 Tính năng tự động

App sẽ tự động:
- ✅ Cài đặt aircrack-ng suite
- ✅ Phát hiện WiFi interface
- ✅ Bật monitor mode
- ✅ Tạo thư mục output
- ✅ Cấu hình hệ thống

## 📖 Hướng dẫn sử dụng

1. **Khởi động**: Chạy `sudo python3 install_and_run.py`
2. **Scan WiFi**: Click "🔍 Scan WiFi" để quét mạng
3. **Chọn mục tiêu**: Chọn mạng từ danh sách
4. **Thực hiện tấn công**: Chọn loại tấn công và nhập thông tin
5. **Dừng**: Click "⏹️ Dừng" để dừng bất cứ lúc nào

## ⚠️ Lưu ý quan trọng

- Chỉ sử dụng trên mạng của bạn hoặc có sự cho phép
- Tuân thủ pháp luật địa phương về bảo mật mạng
- Cần quyền root để thực hiện các tác vụ WiFi
- WiFi adapter phải hỗ trợ monitor mode

## 🐛 Xử lý lỗi

Nếu gặp lỗi:
1. Đảm bảo chạy với quyền sudo
2. Kiểm tra WiFi adapter hỗ trợ monitor mode
3. Chạy `sudo python3 system_setup.py` để setup lại
4. Kiểm tra log trong thư mục `/tmp/wifi-purple/logs`

## 📁 Cấu trúc project

```
wifi-purple-gui/
├── run.py                 # File chính
├── install_and_run.py     # Auto installer
├── system_setup.py        # System setup module
├── start.sh              # Startup script
├── config.json           # Cấu hình
├── requirements.txt      # Python dependencies
├── gui/                  # GUI modules
├── controllers/          # Logic controllers
├── assets/              # Icons & images
└── Wifi-Purple/         # Original wifi-purple tools
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## 📄 License

Dự án này được phát hành dưới MIT License.

---

**⚡ Tip**: Để có trải nghiệm tốt nhất, hãy sử dụng `sudo python3 install_and_run.py` - một lệnh duy nhất để cài đặt và chạy mọi thứ!