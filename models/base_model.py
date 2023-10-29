#!/usr/bin/python3
"""Base model class for AirBnB"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
import models


Base = declarative_base()


class BaseModel:
    """
    This class defines common attributes and methods for other classes.
    Attributes:
        id (str): Is the unique identifier for the object.
        created_at (datetime): Date and time when the object was created.
        updated_at (datetime): Date and time when the object was last updated.
    """

    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """
        Initializing a new instance of the BaseModel.
        Args:
            args: Not used.
            kwargs (dict): Keyword arguments for object attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    self.__dict__[key] = value
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the object.
        Returns:
            str: A string containing the class name, ID,
            and dictionary representation.
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """
        Returns a string representation of the object.
        Returns:
            str: A string representation.
        """
        return self.__str__()

    def save(self):
        """
        Updating the 'updated_at' attribute and saves
        the object to the data store.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Converting the object to a dictionary.
        Returns:
            dict: A dictionary representation of the object.
        """
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']
        return my_dict

    def delete(self):
        """Deletes the object from the data store."""
        models.storage.delete(self)
