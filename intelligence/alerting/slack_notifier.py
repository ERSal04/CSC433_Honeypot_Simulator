import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, title, message):
        if not self.webhook_url:
            return

        payload = {
            "text": f"*{title}*\n{message}"
        }

        try:
            requests.post(self.webhook_url, json=payload)
        except Exception as e:
            print(f"[!] Slack Send Error: {e}")