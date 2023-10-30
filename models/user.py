#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review
from hashlib import md5


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    places = relationship("Place", backref="user",
                          cascade="all, delete-orphan")
    reviews = relationship("Review",
                           cascade='all, delete, delete-orphan',
                           backref="user")

    def __init__(self, *args, **kwargs):
        """
        Initializing a new instance of the User.
        Args:
        """
        if 'password' in kwargs:
            kwargs['password'] = md5(kwargs['password'].encode()).hexdigest()

        super().__init__(*args, **kwargs)
