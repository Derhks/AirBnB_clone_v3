#!/usr/bin/python3
"""
This module create a new view for Amenity objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def show_amenities():
    """
    This method show a list with all the amenities
    """
    all_amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(all_amenities[amenity].to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def show_amenity(amenity_id=None):
    """
    This method show a amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity_id is not None and amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """
    This method delete a amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity_id is not None and amenity is not None:
        storage.delete(amenity)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/amenities',
                 strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    This method create an amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_amenity = Amenity(**request.get_json())
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def modify_amenity(amenity_id=None):
    """
    This method modify an amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity_id is not None and amenity is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            amenity.name = request.get_json()['name']
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
