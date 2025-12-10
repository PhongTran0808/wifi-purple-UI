import os
import sys
import customtkinter as ctk

from controllers.scan_controller import ScanController
# Import controllers
from controllers.deauth_controller import DeauthController
from controllers.evil_twin_controller import EvilTwinController
from controllers.handshake_controller import HandshakeController

# Import GUI pages
from gui.main_app import MainPage
from gui.scan_page import ScanPage
from gui.deauth_page import DeauthPage
from gui.evil_twin_page import EvilTwinPage
from gui.handshake_page import HandshakePage


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
            theme_path = os.path.join("assets", "themes", "dark-theme.json")
            if os.path.exists(theme_path):
                ctk.set_default_color_theme(theme_path)
                ctk.set_appearance_mode("dark")
            else:
                print("[WARNING] Không tìm thấy file theme, dùng theme mặc định.")
        except Exception as e:
            print(f"[ERROR] Lỗi load theme: {e}")

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
            "ScanPage": ScanPage,
            "DeauthPage": DeauthPage,
            "EvilTwinPage": EvilTwinPage,
            "HandshakePage": HandshakePage,
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
    app = WifiPurpleApp()
    app.mainloop()
