#!/usr/bin/python3
"""
This module create a new view for City objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def show_places(city_id=None):
    """
    This method show a list with all the places
    """
    city = storage.get(City, city_id)
    if city_id is not None and city is not None:
        all_places = city.places
        list_places = []
        for place in all_places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def show_place(place_id=None):
    """
    This method show a place
    """
    place = storage.get(Place, place_id)
    if place_id is not None and place is not None:
        return jsonify(place.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id=None):
    """
    This method delete a place
    """
    place = storage.get(Place, place_id)
    if place_id is not None and place is not None:
        storage.delete(place)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id=None):
    """
    This method create a place
    """
    city = storage.get(City, city_id)
    user_id = request.get_json()['user_id']
    user = storage.get(User, user_id)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    elif 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif user is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        if city_id is not None and city is not None:
            custom_request = request.get_json()
            custom_request['city_id'] = city_id
            custom_request['user_id'] = user_id
            new_place = Place(**custom_request)
            new_place.save()
            return make_response(jsonify(new_place.to_dict()), 201)
        else:
            return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def modify_place(place_id=None):
    """
    This method modify a place
    """
    place = storage.get(Place, place_id)
    if place_id is not None and place is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            for attr, val in request.get_json().items():
                if attr not in ['id', 'user_id', 'city_id',
                                'created_at', 'updated_at']:
                    setattr(place, attr, val)
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
