#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    This method return the status
    """
    return jsonify({"status": "OK"})
