import os
import json
import subprocess

class EvilTwinController:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.tool_path = self.config["tools"]["evil_twin"]

    def run_evil_twin(self, interface, ssid_fake):
        """
        Khởi chạy tấn công Evil Twin – tạo AP giả
        """

        if not interface or not ssid_fake:
            return "Thiếu interface hoặc tên SSID giả"

        cmd = [
            "python3",
            self.tool_path,
            "-i", interface,
            "-s", ssid_fake
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"[ERROR] Không thể chạy Evil Twin: {e}"
