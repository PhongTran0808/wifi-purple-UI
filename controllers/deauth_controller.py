import os
import json
import subprocess

class DeauthController:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.tool_path = self.config["tools"]["deauth"]

    def run_deauth(self, interface, target_bssid, count=50):
        """
        Thực thi tấn công deauthentication
        """

        if not interface or not target_bssid:
            return "Thiếu tham số interface hoặc BSSID"

        cmd = [
            "python3",
            self.tool_path,
            "-i", interface,
            "-t", target_bssid,
            "-c", str(count)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr

        except Exception as e:
            return f"[ERROR] Không thể chạy deauth: {e}"
