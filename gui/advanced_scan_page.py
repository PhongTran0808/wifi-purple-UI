import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import folium
import webbrowser
import tempfile
import os
import json
import requests
import subprocess
from gui.navigation import NavigationBar

class VendorDatabase:
    """OUI Vendor identification database"""
    
    def __init__(self):
        self.oui_db = {}
        self.load_oui_database()
    
    def load_oui_database(self):
        """Load OUI database for vendor identification"""
        # Sample OUI database - in production, load from IEEE OUI file
        self.oui_db = {
            "00:1B:63": "Apple",
            "00:26:BB": "Apple", 
            "3C:15:C2": "Apple",
            "00:23:12": "Cisco",
            "00:1E:58": "Cisco",
            "00:50:56": "VMware",
            "08:00:27": "VirtualBox",
            "00:0C:29": "VMware",
            "00:1C:B3": "Netgear",
            "00:26:F2": "Netgear",
            "E8:DE:27": "TP-Link",
            "F4:F2:6D": "TP-Link",
            "00:22:B0": "D-Link",
            "00:26:5A": "D-Link",
            "00:1F:3F": "Linksys",
            "68:7F:74": "Linksys"
        }
    
    def identify_vendor(self, mac_address):
        """Identify vendor from MAC address"""
        if not mac_address or len(mac_address) < 8:
            return "Unknown"
        
        oui = mac_address[:8].upper()
        return self.oui_db.get(oui, "Unknown")

class VulnerabilityScanner:
    """WiFi vulnerability scanner"""
    
    def __init__(self):
        self.vulnerabilities = []
    
    def scan_vulnerabilities(self, network_info):
        """Scan for common WiFi vulnerabilities"""
        vulns = []
        
        # Check for weak encryption
        security = network_info.get('security', 'OPEN')
        if security == 'OPEN':
            vulns.append({
                'type': 'CRITICAL',
                'name': 'Open Network',
                'description': 'Network has no encryption'
            })
        elif 'WEP' in security:
            vulns.append({
                'type': 'HIGH',
                'name': 'WEP Encryption',
                'description': 'WEP is easily crackable'
            })
        elif 'WPS' in security:
            vulns.append({
                'type': 'MEDIUM',
                'name': 'WPS Enabled',
                'description': 'WPS PIN attack possible'
            })
        
        # Check for default credentials
        ssid = network_info.get('ssid', '')
        if any(default in ssid.lower() for default in ['linksys', 'netgear', 'dlink', 'tplink']):
            vulns.append({
                'type': 'MEDIUM',
                'name': 'Default SSID',
                'description': 'May use default credentials'
            })
        
        # Check signal strength for physical security
        signal = network_info.get('signal', -100)
        if signal > -30:
            vulns.append({
                'type': 'LOW',
                'name': 'Strong Signal',
                'description': 'Network accessible from far distance'
            })
        
        return vulns

class GPSMapper:
    """GPS location mapping for WiFi networks"""
    
    def __init__(self):
        self.locations = {}
        self.load_locations()
    
    def load_locations(self):
        """Load saved GPS locations"""
        try:
            location_file = '/tmp/wifi-purple/gps_locations.json'
            if os.path.exists(location_file):
                with open(location_file, 'r') as f:
                    self.locations = json.load(f)
        except Exception as e:
            print(f"Error loading GPS locations: {e}")
    
    def save_locations(self):
        """Save GPS locations to file"""
        try:
            location_file = '/tmp/wifi-purple/gps_locations.json'
            os.makedirs(os.path.dirname(location_file), exist_ok=True)
            with open(location_file, 'w') as f:
                json.dump(self.locations, f, indent=2)
        except Exception as e:
            print(f"Error saving GPS locations: {e}")
    
    def get_current_location(self):
        """Get current GPS location (mock implementation)"""
        # In real implementation, use GPS module or IP geolocation
        return {"lat": 21.0285, "lon": 105.8542}  # Hanoi coordinates
    
    def add_network_location(self, bssid, ssid, location=None):
        """Add network location to database"""
        if location is None:
            location = self.get_current_location()
        
        self.locations[bssid] = {
            'ssid': ssid,
            'lat': location['lat'],
            'lon': location['lon'],
            'timestamp': str(datetime.now())
        }
        self.save_locations()
    
    def create_map(self, networks):
        """Create interactive map with network locations"""
        # Get current location as map center
        center_location = self.get_current_location()
        
        # Create folium map
        m = folium.Map(
            location=[center_location['lat'], center_location['lon']],
            zoom_start=15,
            tiles='OpenStreetMap'
        )
        
        # Add networks to map
        for network in networks:
            bssid = network.get('bssid', '')
            if bssid in self.locations:
                loc = self.locations[bssid]
                
                # Color based on security
                security = network.get('security', 'OPEN')
                if security == 'OPEN':
                    color = 'red'
                elif 'WEP' in security:
                    color = 'orange'
                else:
                    color = 'green'
                
                # Create popup text
                popup_text = f"""
                <b>{network.get('ssid', 'Hidden')}</b><br>
                BSSID: {bssid}<br>
                Security: {security}<br>
                Channel: {network.get('channel', 'N/A')}<br>
                Signal: {network.get('signal', 'N/A')} dBm
                """
                
                folium.Marker(
                    [loc['lat'], loc['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    icon=folium.Icon(color=color, icon='wifi', prefix='fa')
                ).add_to(m)
        
        # Save map to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        m.save(temp_file.name)
        return temp_file.name

class HiddenNetworkDetector:
    """Hidden network detection"""
    
    def __init__(self):
        self.hidden_networks = []
    
    def detect_hidden_networks(self, interface):
        """Detect hidden networks using probe requests"""
        try:
            # Use airodump-ng to capture probe requests
            cmd = f"timeout 30 airodump-ng {interface} --output-format csv --write /tmp/hidden_scan"
            subprocess.run(cmd, shell=True, capture_output=True)
            
            # Parse results for hidden networks
            hidden_networks = []
            csv_file = "/tmp/hidden_scan-01.csv"
            
            if os.path.exists(csv_file):
                with open(csv_file, 'r') as f:
                    lines = f.readlines()
                
                for line in lines:
                    if line.strip() and not line.startswith('BSSID'):
                        parts = line.split(',')
                        if len(parts) >= 14:
                            bssid = parts[0].strip()
                            essid = parts[13].strip()
                            
                            if not essid or essid == ' ':
                                hidden_networks.append({
                                    'bssid': bssid,
                                    'channel': parts[3].strip(),
                                    'security': parts[5].strip(),
                                    'signal': parts[8].strip()
                                })
            
            return hidden_networks
            
        except Exception as e:
            print(f"Error detecting hidden networks: {e}")
            return []

class SignalHeatmap:
    """Signal strength heatmap generator"""
    
    def __init__(self):
        self.signal_data = []
    
    def collect_signal_data(self, networks, location):
        """Collect signal strength data with location"""
        for network in networks:
            self.signal_data.append({
                'bssid': network.get('bssid'),
                'ssid': network.get('ssid'),
                'signal': network.get('signal', -100),
                'lat': location['lat'],
                'lon': location['lon']
            })
    
    def generate_heatmap(self):
        """Generate signal strength heatmap"""
        if not self.signal_data:
            return None
        
        # Create base map
        center_lat = sum(d['lat'] for d in self.signal_data) / len(self.signal_data)
        center_lon = sum(d['lon'] for d in self.signal_data) / len(self.signal_data)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
        
        # Prepare heatmap data
        heat_data = []
        for data in self.signal_data:
            # Convert signal strength to heat intensity (stronger signal = higher intensity)
            intensity = max(0, (data['signal'] + 100) / 100)  # Normalize -100 to 0 dBm to 0-1
            heat_data.append([data['lat'], data['lon'], intensity])
        
        # Add heatmap layer
        from folium.plugins import HeatMap
        HeatMap(heat_data, radius=20, blur=15, max_zoom=1).add_to(m)
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        m.save(temp_file.name)
        return temp_file.name

class AdvancedScanPage(ctk.CTkFrame):
    """Advanced WiFi scanning features"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Initialize components
        self.vendor_db = VendorDatabase()
        self.vuln_scanner = VulnerabilityScanner()
        self.gps_mapper = GPSMapper()
        self.hidden_detector = HiddenNetworkDetector()
        self.heatmap_generator = SignalHeatmap()
        
        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Advanced Scan")
        
        # Title
        title = ctk.CTkLabel(self, text="🔍 Advanced WiFi Scanner", font=("Roboto", 24, "bold"))
        title.pack(pady=20)
        
        # Control panel
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        # Scan options
        options_frame = ctk.CTkFrame(control_frame)
        options_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(options_frame, text="Scan Options:", font=("Roboto", 16, "bold")).pack(pady=10)
        
        # Checkboxes for scan options
        self.vendor_scan = ctk.CTkCheckBox(options_frame, text="🏢 Vendor Identification")
        self.vendor_scan.pack(pady=5, anchor="w", padx=20)
        
        self.vuln_scan = ctk.CTkCheckBox(options_frame, text="🛡️ Vulnerability Scan")
        self.vuln_scan.pack(pady=5, anchor="w", padx=20)
        
        self.gps_mapping = ctk.CTkCheckBox(options_frame, text="🗺️ GPS Mapping")
        self.gps_mapping.pack(pady=5, anchor="w", padx=20)
        
        self.hidden_scan = ctk.CTkCheckBox(options_frame, text="👻 Hidden Network Detection")
        self.hidden_scan.pack(pady=5, anchor="w", padx=20)
        
        self.heatmap_gen = ctk.CTkCheckBox(options_frame, text="🌡️ Signal Heatmap")
        self.heatmap_gen.pack(pady=5, anchor="w", padx=20)
        
        # Control buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        self.scan_button = ctk.CTkButton(
            button_frame, text="🚀 Start Advanced Scan", width=200,
            command=self.start_advanced_scan
        )
        self.scan_button.pack(side="left", padx=10)
        
        self.map_button = ctk.CTkButton(
            button_frame, text="🗺️ View Map", width=150,
            command=self.show_map, state="disabled"
        )
        self.map_button.pack(side="left", padx=10)
        
        self.heatmap_button = ctk.CTkButton(
            button_frame, text="🌡️ View Heatmap", width=150,
            command=self.show_heatmap, state="disabled"
        )
        self.heatmap_button.pack(side="left", padx=10)
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Scan Results")
        self.results_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.scan_results = []
    
    def start_advanced_scan(self):
        """Start advanced WiFi scan"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        self.scan_button.configure(state="disabled", text="🔄 Scanning...")
        
        # Start scan in background thread
        import threading
        threading.Thread(target=self.perform_advanced_scan, daemon=True).start()
    
    def perform_advanced_scan(self):
        """Perform the actual advanced scan"""
        try:
            # Get basic scan results first
            networks = self.get_basic_scan_results()
            
            # Apply advanced features
            enhanced_networks = []
            current_location = self.gps_mapper.get_current_location()
            
            for network in networks:
                enhanced_network = network.copy()
                
                # Vendor identification
                if self.vendor_scan.get():
                    vendor = self.vendor_db.identify_vendor(network.get('bssid', ''))
                    enhanced_network['vendor'] = vendor
                
                # Vulnerability scanning
                if self.vuln_scan.get():
                    vulns = self.vuln_scanner.scan_vulnerabilities(network)
                    enhanced_network['vulnerabilities'] = vulns
                
                # GPS mapping
                if self.gps_mapping.get():
                    self.gps_mapper.add_network_location(
                        network.get('bssid', ''),
                        network.get('ssid', ''),
                        current_location
                    )
                
                # Signal heatmap data collection
                if self.heatmap_gen.get():
                    self.heatmap_generator.collect_signal_data([network], current_location)
                
                enhanced_networks.append(enhanced_network)
            
            # Hidden network detection
            if self.hidden_scan.get():
                hidden_networks = self.hidden_detector.detect_hidden_networks("wlan0mon")
                for hidden in hidden_networks:
                    hidden['ssid'] = '[Hidden Network]'
                    hidden['vendor'] = self.vendor_db.identify_vendor(hidden.get('bssid', ''))
                    enhanced_networks.append(hidden)
            
            self.scan_results = enhanced_networks
            
            # Update UI in main thread
            self.after(0, self.display_advanced_results)
            
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Scan error: {e}"))
    
    def get_basic_scan_results(self):
        """Get basic scan results (mock data for demo)"""
        return [
            {
                "ssid": "HomeWiFi_5G", "bssid": "00:1B:63:84:45:E6", 
                "signal": -45, "security": "WPA2", "channel": 149
            },
            {
                "ssid": "CoffeeShop_Guest", "bssid": "E8:DE:27:12:34:56",
                "signal": -62, "security": "OPEN", "channel": 6
            },
            {
                "ssid": "Linksys_Default", "bssid": "00:1F:3F:AA:BB:CC",
                "signal": -78, "security": "WEP", "channel": 11
            }
        ]
    
    def display_advanced_results(self):
        """Display enhanced scan results"""
        self.scan_button.configure(state="normal", text="🚀 Start Advanced Scan")
        
        if self.gps_mapping.get():
            self.map_button.configure(state="normal")
        
        if self.heatmap_gen.get():
            self.heatmap_button.configure(state="normal")
        
        for network in self.scan_results:
            self.create_enhanced_network_widget(network)
    
    def create_enhanced_network_widget(self, network):
        """Create enhanced network display widget"""
        network_frame = ctk.CTkFrame(self.results_frame)
        network_frame.pack(pady=10, padx=10, fill="x")
        
        # Main info frame
        main_info = ctk.CTkFrame(network_frame, fg_color="transparent")
        main_info.pack(fill="x", padx=10, pady=10)
        
        # SSID and basic info
        ssid_label = ctk.CTkLabel(
            main_info, text=network.get('ssid', 'Hidden'),
            font=("Roboto", 16, "bold")
        )
        ssid_label.pack(anchor="w")
        
        basic_info = f"BSSID: {network.get('bssid', 'N/A')} | Channel: {network.get('channel', 'N/A')} | Signal: {network.get('signal', 'N/A')} dBm"
        basic_label = ctk.CTkLabel(main_info, text=basic_info, font=("Roboto", 12))
        basic_label.pack(anchor="w")
        
        # Vendor info
        if 'vendor' in network:
            vendor_label = ctk.CTkLabel(
                main_info, text=f"🏢 Vendor: {network['vendor']}",
                font=("Roboto", 12), text_color="cyan"
            )
            vendor_label.pack(anchor="w")
        
        # Vulnerabilities
        if 'vulnerabilities' in network and network['vulnerabilities']:
            vuln_frame = ctk.CTkFrame(network_frame)
            vuln_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(vuln_frame, text="🛡️ Vulnerabilities:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=5)
            
            for vuln in network['vulnerabilities']:
                color = {"CRITICAL": "#F44336", "HIGH": "#FF9800", "MEDIUM": "#FFC107", "LOW": "#4CAF50"}
                vuln_color = color.get(vuln['type'], "white")
                
                vuln_text = f"[{vuln['type']}] {vuln['name']}: {vuln['description']}"
                vuln_label = ctk.CTkLabel(
                    vuln_frame, text=vuln_text,
                    font=("Roboto", 11), text_color=vuln_color
                )
                vuln_label.pack(anchor="w", padx=20, pady=2)
    
    def show_map(self):
        """Show GPS map of networks"""
        try:
            map_file = self.gps_mapper.create_map(self.scan_results)
            webbrowser.open(f'file://{map_file}')
        except Exception as e:
            self.show_error(f"Error creating map: {e}")
    
    def show_heatmap(self):
        """Show signal strength heatmap"""
        try:
            heatmap_file = self.heatmap_generator.generate_heatmap()
            if heatmap_file:
                webbrowser.open(f'file://{heatmap_file}')
            else:
                self.show_error("No heatmap data available")
        except Exception as e:
            self.show_error(f"Error creating heatmap: {e}")
    
    def show_error(self, message):
        """Show error message"""
        error_label = ctk.CTkLabel(
            self.results_frame, text=f"❌ {message}",
            font=("Roboto", 14), text_color="red"
        )
        error_label.pack(pady=20)