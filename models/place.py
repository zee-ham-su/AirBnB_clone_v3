#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from os import getenv
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey


place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    # Define the relationship between Place and Review
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")

    else:
        @property
        def reviews(self):
            """
            Getter attribute for reviews that returns
            a list of Review instances
            with place_id equal to the current Place.id
            """
            from models import storage
            review_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ Getter attribute for amenities that
            returns a list of Amenity instances
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute for amenities that
            handles append method for adding an Amenity.id
            """
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
