#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import models
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ This is the city class, contains state ID and name """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey('states.id'),
                      nullable=False)
    name = Column(String(128), nullable=False)

    places = relationship("Place",
                          backref="city",
                          cascade="all, delete-orphan")