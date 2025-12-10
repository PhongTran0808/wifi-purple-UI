import customtkinter as ctk

class EvilTwinPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Evil Twin Attack", font=("Roboto", 22, "bold"))
        title.pack(pady=20)

        self.ssid_entry = ctk.CTkEntry(self, placeholder_text="Fake SSID")
        self.ssid_entry.pack(pady=10)

        self.channel_entry = ctk.CTkEntry(self, placeholder_text="Channel")
        self.channel_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start Evil Twin", command=self.start_evil_twin)
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=800, height=400)
        self.log_box.pack(pady=20)

    def start_evil_twin(self):
        ssid = self.ssid_entry.get()
        channel = self.channel_entry.get()

        self.log_box.insert("end", f"Creating fake AP: {ssid} on channel {channel}\n")
        self.log_box.insert("end", "→ evil_twin_controller.start_evil_twin()\n\n")
