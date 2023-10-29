#!/usr/bin/python3
"""Web Application using Flask"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(excep):
    """
    Close the SQLAlchemy Session after each request
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """Handle the /states_list route and
    render a template with a sorted list of State objects
    """
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
