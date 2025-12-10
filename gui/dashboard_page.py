import customtkinter as ctk
import psutil
import threading
import time
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from gui.navigation import NavigationBar

class SystemMonitor(ctk.CTkFrame):
    """Real-time system monitoring widget"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.monitoring = False
        
        # Title
        title = ctk.CTkLabel(self, text="📊 System Monitor", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        # CPU Usage
        self.cpu_label = ctk.CTkLabel(stats_frame, text="CPU: 0%", font=("Roboto", 14))
        self.cpu_label.pack(pady=5)
        
        self.cpu_progress = ctk.CTkProgressBar(stats_frame)
        self.cpu_progress.pack(pady=5, padx=20, fill="x")
        
        # RAM Usage
        self.ram_label = ctk.CTkLabel(stats_frame, text="RAM: 0%", font=("Roboto", 14))
        self.ram_label.pack(pady=5)
        
        self.ram_progress = ctk.CTkProgressBar(stats_frame)
        self.ram_progress.pack(pady=5, padx=20, fill="x")
        
        # Network Interface Status
        self.interface_label = ctk.CTkLabel(stats_frame, text="Interface: N/A", font=("Roboto", 14))
        self.interface_label.pack(pady=5)
        
        # Start monitoring
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        self.monitoring = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Get system stats
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                ram_percent = memory.percent
                
                # Get network interface status
                interface_status = self.get_interface_status()
                
                # Update UI in main thread
                self.after(0, self.update_ui, cpu_percent, ram_percent, interface_status)
                
                time.sleep(2)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)
    
    def get_interface_status(self):
        """Get WiFi interface status"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            interface = config['settings']['default_interface']
            
            # Check if interface exists and is up
            import subprocess
            result = subprocess.run(['ip', 'link', 'show', interface], 
                                  capture_output=True, text=True)
            
            if 'UP' in result.stdout:
                return f"{interface}: UP"
            else:
                return f"{interface}: DOWN"
                
        except Exception:
            return "Interface: Unknown"
    
    def update_ui(self, cpu_percent, ram_percent, interface_status):
        """Update UI elements"""
        # Update CPU
        self.cpu_label.configure(text=f"CPU: {cpu_percent:.1f}%")
        self.cpu_progress.set(cpu_percent / 100)
        
        # Update RAM
        self.ram_label.configure(text=f"RAM: {ram_percent:.1f}%")
        self.ram_progress.set(ram_percent / 100)
        
        # Update interface
        self.interface_label.configure(text=interface_status)

class NetworkStatsChart(ctk.CTkFrame):
    """Network statistics chart"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        title = ctk.CTkLabel(self, text="📈 Network Statistics", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor='#1a1a1a')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(colors='white')
        self.ax.set_xlabel('Time', color='white')
        self.ax.set_ylabel('Networks Found', color='white')
        self.ax.set_title('WiFi Networks Over Time', color='white')
        
        # Sample data
        self.times = []
        self.network_counts = []
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load historical data
        self.load_network_stats()
        self.update_chart()
    
    def load_network_stats(self):
        """Load network statistics from file"""
        try:
            stats_file = '/tmp/wifi-purple/network_stats.json'
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                
                for entry in data[-20:]:  # Last 20 entries
                    self.times.append(datetime.fromisoformat(entry['timestamp']))
                    self.network_counts.append(entry['count'])
            else:
                # Generate sample data
                now = datetime.now()
                for i in range(10):
                    self.times.append(now - timedelta(minutes=i*5))
                    self.network_counts.append(5 + i % 8)
                self.times.reverse()
                self.network_counts.reverse()
        except Exception as e:
            print(f"Error loading network stats: {e}")
    
    def update_chart(self):
        """Update the chart"""
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        
        if self.times and self.network_counts:
            self.ax.plot(self.times, self.network_counts, 'cyan', linewidth=2, marker='o')
            self.ax.fill_between(self.times, self.network_counts, alpha=0.3, color='cyan')
        
        self.ax.set_xlabel('Time', color='white')
        self.ax.set_ylabel('Networks Found', color='white')
        self.ax.set_title('WiFi Networks Over Time', color='white')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        self.canvas.draw()

class AttackHistory(ctk.CTkFrame):
    """Attack history widget"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        title = ctk.CTkLabel(self, text="🎯 Attack History", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # History list
        self.history_frame = ctk.CTkScrollableFrame(self, height=200)
        self.history_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load attack history
        self.load_attack_history()
    
    def load_attack_history(self):
        """Load attack history from file"""
        try:
            history_file = '/tmp/wifi-purple/attack_history.json'
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    attacks = json.load(f)
                
                for attack in attacks[-10:]:  # Last 10 attacks
                    self.add_attack_entry(attack)
            else:
                # Sample data
                sample_attacks = [
                    {"type": "Deauth", "target": "HomeWiFi_5G", "timestamp": "2024-12-10 14:30", "status": "Success"},
                    {"type": "Evil Twin", "target": "CoffeeShop", "timestamp": "2024-12-10 13:15", "status": "Failed"},
                    {"type": "Handshake", "target": "Neighbor_WiFi", "timestamp": "2024-12-10 12:45", "status": "Success"},
                ]
                
                for attack in sample_attacks:
                    self.add_attack_entry(attack)
                    
        except Exception as e:
            print(f"Error loading attack history: {e}")
    
    def add_attack_entry(self, attack):
        """Add attack entry to history"""
        entry_frame = ctk.CTkFrame(self.history_frame)
        entry_frame.pack(pady=5, padx=10, fill="x")
        
        # Status indicator
        status_color = "#4CAF50" if attack['status'] == 'Success' else "#F44336"
        status_indicator = ctk.CTkLabel(
            entry_frame, text="●", 
            font=("Roboto", 20), text_color=status_color
        )
        status_indicator.pack(side="left", padx=10)
        
        # Attack info
        info_text = f"{attack['type']} → {attack['target']}\n{attack['timestamp']}"
        info_label = ctk.CTkLabel(entry_frame, text=info_text, font=("Roboto", 12))
        info_label.pack(side="left", padx=10)

class SuccessRateWidget(ctk.CTkFrame):
    """Success rate tracking widget"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title
        title = ctk.CTkLabel(self, text="📊 Success Rates", font=("Roboto", 16, "bold"))
        title.pack(pady=10)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        # Load and display success rates
        self.load_success_rates(stats_frame)
    
    def load_success_rates(self, parent):
        """Load and display success rates"""
        # Sample data - in real app, load from database
        success_rates = {
            "Deauth Attack": {"success": 8, "total": 10},
            "Evil Twin": {"success": 3, "total": 7},
            "Handshake Capture": {"success": 6, "total": 8},
            "WPS Attack": {"success": 2, "total": 5}
        }
        
        for attack_type, stats in success_rates.items():
            rate = (stats['success'] / stats['total']) * 100 if stats['total'] > 0 else 0
            
            # Attack type label
            type_label = ctk.CTkLabel(parent, text=attack_type, font=("Roboto", 14))
            type_label.pack(pady=5, anchor="w", padx=20)
            
            # Progress bar
            progress = ctk.CTkProgressBar(parent)
            progress.pack(pady=2, padx=20, fill="x")
            progress.set(rate / 100)
            
            # Rate label
            rate_label = ctk.CTkLabel(
                parent, text=f"{rate:.1f}% ({stats['success']}/{stats['total']})",
                font=("Roboto", 12), text_color="gray"
            )
            rate_label.pack(pady=2, anchor="w", padx=20)

class DashboardPage(ctk.CTkFrame):
    """Main dashboard page"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Navigation bar
        self.nav_bar = NavigationBar(self, controller, "Dashboard")
        
        # Title
        title = ctk.CTkLabel(self, text="📊 Dashboard & Analytics", font=("Roboto", 24, "bold"))
        title.pack(pady=20)
        
        # Main content frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Configure grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Top left: System Monitor
        self.system_monitor = SystemMonitor(main_frame)
        self.system_monitor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Top right: Success Rates
        self.success_rates = SuccessRateWidget(main_frame)
        self.success_rates.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Bottom left: Network Stats Chart
        self.network_chart = NetworkStatsChart(main_frame)
        self.network_chart.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Bottom right: Attack History
        self.attack_history = AttackHistory(main_frame)
        self.attack_history.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    def __del__(self):
        """Cleanup when page is destroyed"""
        if hasattr(self, 'system_monitor'):
            self.system_monitor.stop_monitoring()