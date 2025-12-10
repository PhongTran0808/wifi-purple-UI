import customtkinter as ctk

class DeauthPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Deauthentication Attack", font=("Roboto", 22, "bold"))
        title.pack(pady=20)

        self.bssid_entry = ctk.CTkEntry(self, placeholder_text="BSSID")
        self.bssid_entry.pack(pady=10)

        self.channel_entry = ctk.CTkEntry(self, placeholder_text="Channel")
        self.channel_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start Deauth", width=200, command=self.start_attack)
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=800, height=400)
        self.log_box.pack(pady=20)

    def start_attack(self):
        bssid = self.bssid_entry.get()
        channel = self.channel_entry.get()

        self.log_box.insert("end", f"Starting deauth attack on {bssid} @ channel {channel}\n")
        self.log_box.insert("end", "→ controller: deauth_controller.start_deauth()\n\n")
