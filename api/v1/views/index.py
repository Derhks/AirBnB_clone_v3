#!/usr/bin/python3
"""This module connect to API"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """
    This method return the status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def api_v1_stats():
    """
    This method return the amounts of each class
    """
    cnt_Amenity = storage.count(Amenity)
    cnt_City = storage.count(City)
    cnt_Place = storage.count(Place)
    cnt_Review = storage.count(Review)
    cnt_State = storage.count(State)
    cnt_User = storage.count(User)
    return jsonify({"amenities": cnt_Amenity,
                    "cities": cnt_City,
                    "places": cnt_Place,
                    "reviews": cnt_Review,
                    "states": cnt_State,
                    "users": cnt_User})
