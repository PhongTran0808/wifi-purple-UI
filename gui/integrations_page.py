import customtkinter as ctk
import subprocess
import os
import json
import threading
import tempfile
from gui.navigation import NavigationBar

class MetasploitIntegration:
    """Metasploit Framework integration"""
    
    def __init__(self):
        self.msfconsole_available = self.check_metasploit()
    
    def check_metasploit(self):
        """Check if Metasploit is installed"""
        try:
            result = subprocess.run(['which', 'msfconsole'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def run_auxiliary_scan(self, target_range):
        """Run Metasploit auxiliary scanner"""
        if not self.msfconsole_available:
            return "Metasploit not installed"
        
        try:
            # Create resource script
            script_content = f"""
use auxiliary/scanner/discovery/udp_sweep
set RHOSTS {target_range}
run
exit
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rc', delete=False) as f:
                f.write(script_content)
                script_file = f.name
            
            # Run msfconsole with resource script
            cmd = ['msfconsole', '-q', '-r', script_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Cleanup
            os.unlink(script_file)
            
            return result.stdout
            
        except Exception as e:
            return f"Error running Metasploit scan: {e}"
    
    def exploit_wps_vulnerability(self, target_bssid):
        """Exploit WPS vulnerability using Metasploit"""
        if not self.msfconsole_available:
            return "Metasploit not installed"
        
        script_content = f"""
use auxiliary/scanner/http/wps_brute_pin
set RHOST {target_bssid}
run
exit
"""
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rc', delete=False) as f:
                f.write(script_content)
                script_file = f.name
            
            cmd = ['msfconsole', '-q', '-r', script_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            os.unlink(script_file)
            return result.stdout
            
        except Exception as e:
            return f"Error running WPS exploit: {e}"

class NmapIntegration:
    """Nmap network scanner integration"""
    
    def __init__(self):
        self.nmap_available = self.check_nmap()
    
    def check_nmap(self):
        """Check if Nmap is installed"""
        try:
            result = subprocess.run(['which', 'nmap'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def port_scan(self, target, ports="1-1000"):
        """Perform port scan on target"""
        if not self.nmap_available:
            return "Nmap not installed"
        
        try:
            cmd = ['nmap', '-p', ports, '-sS', '-O', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.stdout
        except Exception as e:
            return f"Error running port scan: {e}"
    
    def service_detection(self, target):
        """Detect services on target"""
        if not self.nmap_available:
            return "Nmap not installed"
        
        try:
            cmd = ['nmap', '-sV', '-sC', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            return result.stdout
        except Exception as e:
            return f"Error detecting services: {e}"
    
    def vulnerability_scan(self, target):
        """Run vulnerability scan using NSE scripts"""
        if not self.nmap_available:
            return "Nmap not installed"
        
        try:
            cmd = ['nmap', '--script', 'vuln', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.stdout
        except Exception as e:
            return f"Error running vulnerability scan: {e}"

class WiresharkIntegration:
    """Wireshark packet analysis integration"""
    
    def __init__(self):
        self.wireshark_available = self.check_wireshark()
        self.tshark_available = self.check_tshark()
    
    def check_wireshark(self):
        """Check if Wireshark is installed"""
        try:
            result = subprocess.run(['which', 'wireshark'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def check_tshark(self):
        """Check if tshark is installed"""
        try:
            result = subprocess.run(['which', 'tshark'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def capture_packets(self, interface, duration=60):
        """Capture packets using tshark"""
        if not self.tshark_available:
            return "tshark not installed"
        
        try:
            output_file = f"/tmp/wifi-purple/capture_{int(time.time())}.pcap"
            cmd = ['tshark', '-i', interface, '-a', f'duration:{duration}', '-w', output_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration+10)
            
            if os.path.exists(output_file):
                return f"Capture saved to: {output_file}"
            else:
                return "Capture failed"
                
        except Exception as e:
            return f"Error capturing packets: {e}"
    
    def analyze_handshake(self, pcap_file):
        """Analyze handshake in pcap file"""
        if not self.tshark_available:
            return "tshark not installed"
        
        try:
            # Look for EAPOL frames (handshake)
            cmd = ['tshark', '-r', pcap_file, '-Y', 'eapol', '-T', 'fields', 
                   '-e', 'frame.time', '-e', 'wlan.sa', '-e', 'wlan.da']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
            
        except Exception as e:
            return f"Error analyzing handshake: {e}"
    
    def open_wireshark(self, pcap_file=None):
        """Open Wireshark GUI"""
        if not self.wireshark_available:
            return "Wireshark not installed"
        
        try:
            if pcap_file and os.path.exists(pcap_file):
                subprocess.Popen(['wireshark', pcap_file])
                return f"Opening {pcap_file} in Wireshark"
            else:
                subprocess.Popen(['wireshark'])
                return "Opening Wireshark"
        except Exception as e:
            return f"Error opening Wireshark: {e}"

class OSINTTools:
    """Open Source Intelligence tools"""
    
    def __init__(self):
        self.tools_available = self.check_osint_tools()
    
    def check_osint_tools(self):
        """Check available OSINT tools"""
        tools = {}
        tool_list = ['whois', 'dig', 'nslookup', 'curl']
        
        for tool in tool_list:
            try:
                result = subprocess.run(['which', tool], capture_output=True)
                tools[tool] = result.returncode == 0
            except:
                tools[tool] = False
        
        return tools
    
    def whois_lookup(self, domain):
        """Perform WHOIS lookup"""
        if not self.tools_available.get('whois', False):
            return "whois not installed"
        
        try:
            cmd = ['whois', domain]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            return f"Error performing WHOIS lookup: {e}"
    
    def dns_lookup(self, domain):
        """Perform DNS lookup"""
        if not self.tools_available.get('dig', False):
            return "dig not installed"
        
        try:
            cmd = ['dig', '+short', domain]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            return f"Error performing DNS lookup: {e}"
    
    def reverse_dns(self, ip):
        """Perform reverse DNS lookup"""
        if not self.tools_available.get('dig', False):
            return "dig not installed"
        
        try:
            cmd = ['dig', '+short', '-x', ip]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            return f"Error performing reverse DNS: {e}"
    
    def geolocation_lookup(self, ip):
        """Get geolocation information for IP"""
        try:
            import requests
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
            data = response.json()
            
            if data['status'] == 'success':
                return f"""
Location: {data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}, {data.get('country', 'Unknown')}
ISP: {data.get('isp', 'Unknown')}
Organization: {data.get('org', 'Unknown')}
Coordinates: {data.get('lat', 'Unknown')}, {data.get('lon', 'Unknown')}
Timezone: {data.get('timezone', 'Unknown')}
"""
            else:
                return "Geolocation lookup failed"
                
        except Exception as e:
            return f"Error performing geolocation lookup: {e}"

class IntegrationsPage(ctk.CTkFrame):
    """External integrations page"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Initialize integrations
        self.metasploit = MetasploitIntegration()
        self.nmap = NmapIntegration()
        self.wireshark = WiresharkIntegration()
        self.osint = OSINTTools()
        
        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Integrations")
        
        # Title
        title = ctk.CTkLabel(self, text="🔗 External Integrations", font=("Roboto", 24, "bold"))
        title.pack(pady=20)
        
        # Main content
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Configure grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Metasploit section
        self.create_metasploit_section(main_frame)
        
        # Nmap section
        self.create_nmap_section(main_frame)
        
        # Wireshark section
        self.create_wireshark_section(main_frame)
        
        # OSINT section
        self.create_osint_section(main_frame)
    
    def create_metasploit_section(self, parent):
        """Create Metasploit integration section"""
        msf_frame = ctk.CTkFrame(parent)
        msf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(msf_frame, text="🎯 Metasploit Framework", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Status
        status_color = "green" if self.metasploit.msfconsole_available else "red"
        status_text = "Available" if self.metasploit.msfconsole_available else "Not Installed"
        status_label = ctk.CTkLabel(msf_frame, text=f"Status: {status_text}", text_color=status_color)
        status_label.pack(pady=5)
        
        # Target input
        self.msf_target_entry = ctk.CTkEntry(msf_frame, placeholder_text="Target IP/Range")
        self.msf_target_entry.pack(pady=10, padx=20, fill="x")
        
        # Buttons
        ctk.CTkButton(
            msf_frame, text="🔍 Auxiliary Scan",
            command=self.run_msf_auxiliary_scan
        ).pack(pady=5)
        
        ctk.CTkButton(
            msf_frame, text="💥 WPS Exploit",
            command=self.run_msf_wps_exploit
        ).pack(pady=5)
        
        # Results
        self.msf_results = ctk.CTkTextbox(msf_frame, height=150)
        self.msf_results.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_nmap_section(self, parent):
        """Create Nmap integration section"""
        nmap_frame = ctk.CTkFrame(parent)
        nmap_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(nmap_frame, text="🌐 Nmap Scanner", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Status
        status_color = "green" if self.nmap.nmap_available else "red"
        status_text = "Available" if self.nmap.nmap_available else "Not Installed"
        status_label = ctk.CTkLabel(nmap_frame, text=f"Status: {status_text}", text_color=status_color)
        status_label.pack(pady=5)
        
        # Target input
        self.nmap_target_entry = ctk.CTkEntry(nmap_frame, placeholder_text="Target IP/Domain")
        self.nmap_target_entry.pack(pady=10, padx=20, fill="x")
        
        # Buttons
        ctk.CTkButton(
            nmap_frame, text="🔍 Port Scan",
            command=self.run_nmap_port_scan
        ).pack(pady=5)
        
        ctk.CTkButton(
            nmap_frame, text="🔧 Service Detection",
            command=self.run_nmap_service_scan
        ).pack(pady=5)
        
        ctk.CTkButton(
            nmap_frame, text="🛡️ Vulnerability Scan",
            command=self.run_nmap_vuln_scan
        ).pack(pady=5)
        
        # Results
        self.nmap_results = ctk.CTkTextbox(nmap_frame, height=150)
        self.nmap_results.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_wireshark_section(self, parent):
        """Create Wireshark integration section"""
        ws_frame = ctk.CTkFrame(parent)
        ws_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(ws_frame, text="🦈 Wireshark Analysis", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Status
        ws_status = "Available" if self.wireshark.wireshark_available else "Not Installed"
        tshark_status = "Available" if self.wireshark.tshark_available else "Not Installed"
        status_label = ctk.CTkLabel(ws_frame, text=f"Wireshark: {ws_status} | tshark: {tshark_status}")
        status_label.pack(pady=5)
        
        # Interface input
        self.ws_interface_entry = ctk.CTkEntry(ws_frame, placeholder_text="Interface (e.g., wlan0mon)")
        self.ws_interface_entry.pack(pady=10, padx=20, fill="x")
        
        # Buttons
        ctk.CTkButton(
            ws_frame, text="📡 Start Capture",
            command=self.start_packet_capture
        ).pack(pady=5)
        
        ctk.CTkButton(
            ws_frame, text="🔍 Analyze Handshake",
            command=self.analyze_handshake
        ).pack(pady=5)
        
        ctk.CTkButton(
            ws_frame, text="🖥️ Open Wireshark",
            command=self.open_wireshark_gui
        ).pack(pady=5)
        
        # Results
        self.ws_results = ctk.CTkTextbox(ws_frame, height=150)
        self.ws_results.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_osint_section(self, parent):
        """Create OSINT tools section"""
        osint_frame = ctk.CTkFrame(parent)
        osint_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(osint_frame, text="🕵️ OSINT Tools", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Status
        available_tools = [tool for tool, available in self.osint.tools_available.items() if available]
        status_text = f"Available: {', '.join(available_tools)}" if available_tools else "No tools available"
        status_label = ctk.CTkLabel(osint_frame, text=status_text)
        status_label.pack(pady=5)
        
        # Target input
        self.osint_target_entry = ctk.CTkEntry(osint_frame, placeholder_text="Domain/IP")
        self.osint_target_entry.pack(pady=10, padx=20, fill="x")
        
        # Buttons
        ctk.CTkButton(
            osint_frame, text="🔍 WHOIS Lookup",
            command=self.run_whois_lookup
        ).pack(pady=5)
        
        ctk.CTkButton(
            osint_frame, text="🌐 DNS Lookup",
            command=self.run_dns_lookup
        ).pack(pady=5)
        
        ctk.CTkButton(
            osint_frame, text="📍 Geolocation",
            command=self.run_geolocation
        ).pack(pady=5)
        
        # Results
        self.osint_results = ctk.CTkTextbox(osint_frame, height=150)
        self.osint_results.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Metasploit methods
    def run_msf_auxiliary_scan(self):
        """Run Metasploit auxiliary scan"""
        target = self.msf_target_entry.get()
        if not target:
            self.msf_results.insert("end", "Please enter a target\\n")
            return
        
        self.msf_results.insert("end", f"Running auxiliary scan on {target}...\\n")
        
        def scan_thread():
            result = self.metasploit.run_auxiliary_scan(target)
            self.after(0, lambda: self.msf_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def run_msf_wps_exploit(self):
        """Run Metasploit WPS exploit"""
        target = self.msf_target_entry.get()
        if not target:
            self.msf_results.insert("end", "Please enter a target BSSID\\n")
            return
        
        self.msf_results.insert("end", f"Running WPS exploit on {target}...\\n")
        
        def exploit_thread():
            result = self.metasploit.exploit_wps_vulnerability(target)
            self.after(0, lambda: self.msf_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=exploit_thread, daemon=True).start()
    
    # Nmap methods
    def run_nmap_port_scan(self):
        """Run Nmap port scan"""
        target = self.nmap_target_entry.get()
        if not target:
            self.nmap_results.insert("end", "Please enter a target\\n")
            return
        
        self.nmap_results.insert("end", f"Port scanning {target}...\\n")
        
        def scan_thread():
            result = self.nmap.port_scan(target)
            self.after(0, lambda: self.nmap_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def run_nmap_service_scan(self):
        """Run Nmap service detection"""
        target = self.nmap_target_entry.get()
        if not target:
            self.nmap_results.insert("end", "Please enter a target\\n")
            return
        
        self.nmap_results.insert("end", f"Detecting services on {target}...\\n")
        
        def scan_thread():
            result = self.nmap.service_detection(target)
            self.after(0, lambda: self.nmap_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def run_nmap_vuln_scan(self):
        """Run Nmap vulnerability scan"""
        target = self.nmap_target_entry.get()
        if not target:
            self.nmap_results.insert("end", "Please enter a target\\n")
            return
        
        self.nmap_results.insert("end", f"Vulnerability scanning {target}...\\n")
        
        def scan_thread():
            result = self.nmap.vulnerability_scan(target)
            self.after(0, lambda: self.nmap_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    # Wireshark methods
    def start_packet_capture(self):
        """Start packet capture"""
        interface = self.ws_interface_entry.get()
        if not interface:
            self.ws_results.insert("end", "Please enter an interface\\n")
            return
        
        self.ws_results.insert("end", f"Starting packet capture on {interface}...\\n")
        
        def capture_thread():
            result = self.wireshark.capture_packets(interface, 60)
            self.after(0, lambda: self.ws_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=capture_thread, daemon=True).start()
    
    def analyze_handshake(self):
        """Analyze handshake in pcap file"""
        # For demo, use a sample file path
        pcap_file = "/tmp/wifi-purple/latest_capture.pcap"
        
        self.ws_results.insert("end", f"Analyzing handshake in {pcap_file}...\\n")
        
        def analyze_thread():
            result = self.wireshark.analyze_handshake(pcap_file)
            self.after(0, lambda: self.ws_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def open_wireshark_gui(self):
        """Open Wireshark GUI"""
        result = self.wireshark.open_wireshark()
        self.ws_results.insert("end", f"{result}\\n")
    
    # OSINT methods
    def run_whois_lookup(self):
        """Run WHOIS lookup"""
        target = self.osint_target_entry.get()
        if not target:
            self.osint_results.insert("end", "Please enter a domain\\n")
            return
        
        self.osint_results.insert("end", f"WHOIS lookup for {target}...\\n")
        
        def lookup_thread():
            result = self.osint.whois_lookup(target)
            self.after(0, lambda: self.osint_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=lookup_thread, daemon=True).start()
    
    def run_dns_lookup(self):
        """Run DNS lookup"""
        target = self.osint_target_entry.get()
        if not target:
            self.osint_results.insert("end", "Please enter a domain\\n")
            return
        
        self.osint_results.insert("end", f"DNS lookup for {target}...\\n")
        
        def lookup_thread():
            result = self.osint.dns_lookup(target)
            self.after(0, lambda: self.osint_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=lookup_thread, daemon=True).start()
    
    def run_geolocation(self):
        """Run geolocation lookup"""
        target = self.osint_target_entry.get()
        if not target:
            self.osint_results.insert("end", "Please enter an IP address\\n")
            return
        
        self.osint_results.insert("end", f"Geolocation lookup for {target}...\\n")
        
        def lookup_thread():
            result = self.osint.geolocation_lookup(target)
            self.after(0, lambda: self.osint_results.insert("end", f"{result}\\n\\n"))
        
        threading.Thread(target=lookup_thread, daemon=True).start()