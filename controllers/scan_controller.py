import os
import json
import subprocess

class ScanController:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.tool_path = self.config["tools"]["scan"]

    def scan_networks(self, interface):
        """
        Quét mạng Wi-Fi xung quanh
        """

        if not interface:
            return "Thiếu interface mạng"

        cmd = [
            "python3",
            self.tool_path,
            "-i", interface,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"[ERROR] Không thể quét mạng: {e}"
