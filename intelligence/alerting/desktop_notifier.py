from plyer import notification
import logging

class DesktopNotifier:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.logger = logging.getLogger("DesktopNotifier")

    def notify(self, title, message):
        """
        Sends a cross-platform desktop notification.
        """
        if not self.enabled:
            return

        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Honeypot Watchtower',
                app_icon=None,  # You can add an .ico (Windows) or .png (Linux) path here
                timeout=10      # How long the notification stays visible
            )
        except Exception as e:
            self.logger.error(f"Failed to send desktop notification: {e}")