from flask import Blueprint

# Create a Blueprint named 'api_bp'
# All routes in this blueprint will start with '/api' (e.g., /api/stats)
api_bp = Blueprint('api', __name__)

from . import routes