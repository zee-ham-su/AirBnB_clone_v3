#!/usr/bin/python3

from models import storage
from models.state import State

print(len(storage.all(State)))
