#!/usr/bin/python3
"""Flask app"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def exit_db(execp):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def err_not_found(error):
    """JSON format to handle 404 errors"""
    return (jsonify({"error": "Not found"})), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
