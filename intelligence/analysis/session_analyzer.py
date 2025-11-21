class SessionAnalyzer:
    """
    Analyzes a full session (list of commands) to determine attacker intent.
    """
    
    def analyze_session(self, command_list):
        """
        Input: list of strings (commands)
        Output: Classification (Recon, Exfiltration, Destruction)
        """
        if not command_list:
            return {"intent": "empty", "score": 0}

        unique_cmds = set(command_list)
        cmd_count = len(command_list)
        
        # 1. Heuristic: Is it a bot or human?
        # Bots typically run very few commands very quickly, or repeat commands.
        is_human_behavior = cmd_count > 5 and (len(unique_cmds) / cmd_count > 0.8)

        # 2. Determine Intent
        intent_scores = {
            "reconnaissance": 0,
            "persistence": 0,
            "destruction": 0
        }

        for cmd in command_list:
            if any(x in cmd for x in ["ls", "pwd", "whoami", "uname", "ps"]):
                intent_scores["reconnaissance"] += 1
            if any(x in cmd for x in ["cron", "rc.d", "init.d", "nohup"]):
                intent_scores["persistence"] += 1
            if any(x in cmd for x in ["rm ", "mv ", "shred", "dd "]):
                intent_scores["destruction"] += 1

        # Find the primary intent
        primary_intent = max(intent_scores, key=intent_scores.get)
        
        return {
            "actor_type": "Human" if is_human_behavior else "Bot",
            "primary_intent": primary_intent,
            "command_count": cmd_count,
            "risk_level": "High" if intent_scores["destruction"] > 0 else "Medium"
        }