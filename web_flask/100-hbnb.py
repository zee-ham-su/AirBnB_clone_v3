#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def teardown(excep):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Display the HTML page for hbnb."""
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    states = storage.all("State")
    return render_template("100-hbnb.html",
                           amenities=amenities,
                           places=places,
                           states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
