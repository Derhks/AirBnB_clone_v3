#!/usr/bin/python3
"""
This module create a new view for City objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def show_cities(state_id=None):
    """
    This method show a list with all the cities
    """
    state = storage.get(State, state_id)
    if state_id is not None and state is not None:
        all_cities = state.cities
        list_cities = []
        for city in all_cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_city(city_id=None):
    """
    This method show a city
    """
    city = storage.get(City, city_id)
    if city_id is not None and city is not None:
        return jsonify(city.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    """
    This method delete a city
    """
    city = storage.get(City, city_id)
    if city_id is not None and city is not None:
        storage.delete(city)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id=None):
    """
    This method create a city
    """
    state = storage.get(State, state_id)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        if state_id is not None and state is not None:
            request_with_state = request.get_json()
            request_with_state['state_id'] = state_id
            new_city = City(**request_with_state)
            new_city.save()
            return make_response(jsonify(new_city.to_dict()), 201)
        else:
            return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def modify_city(city_id=None):
    """
    This method modify a city
    """
    city = storage.get(City, city_id)
    if city_id is not None and city is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            city.name = request.get_json()['name']
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
