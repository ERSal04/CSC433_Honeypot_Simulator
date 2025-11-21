import json
import pandas as pd
from datetime import datetime, timedelta
import os
from jinja2 import Environment, FileSystemLoader

class DailyReportGenerator:
    def __init__(self, log_path="data/logs/honey.log"):
        self.log_path = log_path
        self.template_dir = "intelligence/reporting/report_templates"
        
        # Setup Jinja2 for HTML templating
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def generate(self, date_str=None):
        """
        Generates a report for a specific date (YYYY-MM-DD).
        Defaults to 'today' if not provided.
        """
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')

        # 1. Load Data
        df = self._load_logs()
        if df.empty:
            return "No logs found."

        # 2. Filter for specific date
        # Assuming timestamp format is ISO (2023-10-25T...)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_data = df[df['timestamp'].dt.strftime('%Y-%m-%d') == date_str]

        if daily_data.empty:
            return f"No activity recorded for {date_str}."

        # 3. Calculate Stats
        stats = {
            "date": date_str,
            "total_events": len(daily_data),
            "unique_ips": daily_data['src_ip'].nunique(),
            "top_ips": daily_data['src_ip'].value_counts().head(5).to_dict(),
            "top_countries": daily_data['country'].value_counts().head(5).to_dict(),
            "top_usernames": self._safe_count(daily_data, 'username'),
            "top_passwords": self._safe_count(daily_data, 'password'),
            "attack_types": daily_data['event_type'].value_counts().head(5).to_dict()
        }

        # 4. Render HTML
        return self._render_html(stats)

    def _load_logs(self):
        """Reads JSON lines into a Pandas DataFrame."""
        if not os.path.exists(self.log_path):
            return pd.DataFrame()

        data = []
        with open(self.log_path, 'r') as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except:
                    continue
        return pd.DataFrame(data)

    def _safe_count(self, df, column, limit=5):
        """Helper to count columns that might not exist."""
        if column in df.columns:
            return df[column].value_counts().head(limit).to_dict()
        return {}

    def _render_html(self, stats):
        """Fills the HTML template with data."""
        template = self.env.get_template("daily_summary.html")
        return template.render(stats=stats)

# Example Usage:
# report = DailyReportGenerator().generate()
# with open("daily_report.html", "w") as f:
#     f.write(report)