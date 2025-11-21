import time
import json
import os
import logging
from threading import Thread

class LogParser:
    """
    Watches a specific log file for new entries (similar to 'tail -f').
    Parses JSON lines and sends them to a callback function.
    """
    
    def __init__(self, log_path, callback=None):
        """
        Initialize the parser.
        
        :param log_path: Path to the honey.log file (e.g., 'data/logs/honey.log')
        :param callback: Function to call with the parsed dict when a new log arrives.
        """
        self.log_path = log_path
        self.callback = callback
        self.running = False
        self.logger = logging.getLogger("LogParser")

    def start(self):
        """Starts the watcher in a background thread."""
        self.running = True
        # Daemon=True means this thread will die automatically when the main program exits
        t = Thread(target=self._tail_log, daemon=True)
        t.start()
        self.logger.info(f"LogParser started watching: {self.log_path}")

    def stop(self):
        """Stops the watcher thread safely."""
        self.running = False

    def _tail_log(self):
        """
        The main loop that reads the file.
        """
        # 1. Wait for the file to exist (in case Role A hasn't started yet)
        while not os.path.exists(self.log_path):
            if not self.running: return
            time.sleep(1)

        # 2. Open the file
        file = open(self.log_path, "r")
        
        # 3. Seek to the end. We only want NEW logs, not old history.
        file.seek(0, os.SEEK_END)
        
        # Get the file inode (ID) to detect if the file is deleted/rotated
        inode = os.fstat(file.fileno()).st_ino

        while self.running:
            # Check if file was rotated (deleted and recreated by log rotation)
            if self._file_was_rotated(inode):
                file.close()
                # Re-open the new file
                if os.path.exists(self.log_path):
                    file = open(self.log_path, "r")
                    inode = os.fstat(file.fileno()).st_ino
                else:
                    time.sleep(1)
                    continue

            # Read new lines
            line = file.readline()
            
            # If no new line, wait a tiny bit and try again
            if not line:
                time.sleep(0.1)
                continue

            self._process_line(line)

        file.close()

    def _file_was_rotated(self, current_inode):
        """Checks if the file underlying the handle has changed."""
        try:
            if not os.path.exists(self.log_path):
                return False 
            
            # Compare the current file on disk with the one we have open
            new_inode = os.stat(self.log_path).st_ino
            return new_inode != current_inode
        except OSError:
            return False

    def _process_line(self, line):
        """Parses the JSON line and triggers the callback."""
        line = line.strip()
        if not line:
            return

        try:
            data = json.loads(line)
            
            # If a callback function is set, send the data there
            if self.callback:
                self.callback(data)
                
        except json.JSONDecodeError:
            # This happens if the log line is half-written or corrupt
            self.logger.warning(f"Skipping invalid JSON line")
        except Exception as e:
            self.logger.error(f"Error processing log line: {e}")