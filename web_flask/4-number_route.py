#!/usr/bin/python3
"""
a script that starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ display's Hello HBNB!
    """
    return ('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ displays HBNB"""
    return ('HBNB')


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """display “C ” followed by the
       value of the text variable
    """
    return ('C {}'.format(text.replace('_', ' ')))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def python_text(text="is_cool"):
    """Displays 'Python ' followed by the
       value of the text variable
    """
    return('Python {}'.format(text.replace('_', ' ')))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays 'n is a number' only if n
       is an integer."""
    return ('{} is a number'.format(n))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
