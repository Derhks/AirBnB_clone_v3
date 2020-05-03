#!/usr/bin/python3
"""
This module create a new view for State objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def show_reviews(place_id=None):
    """
    This method show a list with all the reviews
    """
    place = storage.get(Place, place_id)
    if place is not None:
        all_reviews = place.reviews
        list_reviews = []
        for review in all_reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def show_review(review_id=None):
    """
    This method show a review
    """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id=None):
    """
    This method delete a review
    """
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id=None):
    """
    This method create a review
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    else:
        place = storage.get(Place, place_id)
        user_id = request.get_json()['user_id']
        user = storage.get(User, user_id)
        if place is not None and user is not None:
            custom_request = request.get_json()
            custom_request['place_id'] = place_id
            custom_request['user_id'] = user_id
            new_review = Review(**custom_request)
            new_review.save()
            return make_response(jsonify(new_review.to_dict()), 201)
        else:
            return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def modify_review(review_id=None):
    """
    This method modify a review
    """
    review = storage.get(Review, review_id)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif review is not None:
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'place_id',
                            'created_at', 'updated_at']:
                setattr(review, attr, val)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
