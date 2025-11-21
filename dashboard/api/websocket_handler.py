from flask_socketio import emit
from flask import request
import logging

logger = logging.getLogger("WebSocket")

def register_socket_events(socketio):
    """
    Attaches event listeners to the SocketIO instance.
    Call this from web_dashboard.py.
    """

    @socketio.on('connect')
    def handle_connect():
        client_ip = request.remote_addr
        logger.info(f"Dashboard Client Connected: {client_ip}")
        emit('server_status', {'msg': 'Connected to Watchtower Core'})

    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info("Dashboard Client Disconnected")

    @socketio.on('request_snapshot')
    def handle_snapshot_request():
        """
        The frontend can ask for a 'snapshot' of current state 
        immediately upon loading, instead of waiting for a new attack.
        """
        # In a real app, you might fetch the last 10 logs from RAM cache here
        emit('notification', {'title': 'System', 'message': 'Real-time feed active'})

    @socketio.on('ping')
    def handle_ping():
        emit('pong', {'status': 'alive'})