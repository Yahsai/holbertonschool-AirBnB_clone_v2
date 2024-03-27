#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
Base = declarative_base()


class State(BaseModel, Base):
    """ State class """
    __tablename__  = "states"
    name = Column(String(128), nullable=False)

    # Relación para DBStorage
    cities = relationship("City", cascade="all, delete-orphan", backref="state")

    # Getter para FileStorage
    @property
    def cities(self):
        from models import storage
        from models.city import City
        return storage.all(City).filter(City.state_id == self.id)
