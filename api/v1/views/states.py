#!/usr/bin/python3
"""File that contains views for State
objects in the RESTful API.
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_getter():
    """gets the list of all State objects"""
    states = storage.all(State).values()
    sta_list = []
    for state in states:
        sta_list.append(state.to_dict())
    return (jsonify(sta_list))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id_getter(state_id):
    """gets a state object by its Id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ deletes a state object with its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_creation():
    """creates a new state obj"""
    json_data = request.get_json()

    if json_data is None:
        abort(400, description='Not a JSON')
    if 'name' not in json_data:
        abort(400, description='Missing name')
    new_state = State(**json_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """Updates a State object by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'created_at', 'updated_at']:
            setattr(state, attribute, val)
    storage.save()
    return jsonify(state.to_dict()), 200
