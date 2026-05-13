from flask import jsonify
from . import main_bp

@main_bp.route('/')
def index():
    # api information
    return jsonify({
        'message': 'ReRead API',
        'version': '0.1.0',
        'endpoints': {
            'auth': [
                'POST /api/register',
                'POST /api/login',
                'GET /api/me'
            ],

        }
    })



