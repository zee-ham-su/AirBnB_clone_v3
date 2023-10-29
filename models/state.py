#!/usr/bin/python3
""" State Module for HBNB project """
import shlex
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'  # Name of the database table
    name = Column(String(128), nullable=False)

    # Define the relationship between State and City
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        data = models.storage.all()
        city_data = []
        filtered_cities = []

        for data_key in data:
            city_name = data_key.replace('.', ' ')
            city_name_parts = shlex.split(city_name)

            if city_name_parts[0] == 'City':
                city_data.append(data[data_key])

        for city in city_data:
            if city.state_id == self.id:
                filtered_cities.append(city)

        return filtered_cities
