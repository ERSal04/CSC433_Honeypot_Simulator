import requests
import json

class DiscordNotifier:
    """
    Sends alerts to a Discord channel using a Webhook URL.
    It uses 'Embeds' to format the message with colors based on severity.
    """

    def __init__(self, webhook_url):
        """
        :param webhook_url: The URL provided by Discord (Server Settings > Integrations > Webhooks)
        """
        self.webhook_url = webhook_url

    def send(self, title, message, severity='low'):
        """
        Sends the formatted alert to Discord.
        
        :param title: The headline of the alert (e.g., "[HIGH] SSH Attack")
        :param message: The detailed body text
        :param severity: Used to pick the color of the sidebar (Red, Orange, Blue)
        """
        if not self.webhook_url:
            return

        # Color mapping (Decimal values for Discord)
        # Red = 15158332, Orange = 15105570, Blue = 3447003
        colors = {
            'high': 15158332,     # Red (Critical/High)
            'critical': 15158332, # Red
            'medium': 15105570,   # Orange
            'low': 3447003        # Blue
        }

        # Construct the JSON payload
        payload = {
            "username": "Honeypot Watchtower",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/2493/2493069.png", # Generic Shield Icon
            "embeds": [{
                "title": title,
                "description": message,
                "color": colors.get(severity.lower(), 3447003), # Default to Blue if unknown
                "footer": {
                    "text": "Security Event Log"
                }
            }]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status() # Raise error if 4xx/5xx code
        except Exception as e:
            print(f"[!] Discord Webhook Failed: {e}")