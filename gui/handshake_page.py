import customtkinter as ctk

class HandshakePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Handshake Capture", font=("Roboto", 22, "bold"))
        title.pack(pady=20)

        self.bssid_entry = ctk.CTkEntry(self, placeholder_text="Target BSSID")
        self.bssid_entry.pack(pady=10)

        self.channel_entry = ctk.CTkEntry(self, placeholder_text="Channel")
        self.channel_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start Capture", command=self.start_capture)
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=800, height=400)
        self.log_box.pack(pady=20)

    def start_capture(self):
        bssid = self.bssid_entry.get()
        channel = self.channel_entry.get()

        self.log_box.insert("end", f"Capturing handshake from {bssid} @ channel {channel}\n")
        self.log_box.insert("end", "→ handshake_controller.capture_handshake()\n\n")
