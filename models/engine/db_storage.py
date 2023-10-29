#!/usr/bin/python3
"""DB Storage module for AirBnB clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DBStorage class for database storage management"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage class"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, password, host, database))

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database"""
        objs = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            for obj in self.__session.query(cls):
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs[key] = obj
        else:
            class_list = [State, City, User, Place, Review, Amenity]
            objs = {}  # Dictionary to store queried objects

            for cls in class_list:
                for obj in self.__session.query(cls):
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj

        return objs

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database
        the current database session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """ calls remove()
        """
        self.__session.close()
