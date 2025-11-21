import eventlet
eventlet.monkey_patch() # Required for optimal WebSocket performance

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import yaml
import os
import logging

# Import our custom modules
from intelligence.log_parser import LogParser
from intelligence.enrichment import GeoIPEnricher
from intelligence.alerting import AlertEngine
from intelligence.analysis import PatternMatcher

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'honeypot_secret_key' # Change this in production
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- Global Services ---
config = {}
log_parser = None
geo_enricher = None
alert_engine = None
pattern_matcher = None

def load_config():
    """Loads the main configuration file."""
    global config
    config_path = "config/honeypot_config.yaml"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        print("[!] Config file not found. Using defaults.")
        config = {
            'intelligence': {
                'log_path': 'data/logs/honey.log',
                'geoip_db': 'data/GeoLite2-City.mmdb'
            }
        }

def process_log_entry(log_data):
    """
    The Core Pipeline:
    1. Log Ingestion -> 2. Enrichment -> 3. Analysis -> 4. Alerting -> 5. Visualization
    """
    try:
        # 1. Enrichment (Where is the IP from?)
        if geo_enricher:
            location = geo_enricher.get_location(log_data.get('src_ip'))
            if location:
                log_data.update(location)

        # 2. Analysis (What kind of attack is it?)
        if pattern_matcher:
            attacks = pattern_matcher.analyze_payload(log_data.get('payload', ''))
            log_data['attack_types'] = attacks
            
            # Calculate dynamic severity
            if 'attack_types' in log_data and log_data['attack_types']:
                log_data['severity'] = 'medium'
            if 'destruction' in str(log_data.get('payload')): # Simple heuristic
                log_data['severity'] = 'high'

        # 3. Alerting (Should we wake up the admin?)
        if alert_engine:
            alert_engine.process_event(log_data)

        # 4. Visualization (Push to Browser via WebSocket)
        socketio.emit('new_log', log_data)
        
    except Exception as e:
        print(f"[Dashboard] Error processing log: {e}")

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main dashboard."""
    return render_template('index.html')

@app.route('/map')
def map_view():
    """Renders the full-screen attack map."""
    return render_template('map.html')

@app.route('/analytics')
def analytics():
    """Renders the statistics page."""
    return render_template('analytics.html')

@app.route('/api/status')
def status():
    """Simple API endpoint to check health."""
    return jsonify({"status": "online", "services": ["dashboard", "intelligence"]})

# --- Startup Logic ---

def start_services():
    global log_parser, geo_enricher, alert_engine, pattern_matcher
    
    load_config()
    
    # Initialize Intelligence Modules
    geo_db = config.get('intelligence', {}).get('geoip_db', 'data/GeoLite2-City.mmdb')
    geo_enricher = GeoIPEnricher(geo_db)
    
    alert_engine = AlertEngine(config)
    pattern_matcher = PatternMatcher()
    
    # Start Log Watcher
    log_path = config.get('intelligence', {}).get('log_path', 'data/logs/honey.log')
    log_parser = LogParser(log_path, callback=process_log_entry)
    log_parser.start()

if __name__ == '__main__':
    print("[*] Starting Honeypot Dashboard...")
    start_services()
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)