#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan", backref="state")

    def __init__(self, *args, **kwargs):
        """ Initializes State """
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """ Getter attribute cities that returns a list of City instances
            with state_id equals to the current State.id """
        from models import storage
        cities_list = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
