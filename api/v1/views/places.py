#!/usr/bin/python3
"""File that contains views for Place objects in the RESTful API."""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by its ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object by its ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in json_data:
        abort(400, description='Missing user_id')
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in json_data:
        abort(400, description='Missing name')
    new_place = Place(city_id=city_id, user_id=json_data['user_id'],
                      **json_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_by_id(place_id):
    """Updates a Place object by its ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'user_id', 'city_id', 'created_at',
                             'updated_at']:
            setattr(place, attribute, val)
    storage.save()
    return jsonify(place.to_dict()), 200
