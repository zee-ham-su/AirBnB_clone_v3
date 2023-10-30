#!/usr/bin/python3
"""
File that contains views for Amenity objects in the RESTful API.
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    list_amens = []
    for amenity in storage.all(Amenity).values():
        list_amens.append(amenity.to_dict())
    return jsonify(list_amens)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes an Amenity object by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object."""
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    if 'name' not in json_data:
        abort(400, description='Missing name')
    new_amenity = Amenity(**json_data)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """Updates an Amenity object by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attribute, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
