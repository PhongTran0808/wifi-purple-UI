import customtkinter as ctk
import subprocess
import os
from gui.navigation import NavigationBar
from gui.theme_manager import theme_manager, ThemeSelector

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Settings")
        
        # Title
        title = ctk.CTkLabel(self, text="⚙️ Cài đặt hệ thống", font=("Roboto", 24, "bold"))
        title.pack(pady=20)
        
        # Main settings frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Interface selection
        interface_frame = ctk.CTkFrame(settings_frame)
        interface_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(interface_frame, text="📡 WiFi Interface:", font=("Roboto", 16, "bold")).pack(pady=10)
        
        self.interface_var = ctk.StringVar(value="wlan0")
        self.interface_entry = ctk.CTkEntry(
            interface_frame, textvariable=self.interface_var,
            placeholder_text="wlan0, wlan1, etc."
        )
        self.interface_entry.pack(pady=5)
        
        # Interface buttons
        interface_buttons = ctk.CTkFrame(interface_frame, fg_color="transparent")
        interface_buttons.pack(pady=10)
        
        ctk.CTkButton(
            interface_buttons, text="🔍 Xem Interfaces",
            command=self.show_interfaces
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            interface_buttons, text="🔄 Monitor Mode ON",
            command=self.start_monitor_mode
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            interface_buttons, text="⏹️ Monitor Mode OFF", 
            command=self.stop_monitor_mode
        ).pack(side="left", padx=5)
        
        # Output settings
        output_frame = ctk.CTkFrame(settings_frame)
        output_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(output_frame, text="📁 Thư mục lưu file:", font=("Roboto", 16, "bold")).pack(pady=10)
        
        self.output_path = ctk.StringVar(value="/tmp/wifi-purple")
        self.output_entry = ctk.CTkEntry(
            output_frame, textvariable=self.output_path,
            placeholder_text="/path/to/output"
        )
        self.output_entry.pack(pady=5, fill="x", padx=20)
        
        # Theme settings
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(pady=20, padx=20, fill="x")
        
        self.theme_selector = ThemeSelector(theme_frame, theme_manager, self.on_theme_change)
        self.theme_selector.pack(pady=10, padx=20, fill="x")
        
        # Auto refresh settings
        refresh_frame = ctk.CTkFrame(settings_frame)
        refresh_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(refresh_frame, text="🔄 Tự động refresh (giây):", font=("Roboto", 16, "bold")).pack(pady=10)
        
        self.refresh_var = ctk.StringVar(value="5")
        self.refresh_entry = ctk.CTkEntry(
            refresh_frame, textvariable=self.refresh_var,
            placeholder_text="5"
        )
        self.refresh_entry.pack(pady=5)
        
        # Log display
        self.log_frame = ctk.CTkFrame(settings_frame)
        self.log_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(self.log_frame, text="📋 System Log:", font=("Roboto", 16, "bold")).pack(pady=10)
        
        self.log_textbox = ctk.CTkTextbox(self.log_frame, height=200)
        self.log_textbox.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame, text="💾 Lưu cài đặt",
            command=self.save_settings
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, text="🏠 Trang chủ",
            command=lambda: controller.show_frame("MainPage")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, text="🔙 Quay lại",
            command=lambda: controller.show_frame("MainPage")
        ).pack(side="left", padx=10)
        
        # Load current settings
        self.load_settings()
    
    def show_interfaces(self):
        try:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.insert("1.0", result.stdout)
        except Exception as e:
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.insert("1.0", f"Lỗi: {str(e)}")
    
    def start_monitor_mode(self):
        interface = self.interface_var.get()
        try:
            self.log_textbox.insert("end", f"\\n[INFO] Bắt đầu monitor mode cho {interface}...")
            cmd = f"airmon-ng check kill && airmon-ng start {interface}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.log_textbox.insert("end", f"\\n{result.stdout}")
            if result.stderr:
                self.log_textbox.insert("end", f"\\n[ERROR] {result.stderr}")
        except Exception as e:
            self.log_textbox.insert("end", f"\\n[ERROR] {str(e)}")
    
    def stop_monitor_mode(self):
        interface = self.interface_var.get()
        try:
            self.log_textbox.insert("end", f"\\n[INFO] Dừng monitor mode cho {interface}...")
            cmd = f"airmon-ng stop {interface}mon"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.log_textbox.insert("end", f"\\n{result.stdout}")
            if result.stderr:
                self.log_textbox.insert("end", f"\\n[ERROR] {result.stderr}")
        except Exception as e:
            self.log_textbox.insert("end", f"\\n[ERROR] {str(e)}")
    
    def save_settings(self):
        # Save to config file
        config = {
            "interface": self.interface_var.get(),
            "output_path": self.output_path.get(),
            "refresh_interval": int(self.refresh_var.get())
        }
        
        try:
            import json
            with open("config.json", "r") as f:
                full_config = json.load(f)
            
            full_config["settings"]["default_interface"] = config["interface"]
            full_config["settings"]["auto_refresh_scan"] = config["refresh_interval"]
            full_config["settings"]["output_path"] = config["output_path"]
            
            with open("config.json", "w") as f:
                json.dump(full_config, f, indent=4)
            
            self.log_textbox.insert("end", "\\n[INFO] Đã lưu cài đặt thành công!")
        except Exception as e:
            self.log_textbox.insert("end", f"\\n[ERROR] Lỗi lưu cài đặt: {str(e)}")
    
    def load_settings(self):
        try:
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            
            self.interface_var.set(config["settings"]["default_interface"])
            self.refresh_var.set(str(config["settings"]["auto_refresh_scan"]))
            
            if "output_path" in config["settings"]:
                self.output_path.set(config["settings"]["output_path"])
                
        except Exception as e:
            self.log_textbox.insert("end", f"[ERROR] Lỗi load cài đặt: {str(e)}")
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        self.log_textbox.insert("end", f"\\n[INFO] Đã chuyển sang theme: {theme_name}")
        # Note: App restart may be required for full theme application