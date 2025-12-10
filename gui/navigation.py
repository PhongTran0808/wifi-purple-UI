import customtkinter as ctk

class NavigationBar(ctk.CTkFrame):
    """Thanh navigation chung cho tất cả các trang"""
    
    def __init__(self, parent, controller, current_page=""):
        super().__init__(parent, height=60, fg_color="#1a1a1a")
        self.controller = controller
        self.current_page = current_page
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        logo_label = ctk.CTkLabel(
            title_frame, text="🌐 WiFi Purple", 
            font=("Roboto", 18, "bold")
        )
        logo_label.pack(side="left")
        
        # Current page indicator
        if current_page:
            page_label = ctk.CTkLabel(
                title_frame, text=f"› {current_page}",
                font=("Roboto", 14), text_color="gray"
            )
            page_label.pack(side="left", padx=(10, 0))
        
        # Navigation buttons
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent")
        nav_buttons.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        # Home button
        home_btn = ctk.CTkButton(
            nav_buttons, text="🏠 Trang chủ", width=100, height=35,
            command=lambda: controller.show_frame("MainPage")
        )
        home_btn.pack(side="left", padx=5)
        
        # Help button
        help_btn = ctk.CTkButton(
            nav_buttons, text="📖 Help", width=80, height=35,
            command=lambda: controller.show_frame("HelpPage")
        )
        help_btn.pack(side="left", padx=5)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            nav_buttons, text="⚙️", width=40, height=35,
            command=lambda: controller.show_frame("SettingsPage")
        )
        settings_btn.pack(side="left", padx=5)
        
        # Pack to top
        self.pack(side="top", fill="x", padx=0, pady=0)