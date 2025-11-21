class CredentialAnalyzer:
    """
    Analyzes captured credentials to determine sophistication.
    """
    def __init__(self):
        self.common_users = {"root", "admin", "support", "user", "oracle", "guest"}
        self.weak_passwords = {"123456", "password", "admin", "root", "12345", "toor"}

    def analyze(self, username, password):
        """
        Returns a dictionary with risk score and tags.
        """
        tags = []
        risk_score = 0

        # Check Username
        if username in self.common_users:
            tags.append("default_username")
            risk_score += 10
        
        # Check Password
        if password in self.weak_passwords:
            tags.append("weak_password")
            risk_score += 20
        
        if username == password:
            tags.append("user_equals_pass")
            risk_score += 15

        if not password:
            tags.append("empty_password")
            risk_score += 30

        return {
            "risk_score": risk_score,
            "tags": tags,
            "is_critical": risk_score >= 40
        }