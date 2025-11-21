import logging
from datetime import datetime

# Import the specific notifiers (we assume these files are in the same folder)
from .discord_notifier import DiscordNotifier
from .slack_notifier import SlackNotifier
from .email_notifier import EmailNotifier
from .desktop_notifier import DesktopNotifier
from .sound_alert import SoundAlert

class AlertEngine:
    """
    The AlertEngine acts as the central brain for notifications.
    It receives security events, checks their severity, and dispatches
    them to all enabled channels (Discord, Desktop, Sound, etc.).
    """

    def __init__(self, config):
        """
        Initialize the engine with the configuration dictionary.
        
        :param config: A dictionary loaded from honeypot_config.yaml.
                       It should contain keys like 'discord_webhook', 'smtp_settings', etc.
        """
        self.logger = logging.getLogger("AlertEngine")
        self.config = config

        # --- Initialize Remote Notifiers ---
        # These use API URLs or settings found in the config
        self.discord = DiscordNotifier(config.get('discord_webhook'))
        self.slack = SlackNotifier(config.get('slack_webhook'))
        self.email = EmailNotifier(config.get('smtp_settings'))

        # --- Initialize Local Notifiers (Universal) ---
        # These use boolean flags (True/False) to enable/disable
        self.desktop = DesktopNotifier(enabled=config.get('desktop_notifications', False))
        self.sound = SoundAlert(enabled=config.get('sound_alerts', False))

        self.logger.info("AlertEngine initialized and ready.")

    def process_event(self, event_data):
        """
        The main entry point. Call this method with the enriched log data
        to determine if an alert needs to be sent.
        
        :param event_data: Dictionary containing 'severity', 'src_ip', 'event_type', etc.
        """
        # 1. Extract Severity (Default to 'low' if missing)
        severity = event_data.get('severity', 'low').lower()

        # 2. Filter Logic
        # We typically ignore 'low' severity events to prevent spamming the admin.
        # Only alert on Medium, High, or Critical.
        if severity not in ['medium', 'high', 'critical']:
            return

        # 3. Prepare the Alert Content
        event_type = event_data.get('event_type', 'Security Event')
        src_ip = event_data.get('src_ip', 'Unknown IP')
        
        # Title Example: "[HIGH] SSH Brute Force detected from 192.168.1.5"
        title = f"[{severity.upper()}] {event_type} detected from {src_ip}"
        
        # Message: A detailed description of the event
        message = self._format_message(event_data)

        # 4. Broadcast the Alert
        self._broadcast(title, message, severity)

    def _broadcast(self, title, message, severity):
        """
        Internal method to send the data to all active channels.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg_body = f"Time: {timestamp}\n{message}"

        self.logger.info(f"Triggering alert: {title}")

        # --- Local Alerts (Visual & Audio) ---
        # Always show desktop notification if enabled in config
        self.desktop.notify(title, full_msg_body)
        
        # Only play loud alarm sounds for HIGH or CRITICAL severity
        if severity in ['high', 'critical']:
            self.sound.play_alarm()

        # --- Remote Alerts ---
        # Send to Discord and Slack
        self.discord.send(title, full_msg_body, severity)
        self.slack.send(title, full_msg_body)

        # --- Email Alert ---
        # Only send emails for CRITICAL events to avoid clogging the inbox
        if severity in ['high', 'critical']:
            self.email.send(title, full_msg_body)

    def _format_message(self, data):
        """
        Helper to create a clean, readable string from the event data.
        """
        return (
            f"Source IP: {data.get('src_ip')}\n"
            f"Location: {data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}\n"
            f"Protocol: {data.get('protocol', 'N/A')}\n"
            f"Payload: {data.get('payload', 'N/A')}\n"
            f"Tags: {', '.join(data.get('tags', []))}"
        )