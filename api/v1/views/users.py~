#!/usr/bin/python3
"""File that contains views for User objects in the RESTful API."""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    list_users = []
    for user in storage.all(User).values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object by its ID."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """Deletes a User object by its ID."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object."""
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    if 'email' not in json_data:
        abort(400, description='Missing email')
    if 'password' not in json_data:
        abort(400, description='Missing password')
    new_user = User(**json_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """Updates a User object by its ID."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attribute, val)
    storage.save()
    return jsonify(user.to_dict()), 200
