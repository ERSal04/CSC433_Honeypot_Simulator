import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import yaml
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligence.log_parser import LogParser
from intelligence.enrichment import GeoIPEnricher
from intelligence.analysis import PatternMatcher
from dashboard.api import api_bp

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'honeypot_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Register API Blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Global services
config = {}
log_parser = None
geo_enricher = None
pattern_matcher = None

def load_config():
    global config
    config_path = "../config/honeypot_config.yaml"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'intelligence': {
                'log_path': '../data/logs/honey.log',
                'geoip_db': '../data/GeoLite2-City.mmdb'
            }
        }

def process_log_entry(log_data):
    """Pipeline: Enrich -> Analyze -> Broadcast"""
    try:
        # Enrichment
        if geo_enricher:
            location = geo_enricher.get_location(log_data.get('ip'))
            if location:
                log_data.update({
                    'country': location.get('country', 'Unknown'),
                    'city': location.get('city', 'Unknown'),
                    'lat': location.get('latitude', 0),
                    'lon': location.get('longitude', 0)
                })
                log_data['src_ip'] = log_data.get('ip')  # Normalize field name
        
        # Analysis
        if pattern_matcher:
            payload = log_data.get('data', {}).get('command', '')
            if payload:
                log_data['payload'] = payload
        
        # Broadcast to frontend
        socketio.emit('new_log', log_data)
        
    except Exception as e:
        print(f"[Dashboard] Error processing log: {e}")

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

def start_services():
    global log_parser, geo_enricher, pattern_matcher
    
    load_config()
    
    # Initialize services
    geo_db = config.get('intelligence', {}).get('geoip_db', '../data/GeoLite2-City.mmdb')
    if os.path.exists(geo_db):
        geo_enricher = GeoIPEnricher(geo_db)
    
    pattern_matcher = PatternMatcher()
    
    # Start log watcher
    log_path = config.get('intelligence', {}).get('log_path', '../data/logs/honey.log')
    log_parser = LogParser(log_path, callback=process_log_entry)
    log_parser.start()
    
    print("[+] Intelligence services started")

if __name__ == '__main__':
    print("[*] Starting Honeypot Dashboard...")
    start_services()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False)