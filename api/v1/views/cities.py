#!/usr/bin/python3
"""
File that contains views for City objects in the RESTful API.
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Get the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by its ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by its ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    if 'name' not in json_data:
        abort(400, description='Missing name')
    new_city = City(**json_data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object by its ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'state_id', 'created_at',
                             'updated_at']:
            setattr(city, attribute, val)
    storage.save()
    return jsonify(city.to_dict()), 200
