import os
import platform
import threading
import logging

class SoundAlert:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.logger = logging.getLogger("SoundAlert")
        # Get absolute path to the sound file
        self.sound_file = os.path.abspath("dashboard/static/sounds/alert.wav")

    def play_alarm(self):
        """
        Plays the alert sound in a non-blocking thread.
        """
        if not self.enabled:
            return
            
        if not os.path.exists(self.sound_file):
            # Only warn once to avoid log spam
            return

        # Run in a thread so it doesn't freeze the dashboard
        t = threading.Thread(target=self._play_thread, daemon=True)
        t.start()

    def _play_thread(self):
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                # 'afplay' is built into every Mac
                os.system(f"afplay '{self.sound_file}'")
            
            elif system == "Windows":
                # 'winsound' is built into Python on Windows
                import winsound
                winsound.PlaySound(self.sound_file, winsound.SND_FILENAME)
                
            elif system == "Linux":
                # Try common linux players
                os.system(f"aplay '{self.sound_file}' || paplay '{self.sound_file}'")
                
        except Exception as e:
                        self.logger.error(f"Failed to play sound: {e}")