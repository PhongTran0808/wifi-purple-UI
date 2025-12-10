import os
import sys
import customtkinter as ctk

# Import system setup
from system_setup import auto_setup_if_needed

from controllers.scan_controller import ScanController
# Import controllers
from controllers.deauth_controller import DeauthController
from controllers.evil_twin_controller import EvilTwinController
from controllers.handshake_controller import HandshakeController

# Import GUI pages
from gui.main_app import MainPage
from gui.dashboard_page import DashboardPage
from gui.scan_page import ScanPage
from gui.advanced_scan_page import AdvancedScanPage
from gui.deauth_page import DeauthPage
from gui.evil_twin_page import EvilTwinPage
from gui.handshake_page import HandshakePage
from gui.help_page import HelpPage
from gui.settings_page import SettingsPage
from gui.integrations_page import IntegrationsPage


# ===============================
# ỨNG DỤNG CHÍNH
# ===============================
class WifiPurpleApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # --------------------------
        # Cấu hình cửa sổ
        # --------------------------
        self.title("WiFi Purple - GUI Controller")
        self.geometry("1100x700")
        self.resizable(True, True)

        # Load theme
        self.load_theme()

        # Load icon nếu có
        self.load_icon()

        # Controller (logic)
        self.scan_ctrl = ScanController()
        self.deauth_ctrl = DeauthController()
        self.evil_ctrl = EvilTwinController()
        self.handshake_ctrl = HandshakeController()

        # --------------------------
        # Frame chứa các trang
        # --------------------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Dictionary chứa tất cả pages
        self.frames = {}

        # Khởi tạo các page GUI
        self.init_pages()

        # Mở trang chính
        self.show_frame("MainPage")

    # ==========================================
    # Load theme (dark-theme.json)
    # ==========================================
    def load_theme(self):
        try:
            # Tạm thời dùng theme mặc định để tránh lỗi
            ctk.set_default_color_theme("blue")
            ctk.set_appearance_mode("dark")
            print("[INFO] Đang dùng theme mặc định")
        except Exception as e:
            print(f"[ERROR] Lỗi load theme: {e}")
            ctk.set_default_color_theme("blue")
            ctk.set_appearance_mode("dark")

    # ==========================================
    # Load icon
    # ==========================================
    def load_icon(self):
        try:
            icon_path = os.path.join("assets", "icons", "wifi.png")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass

    # ==========================================
    # Khởi tạo tất cả trang GUI
    # ==========================================
    def init_pages(self):
        pages = {
            "MainPage": MainPage,
            "DashboardPage": DashboardPage,
            "ScanPage": ScanPage,
            "AdvancedScanPage": AdvancedScanPage,
            "DeauthPage": DeauthPage,
            "EvilTwinPage": EvilTwinPage,
            "HandshakePage": HandshakePage,
            "HelpPage": HelpPage,
            "SettingsPage": SettingsPage,
            "IntegrationsPage": IntegrationsPage,
        }

        for name, PageClass in pages.items():
            frame = PageClass(
                parent=self.container,
                controller=self
            )
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # ==========================================
    # Hàm chuyển trang
    # ==========================================
    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()


# ===============================
# CHẠY CHƯƠNG TRÌNH
# ===============================
if __name__ == "__main__":
    print("🚀 Khởi động WiFi Purple GUI...")
    
    # Tự động setup hệ thống nếu cần
    if not auto_setup_if_needed():
        print("❌ Setup thất bại. Một số tính năng có thể không hoạt động.")
        print("Bạn có thể chạy thủ công: sudo python3 system_setup.py")
        
        # Hỏi người dùng có muốn tiếp tục không
        try:
            choice = input("Tiếp tục chạy app? (y/n): ").lower()
            if choice != 'y':
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
    
    print("✓ Khởi động giao diện...")
    app = WifiPurpleApp()
    app.mainloop()
