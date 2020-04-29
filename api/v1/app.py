#!/usr/bin/python3
"""This module connect to API"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, Blueprint

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(code):
    """
    This method close the storage
    """
    storage.close()

if __name__ == "__main__":
    app.run(host=environ.get('HBNB_API_HOST'),
            port=environ.get('HBNB_API_PORT'),
            debug=True)
