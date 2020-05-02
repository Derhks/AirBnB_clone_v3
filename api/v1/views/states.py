#!/usr/bin/python3
"""
This module create a new view for State objects
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def show_states():
    """
    This method show a list with all the states
    """
    all_states = storage.all(State)
    list_states = []
    for state in all_states:
        list_states.append(all_states[state].to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def show_state(state_id=None):
    """
    This method show a state
    """
    state = storage.get(State, state_id)
    if state_id is not None and state is not None:
        return jsonify(state.to_dict())
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id=None):
    """
    This method delete a state
    """
    state = storage.get(State, state_id)
    if state_id is not None and state is not None:
        storage.delete(state)
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
    This method create a state
    """
    # If the HTTP body request is not valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    # If the dictionary doesn’t contain the key name
    elif 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        #  def __init__(self, *args, **kwargs): --> base_model.py
        new_state = State(**request.get_json())
        # def save(self): --> base_model.py
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def modify_state(state_id=None):
    """
    This method modify a state
    """
    state = storage.get(State, state_id)
    if state_id is not None and state is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            state.name = request.get_json()['name']
            storage.save()
            return make_response(jsonify(state.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
