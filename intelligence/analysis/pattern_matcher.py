import re
import logging

class PatternMatcher:
    """
    Scans text payloads for known attack signatures using Regex.
    """
    def __init__(self):
        self.logger = logging.getLogger("PatternMatcher")
        
        # Dictionary of regex patterns for common attacks
        self.patterns = {
            "sql_injection": [
                r"UNION SELECT", r"OR 1=1", r"DROP TABLE", 
                r"information_schema", r"waitfor delay"
            ],
            "path_traversal": [
                r"\.\./\.\./", r"/etc/passwd", r"/etc/shadow", 
                r"c:\\windows\\system32", r"boot.ini"
            ],
            "command_injection": [
                r";\s*ls", r"\|\s*cat", r"`whoami`", r"\$\(wget"
            ],
            "downloader": [
                r"wget\s+http", r"curl\s+http", r"tftp\s+-g", 
                r"powershell.*DownloadFile"
            ],
            "reverse_shell": [
                r"nc\s+-e", r"bash\s+-i", r"socket\.socket", 
                r"fsockopen"
            ]
        }

        # Pre-compile regexes for speed
        self.compiled_patterns = {
            key: [re.compile(p, re.IGNORECASE) for p in values]
            for key, values in self.patterns.items()
        }

    def analyze_payload(self, payload):
        """
        Checks a string payload against all patterns.
        Returns a list of detected attack types.
        """
        if not payload:
            return []

        detected_attacks = []
        
        for attack_type, regex_list in self.compiled_patterns.items():
            for regex in regex_list:
                if regex.search(payload):
                    detected_attacks.append(attack_type)
                    break # Found a match for this category, move to next
        
        return detected_attacks