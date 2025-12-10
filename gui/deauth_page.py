import customtkinter as ctk
from gui.navigation import NavigationBar

class DeauthPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Deauth Attack")

        title = ctk.CTkLabel(self, text="Deauthentication Attack", font=("Roboto", 22, "bold"))
        title.pack(pady=20)

        self.bssid_entry = ctk.CTkEntry(self, placeholder_text="BSSID")
        self.bssid_entry.pack(pady=10)

        self.channel_entry = ctk.CTkEntry(self, placeholder_text="Channel")
        self.channel_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="💥 Bắt đầu Deauth", width=200, command=self.start_attack)
        self.start_button.pack(pady=20)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=10)
        
        self.stop_button = ctk.CTkButton(
            control_frame, text="⏹️ Dừng", width=100,
            command=self.stop_attack, state="disabled"
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

    def start_attack(self):
        bssid = self.bssid_entry.get()
        channel = self.channel_entry.get()
        
        if not bssid or not channel:
            self.log_box.insert("end", "❌ Vui lòng nhập đầy đủ BSSID và Channel!\n\n")
            return

        self.log_box.insert("end", f"💥 Bắt đầu tấn công deauth: {bssid} @ channel {channel}\n")
        self.log_box.insert("end", "🔄 Đang thực thi lệnh...\n")
        
        # Disable start button, enable stop button
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Run attack in background thread
        import threading
        threading.Thread(target=self.run_deauth_attack, args=(bssid, channel), daemon=True).start()
    
    def run_deauth_attack(self, bssid, channel):
        """Run deauth attack in background"""
        try:
            # Lấy interface từ config
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            
            if 'monitor_interface' in config.get('system', {}):
                interface = config['system']['monitor_interface']
            else:
                interface = config["settings"]["default_interface"] + "mon"
            
            result = self.controller.deauth_ctrl.run_deauth(interface, bssid, 0)  # 0 = continuous
            self.after(0, lambda: self.log_box.insert("end", f"📡 {result}\n"))
        except Exception as e:
            self.after(0, lambda: self.log_box.insert("end", f"❌ Lỗi: {str(e)}\n"))
        finally:
            self.after(0, self.attack_finished)
    
    def stop_attack(self):
        """Stop deauth attack"""
        import subprocess
        try:
            # Kill aireplay-ng processes
            subprocess.run("pkill aireplay-ng", shell=True)
            self.log_box.insert("end", "⏹️ Đã dừng tấn công deauth\n\n")
        except:
            pass
        
        self.attack_finished()
    
    def attack_finished(self):
        """Reset buttons when attack finishes"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
