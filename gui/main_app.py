import customtkinter as ctk
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
