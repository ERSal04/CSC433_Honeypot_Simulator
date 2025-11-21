import os
import threading
import logging
from playsound import playsound

class SoundAlert:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.logger = logging.getLogger("SoundAlert")
        
        # We use os.path.abspath to ensure Windows/Mac paths are handled correctly
        # Assumes you run the script from the project root
        self.sound_file = os.path.abspath("dashboard/static/sounds/alert.wav")

    def play_alarm(self):
        """
        Plays the alert sound in a non-blocking thread.
        """
        if not self.enabled:
            return
            
        if not os.path.exists(self.sound_file):
            self.logger.warning(f"Sound file not found at: {self.sound_file}")
            return

        # We use a thread so the honeypot doesn't freeze while the sound plays
        t = threading.Thread(target=self._play_thread, daemon=True)
        t.start()

    def _play_thread(self):
        try:
            playsound(self.sound_file)
        except Exception as e:
            self.logger.error(f"Failed to play sound: {e}")