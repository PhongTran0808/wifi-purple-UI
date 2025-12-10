import os
import json
import subprocess

class HandshakeController:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.tool_path = self.config["tools"]["handshake"]

    def capture_handshake(self, interface, target_bssid, channel):
        """
        Bắt gói handshake WPA/WPA2
        """

        if not interface or not target_bssid or not channel:
            return "Thiếu interface, BSSID hoặc channel"

        cmd = [
            "python3",
            self.tool_path,
            "-i", interface,
            "-b", target_bssid,
            "-c", str(channel)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"[ERROR] Không thể bắt Handshake: {e}"
