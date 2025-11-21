from flask import jsonify, request
import sqlite3
import os
from . import api_bp

DB_PATH = "data/database/honeytrap.db"

def get_db_connection():
    """Helper to connect to SQLite database."""
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

@api_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "online", "module": "dashboard_api"})

@api_bp.route('/stats/summary', methods=['GET'])
def get_summary_stats():
    """Returns counts for the KPI cards (Total Events, Unique IPs)."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database not initialized"}), 500

    try:
        total_events = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        unique_ips = conn.execute("SELECT COUNT(DISTINCT src_ip) FROM logs").fetchone()[0]
        
        # Get top country
        top_country = conn.execute("""
            SELECT country, COUNT(*) as c 
            FROM logs 
            WHERE country != 'Unknown' 
            GROUP BY country 
            ORDER BY c DESC LIMIT 1
        """).fetchone()
        
        return jsonify({
            "total_events": total_events,
            "unique_ips": unique_ips,
            "top_country": top_country['country'] if top_country else "N/A"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@api_bp.route('/logs/recent', methods=['GET'])
def get_recent_logs():
    """Returns the last 50 logs for the table."""
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        logs = conn.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50").fetchall()
        # Convert Row objects to dicts
        return jsonify([dict(row) for row in logs])
    finally:
        conn.close()