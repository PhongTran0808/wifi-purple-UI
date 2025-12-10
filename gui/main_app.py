import customtkinter as ctk
import os
from PIL import Image, ImageTk
from gui.scan_page import ScanPage
from gui.deauth_page import DeauthPage
from gui.evil_twin_page import EvilTwinPage
from gui.handshake_page import HandshakePage

class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Wifi Purple GUI")
        self.geometry("1100x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ============================
        #  Sidebar
        # ============================
        self.sidebar_frame = ctk.CTkFrame(self, width=180)
        self.sidebar_frame.pack(side="left", fill="y")

        self.sidebar_label = ctk.CTkLabel(
            self.sidebar_frame, text="Wifi Purple",
            font=("Roboto", 18, "bold")
        )
        self.sidebar_label.pack(pady=20)

        # Buttons
        self.scan_button = ctk.CTkButton(
            self.sidebar_frame, text="Scan WiFi", command=self.show_scan_page
        )
        self.scan_button.pack(pady=10)

        self.deauth_button = ctk.CTkButton(
            self.sidebar_frame, text="Deauth Attack", command=self.show_deauth_page
        )
        self.deauth_button.pack(pady=10)

        self.evil_twin_button = ctk.CTkButton(
            self.sidebar_frame, text="Evil Twin", command=self.show_evil_twin_page
        )
        self.evil_twin_button.pack(pady=10)

        self.handshake_button = ctk.CTkButton(
            self.sidebar_frame, text="Handshake Capture", command=self.show_handshake_page
        )
        self.handshake_button.pack(pady=10)

        # ============================
        #  Main content frame
        # ============================
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Load default page
        self.current_page = None
        self.show_scan_page()

    # ============================
    # Page switching
    # ============================

    def clear_main_frame(self):
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()

    def show_scan_page(self):
        self.clear_main_frame()
        self.current_page = ScanPage(self.main_frame)
        self.current_page.pack(expand=True, fill="both")

    def show_deauth_page(self):
        self.clear_main_frame()
        self.current_page = DeauthPage(self.main_frame)
        self.current_page.pack(expand=True, fill="both")

    def show_evil_twin_page(self):
        self.clear_main_frame()
        self.current_page = EvilTwinPage(self.main_frame)
        self.current_page.pack(expand=True, fill="both")

    def show_handshake_page(self):
        self.clear_main_frame()
        self.current_page = HandshakePage(self.main_frame)
        self.current_page.pack(expand=True, fill="both")


class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Logo/Banner
        try:
            logo_path = os.path.join("assets", "images", "logo.png")
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path).resize((100, 100))
                logo_photo = ImageTk.PhotoImage(logo_image)
                logo_label = ctk.CTkLabel(self, image=logo_photo, text="")
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack(pady=20)
        except:
            pass

        self.label = ctk.CTkLabel(self, text="🌐 WiFi Purple GUI", font=("Roboto", 28, "bold"))
        self.label.pack(pady=20)
        
        subtitle = ctk.CTkLabel(self, text="Công cụ kiểm tra bảo mật WiFi", font=("Roboto", 16))
        subtitle.pack(pady=10)

        # Main buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)

        # Create buttons with icons
        buttons = [
            ("📊 Dashboard", "DashboardPage", "scan.png"),
            ("🔍 Basic Scan", "ScanPage", "scan.png"),
            ("🔍 Advanced Scan", "AdvancedScanPage", "scan.png"),
            ("💥 Deauth Attack", "DeauthPage", "deauth.png"), 
            ("👥 Evil Twin", "EvilTwinPage", "evil_twin.png"),
            ("🤝 Handshake Capture", "HandshakePage", "handshake.png"),
            ("🔗 Integrations", "IntegrationsPage", "settings.png"),
        ]

        for text, page_name, icon_name in buttons:
            button = ctk.CTkButton(
                button_frame,
                text=text,
                width=250,
                height=50,
                font=("Roboto", 16),
                command=lambda p=page_name: controller.show_frame(p)
            )
            button.pack(pady=8)
        
        # Help and Settings buttons
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(pady=30)
        
        help_button = ctk.CTkButton(
            bottom_frame,
            text="📖 Hướng dẫn",
            width=150,
            height=40,
            command=lambda: controller.show_frame("HelpPage")
        )
        help_button.pack(side="left", padx=10)
        
        settings_button = ctk.CTkButton(
            bottom_frame,
            text="⚙️ Cài đặt", 
            width=150,
            height=40,
            command=lambda: controller.show_frame("SettingsPage")
        )
        settings_button.pack(side="left", padx=10)
        
        exit_button = ctk.CTkButton(
            bottom_frame,
            text="🚪 Thoát",
            width=150,
            height=40,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.exit_app
        )
        exit_button.pack(side="left", padx=10)
    
    def exit_app(self):
        """Thoát ứng dụng"""
        import tkinter.messagebox as msgbox
        if msgbox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.controller.quit()
