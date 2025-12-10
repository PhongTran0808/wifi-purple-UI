import customtkinter as ctk
from PIL import Image, ImageTk
import os
from gui.navigation import NavigationBar

class HelpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Help")
        
        # Title
        title = ctk.CTkLabel(self, text="📖 Hướng dẫn sử dụng WiFi Purple", font=("Roboto", 24, "bold"))
        title.pack(pady=20)
        
        # Scrollable frame for help content
        self.help_frame = ctk.CTkScrollableFrame(self, label_text="Chức năng các nút")
        self.help_frame.pack(pady=20, padx=20, expand=True, fill="both")
        
        # Help content
        self.create_help_content()
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=20)
        
        home_button = ctk.CTkButton(
            nav_frame, text="🏠 Trang chủ", width=120, height=40,
            command=lambda: controller.show_frame("MainPage")
        )
        home_button.pack(side="left", padx=10)
        
        back_button = ctk.CTkButton(
            nav_frame, text="🔙 Quay lại", width=120, height=40,
            command=lambda: controller.show_frame("MainPage")
        )
        back_button.pack(side="left", padx=10)
    
    def create_help_content(self):
        help_items = [
            {
                "title": "🔍 Scan WiFi",
                "description": "Quét và hiển thị tất cả các mạng WiFi xung quanh",
                "details": [
                    "• Tự động phát hiện interface WiFi",
                    "• Hiển thị SSID, BSSID, Channel, Signal strength",
                    "• Phân loại bảo mật (WPA, WPA2, WPA3, Open)",
                    "• Cập nhật real-time"
                ]
            },
            {
                "title": "💥 Deauth Attack", 
                "description": "Tấn công ngắt kết nối thiết bị khỏi mạng WiFi",
                "details": [
                    "• Nhập BSSID của mạng mục tiêu",
                    "• Chọn channel tương ứng",
                    "• Gửi gói deauthentication",
                    "• Có thể dừng bất cứ lúc nào"
                ]
            },
            {
                "title": "👥 Evil Twin",
                "description": "Tạo Access Point giả mạo để thu thập thông tin",
                "details": [
                    "• Tạo AP giả với tên tùy chỉnh",
                    "• Chọn channel phù hợp",
                    "• Bắt chước mạng thật",
                    "• Monitor kết nối của victim"
                ]
            },
            {
                "title": "🤝 Handshake Capture",
                "description": "Bắt gói handshake WPA/WPA2 để crack password",
                "details": [
                    "• Nhập BSSID mục tiêu",
                    "• Chọn channel chính xác", 
                    "• Tự động capture handshake",
                    "• Lưu file để crack sau"
                ]
            },
            {
                "title": "⚙️ Cài đặt",
                "description": "Cấu hình interface và các tùy chọn khác",
                "details": [
                    "• Chọn WiFi interface",
                    "• Bật/tắt monitor mode",
                    "• Cài đặt thời gian refresh",
                    "• Quản lý file output"
                ]
            }
        ]
        
        for item in help_items:
            # Create frame for each help item
            item_frame = ctk.CTkFrame(self.help_frame)
            item_frame.pack(pady=10, padx=10, fill="x")
            
            # Title
            title_label = ctk.CTkLabel(
                item_frame, text=item["title"], 
                font=("Roboto", 18, "bold")
            )
            title_label.pack(pady=(15, 5), padx=20, anchor="w")
            
            # Description
            desc_label = ctk.CTkLabel(
                item_frame, text=item["description"],
                font=("Roboto", 14), wraplength=600
            )
            desc_label.pack(pady=5, padx=20, anchor="w")
            
            # Details
            for detail in item["details"]:
                detail_label = ctk.CTkLabel(
                    item_frame, text=detail,
                    font=("Roboto", 12), text_color="gray"
                )
                detail_label.pack(pady=2, padx=40, anchor="w")
        
        # Warning section
        warning_frame = ctk.CTkFrame(self.help_frame, fg_color="#4a1a1a")
        warning_frame.pack(pady=20, padx=10, fill="x")
        
        warning_title = ctk.CTkLabel(
            warning_frame, text="⚠️ LƯU Ý QUAN TRỌNG",
            font=("Roboto", 16, "bold"), text_color="#ff6b6b"
        )
        warning_title.pack(pady=15, padx=20)
        
        warnings = [
            "• Chỉ sử dụng trên mạng của bạn hoặc có sự cho phép",
            "• Cần quyền root để chạy các tính năng",
            "• WiFi adapter phải hỗ trợ monitor mode",
            "• Tuân thủ pháp luật địa phương về bảo mật mạng"
        ]
        
        for warning in warnings:
            warning_label = ctk.CTkLabel(
                warning_frame, text=warning,
                font=("Roboto", 12), text_color="#ffcc99"
            )
            warning_label.pack(pady=2, padx=40, anchor="w")