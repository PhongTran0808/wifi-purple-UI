import customtkinter as ctk
from gui.navigation import NavigationBar

class HandshakePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Handshake Capture")

        title = ctk.CTkLabel(self, text="Handshake Capture", font=("Roboto", 22, "bold"))
        title.pack(pady=20)

        self.bssid_entry = ctk.CTkEntry(self, placeholder_text="Target BSSID")
        self.bssid_entry.pack(pady=10)

        self.channel_entry = ctk.CTkEntry(self, placeholder_text="Channel")
        self.channel_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="🤝 Bắt đầu Capture", width=200, command=self.start_capture)
        self.start_button.pack(pady=20)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=10)
        
        self.stop_button = ctk.CTkButton(
            control_frame, text="⏹️ Dừng", width=100,
            command=self.stop_capture, state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        home_button = ctk.CTkButton(
            control_frame, text="🏠 Trang chủ", width=100,
            command=lambda: self.controller.show_frame("MainPage")
        )
        home_button.pack(side="left", padx=5)
        
        back_button = ctk.CTkButton(
            control_frame, text="🔙 Quay lại", width=100,
            command=lambda: self.controller.show_frame("MainPage")
        )
        back_button.pack(side="left", padx=5)

        self.log_box = ctk.CTkTextbox(self, width=800, height=400)
        self.log_box.pack(pady=20)

    def start_capture(self):
        bssid = self.bssid_entry.get()
        channel = self.channel_entry.get()
        
        if not bssid or not channel:
            self.log_box.insert("end", "❌ Vui lòng nhập đầy đủ BSSID và Channel!\n\n")
            return

        self.log_box.insert("end", f"🤝 Bắt handshake từ {bssid} @ channel {channel}\n")
        self.log_box.insert("end", "🔄 Đang monitor và capture...\n")
        
        # Disable start button, enable stop button
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Run capture in background thread
        import threading
        threading.Thread(target=self.run_handshake_capture, args=(bssid, channel), daemon=True).start()
    
    def run_handshake_capture(self, bssid, channel):
        """Run handshake capture in background"""
        try:
            # Lấy interface từ config
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            
            if 'monitor_interface' in config.get('system', {}):
                interface = config['system']['monitor_interface']
            else:
                interface = config["settings"]["default_interface"] + "mon"
            
            result = self.controller.handshake_ctrl.capture_handshake(interface, bssid, channel)
            self.after(0, lambda: self.log_box.insert("end", f"📡 {result}\n"))
        except Exception as e:
            self.after(0, lambda: self.log_box.insert("end", f"❌ Lỗi: {str(e)}\n"))
        finally:
            self.after(0, self.capture_finished)
    
    def stop_capture(self):
        """Stop handshake capture"""
        import subprocess
        try:
            # Kill airodump-ng and aireplay-ng processes
            subprocess.run("pkill airodump-ng", shell=True)
            subprocess.run("pkill aireplay-ng", shell=True)
            self.log_box.insert("end", "⏹️ Đã dừng capture handshake\n\n")
        except:
            pass
        
        self.capture_finished()
    
    def capture_finished(self):
        """Reset buttons when capture finishes"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
