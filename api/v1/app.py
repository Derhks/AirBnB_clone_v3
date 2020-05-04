#!/usr/bin/python3
"""This module connect to API"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(code):
    """
    This method close the storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=environ.get('HBNB_API_HOST'),
            port=environ.get('HBNB_API_PORT'),
            debug=True)
