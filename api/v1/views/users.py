#!/usr/bin/python3
"""
This module create a new view for State objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users',
                 strict_slashes=False, methods=['GET'])
def show_users():
    """
    This method show a list with all the users
    """
    # storage.all() ~~> return a dict
    all_users = storage.all(User)
    list_users = []
    for user in all_users:
        list_users.append(all_users[user].to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def show_user(user_id=None):
    """
    This method show a user
    """
    user = storage.get(User, user_id)
    if user_id is not None and user is not None:
        return jsonify(user.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id=None):
    """
    This method delete a user
    """
    user = storage.get(User, user_id)
    if user_id is not None and user is not None:
        storage.delete(user)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users',
                 strict_slashes=False, methods=['POST'])
def create_user():
    """
    This method create a user
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    else:
        new_user = User(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def modify_user(user_id=None):
    """
    This method modify a user
    """
    user = storage.get(User, user_id)
    if user_id is not None and user is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            user.password = request.get_json()['password']
            user.first_name = request.get_json()['first_name']
            user.last_name = request.get_json()['last_name']
            storage.save()
            return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
