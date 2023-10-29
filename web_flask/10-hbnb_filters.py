#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def close_storage(excep):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filters_hbnb():
    """display hbnb filter html page"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return (render_template("10-hbnb_filters.html",
                            states=states, amenities=amenities))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
