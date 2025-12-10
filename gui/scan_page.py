import customtkinter as ctk
from PIL import Image, ImageTk

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

    def __init__(self, parent):
        super().__init__(parent)

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

    def start_scan(self):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Placeholder text
        loading_label = ctk.CTkLabel(self.result_frame, text="Đang quét, vui lòng chờ...")
        loading_label.pack(pady=20)
        
        # Simulate a delay for scanning
        self.after(2000, self.display_results)

    def display_results(self):
        # Clear "loading" text
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        networks = self._simulate_scan_results()
        
        # Create and display a WifiNetworkItem for each network
        for network in networks:
            item = WifiNetworkItem(self.result_frame, network)
            item.pack(pady=5, padx=10, fill="x")

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
