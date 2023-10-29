#!/usr/bin/python3
"""API routes for status and other functionalities
"""
from flask import Flask
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stats():
    """
    Return a JSON response with the status "OK".
    """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def objects_count():
    """get the amount of each object by type"""
    objs_stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return (jsonify(objs_stats))
