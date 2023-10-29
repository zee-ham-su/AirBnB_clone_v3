#!/usr/bin/python3
"""File that contains views for Review objects in the RESTful API."""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object by its ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a Review object by its ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in json_data:
        abort(400, description='Missing user_id')
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in json_data:
        abort(400, description='Missing text')
    new_review = Review(place_id=place_id, user_id=json_data['user_id'],
                        **json_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """Updates a Review object by its ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, description='Not a JSON')
    for attribute, val in json_data.items():
        if attribute not in ['id', 'user_id', 'place_id', 'created_at',
                             'updated_at']:
            setattr(review, attribute, val)
    storage.save()
    return jsonify(review.to_dict()), 200
