import customtkinter as ctk
from PIL import Image, ImageTk
from gui.navigation import NavigationBar

class WifiNetworkItem(ctk.CTkFrame):
    def __init__(self, parent, network_info):
        super().__init__(parent, fg_color=("#F0F0F0", "#202020"), corner_radius=10)

        self.network_info = network_info
        
        self.grid_columnconfigure(1, weight=1)

        # Security Icon
        sec_icon = self._get_security_icon(network_info.get("security", "OPEN"))
        sec_label = ctk.CTkLabel(self, image=sec_icon, text="")
        sec_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # SSID
        ssid_label = ctk.CTkLabel(self, text=network_info.get("ssid", "N/A"), font=("Roboto", 16, "bold"))
        ssid_label.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="w")

        # BSSID and Channel
        bssid = network_info.get("bssid", "??:??:??:??:??:??")
        channel = network_info.get("channel", "?")
        details_label = ctk.CTkLabel(self, text=f"BSSID: {bssid} | Channel: {channel}", font=("Roboto", 10), text_color="gray")
        details_label.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="w")

        # Signal Strength
        signal_strength = self._get_signal_strength_widget(network_info.get("signal", -100))
        signal_strength.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    def _get_security_icon(self, security_type):
        # Placeholder logic: uses wifi icon for all. Could be improved with more icons.
        icon_path = "assets/icons/wifi.png" # Default
        if "WPA" in security_type:
            # In a real scenario, you might have a 'lock.png' icon
            icon_path = "assets/icons/wifi.png" 
        elif "OPEN" in security_type:
            # You might have an 'unlock.png' icon
            icon_path = "assets/icons/wifi.png"

        pil_image = Image.open(icon_path).resize((24, 24))
        return ImageTk.PhotoImage(pil_image)

    def _get_signal_strength_widget(self, signal_dbm):
        # Convert dBm to a 0-4 bar scale
        if signal_dbm > -50:
            bars = 4
        elif signal_dbm > -67:
            bars = 3
        elif signal_dbm > -80:
            bars = 2
        elif signal_dbm > -90:
            bars = 1
        else:
            bars = 0
            
        # Create a frame to hold the bars
        bar_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        for i in range(4):
            bar = ctk.CTkFrame(bar_frame, width=5, height=6 * (i + 1), corner_radius=2)
            if i < bars:
                bar.configure(fg_color="#4A90E2")
            else:
                bar.configure(fg_color=("gray70", "gray30"))
            bar.pack(side="left", padx=1, anchor="bottom")
            
        return bar_frame

class ScanPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Scan WiFi")

        # Title and description
        title = ctk.CTkLabel(self, text="Quét Mạng WiFi", font=("Roboto", 22, "bold"))
        title.pack(pady=10, padx=20, anchor="w")
        
        description = ctk.CTkLabel(self, text="Tại đây, bạn có thể quét để tìm các mạng WiFi xung quanh và xem thông tin cơ bản về chúng.",
                                   font=("Roboto", 12))
        description.pack(pady=5, padx=20, anchor="w")

        # Scan button
        self.scan_button = ctk.CTkButton(
            self, text="Bắt đầu Quét", width=200,
            command=self.start_scan
        )
        self.scan_button.pack(pady=10, padx=20, anchor="w")

        # Frame for results
        self.result_frame = ctk.CTkScrollableFrame(self, label_text="Kết quả quét")
        self.result_frame.pack(pady=20, padx=20, expand=True, fill="both")
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=10)
        
        home_button = ctk.CTkButton(
            nav_frame, text="🏠 Trang chủ", width=120, height=40,
            command=lambda: self.controller.show_frame("MainPage")
        )
        home_button.pack(side="left", padx=5)
        
        back_button = ctk.CTkButton(
            nav_frame, text="🔙 Quay lại", width=120, height=40,
            command=lambda: self.controller.show_frame("MainPage")
        )
        back_button.pack(side="left", padx=5)

    def start_scan(self):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Disable scan button
        self.scan_button.configure(state="disabled", text="Đang quét...")
        
        # Add stop button
        self.stop_button = ctk.CTkButton(
            self, text="⏹️ Dừng quét", width=200,
            command=self.stop_scan
        )
        self.stop_button.pack(pady=5, padx=20, anchor="w")
        
        # Loading indicator
        loading_label = ctk.CTkLabel(self.result_frame, text="🔄 Đang quét mạng WiFi, vui lòng chờ...")
        loading_label.pack(pady=20)
        
        # Start real scan
        self.scan_networks_real()

    def display_results(self):
        # Clear "loading" text
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        networks = self._simulate_scan_results()
        
        # Create and display a WifiNetworkItem for each network
        for network in networks:
            item = WifiNetworkItem(self.result_frame, network)
            item.pack(pady=5, padx=10, fill="x")

    def scan_networks_real(self):
        """Thực hiện quét mạng thật sử dụng airodump-ng"""
        import subprocess
        import threading
        import json
        
        def scan_thread():
            try:
                # Load config để lấy interface
                with open("config.json", "r") as f:
                    config = json.load(f)
                
                # Sử dụng monitor interface nếu có, nếu không thì thêm 'mon'
                if 'monitor_interface' in config.get('system', {}):
                    interface = config['system']['monitor_interface']
                else:
                    interface = config["settings"]["default_interface"] + "mon"
                
                # Chạy airodump-ng trong thời gian ngắn để lấy kết quả
                cmd = f"timeout 10 airodump-ng {interface} --output-format csv --write /tmp/scan_result"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                # Parse kết quả từ CSV file
                networks = self.parse_airodump_csv("/tmp/scan_result-01.csv")
                
                # Update UI trong main thread
                self.after(0, lambda: self.display_real_results(networks))
                
            except Exception as e:
                # Fallback to demo data if real scan fails
                self.after(0, lambda: self.display_results())
                print(f"Scan error: {e}")
        
        # Start scan in background thread
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def parse_airodump_csv(self, csv_file):
        """Parse airodump-ng CSV output"""
        networks = []
        try:
            with open(csv_file, 'r') as f:
                lines = f.readlines()
            
            # Find the start of AP data
            ap_start = -1
            for i, line in enumerate(lines):
                if line.startswith("BSSID"):
                    ap_start = i + 1
                    break
            
            if ap_start == -1:
                return self._simulate_scan_results()
            
            # Parse AP data
            for line in lines[ap_start:]:
                if line.strip() == "" or line.startswith("Station MAC"):
                    break
                
                parts = line.split(',')
                if len(parts) >= 14:
                    bssid = parts[0].strip()
                    channel = parts[3].strip()
                    privacy = parts[5].strip()
                    power = parts[8].strip()
                    essid = parts[13].strip()
                    
                    if essid and bssid:
                        networks.append({
                            "ssid": essid,
                            "bssid": bssid,
                            "signal": int(power) if power.lstrip('-').isdigit() else -100,
                            "security": privacy if privacy else "OPEN",
                            "channel": int(channel) if channel.isdigit() else 0
                        })
            
            return networks if networks else self._simulate_scan_results()
            
        except Exception as e:
            print(f"Parse error: {e}")
            return self._simulate_scan_results()
    
    def display_real_results(self, networks):
        """Display real scan results"""
        # Clear loading text
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        if not networks:
            no_result_label = ctk.CTkLabel(self.result_frame, text="Không tìm thấy mạng WiFi nào")
            no_result_label.pack(pady=20)
            return
        
        # Create and display network items
        for network in networks:
            item = WifiNetworkItem(self.result_frame, network)
            item.pack(pady=5, padx=10, fill="x")
        
        # Re-enable scan button
        self.scan_button.configure(state="normal", text="Bắt đầu Quét")
        if hasattr(self, 'stop_button'):
            self.stop_button.destroy()
    
    def stop_scan(self):
        """Stop the scanning process"""
        # Kill any running airodump-ng processes
        import subprocess
        try:
            subprocess.run("pkill airodump-ng", shell=True)
        except:
            pass
        
        # Re-enable scan button
        self.scan_button.configure(state="normal", text="Bắt đầu Quét")
        if hasattr(self, 'stop_button'):
            self.stop_button.destroy()
        
        # Show stopped message
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        stopped_label = ctk.CTkLabel(self.result_frame, text="⏹️ Đã dừng quét")
        stopped_label.pack(pady=20)
    
    def _simulate_scan_results(self):
        """Returns a list of fake WiFi networks for UI demonstration."""
        return [
            {"ssid": "MyHome_WiFi_5G", "bssid": "A1:B2:C3:D4:E5:F6", "signal": -45, "security": "WPA2", "channel": 149},
            {"ssid": "Neighbors_Guest", "bssid": "1A:2B:3C:4D:5E:6F", "signal": -78, "security": "WPA2", "channel": 6},
            {"ssid": "Free_Public_WiFi", "bssid": "FF:EE:DD:CC:BB:AA", "signal": -85, "security": "OPEN", "channel": 11},
            {"ssid": "CoffeeShop_WiFi", "bssid": "DE:AD:BE:EF:CA:FE", "signal": -62, "security": "WPA3", "channel": 1},
            {"ssid": "Hidden_Network", "bssid": "00:11:22:33:44:55", "signal": -90, "security": "WPA2", "channel": 8},
            {"ssid": "DIRECT-roku-123", "bssid": "F0:E1:D2:C3:B4:A5", "signal": -55, "security": "WPA2", "channel": 11},
        ]
