#!/usr/bin/python3
""" """
import unittest
from models.city import City
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class TestCity(unittest.TestCase):
    """Test cases for the City class"""

    def setUp(self):
        """Set up testing environment"""
        self.city = City()

    def tearDown(self):
        """Tear down testing environment"""
        del self.city

    def test_inheritance(self):
        """Test inheritance"""
        self.assertIsInstance(self.city, BaseModel)

    def test_attributes(self):
        """Test attributes"""
        self.assertTrue(hasattr(self.city, 'id'))
        self.assertTrue(hasattr(self.city, 'created_at'))
        self.assertTrue(hasattr(self.city, 'updated_at'))
        self.assertTrue(hasattr(self.city, 'name'))
        self.assertTrue(hasattr(self.city, 'state_id'))

    def test_defaults(self):
        """Test default values"""
        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

    def test_to_dict_method(self):
        """Test to_dict method"""
        city_dict = self.city.to_dict()
        self.assertEqual(type(city_dict), dict)
        self.assertTrue('id' in city_dict)
        self.assertTrue('created_at' in city_dict)
        self.assertTrue('updated_at' in city_dict)
        self.assertTrue('name' in city_dict)
        self.assertTrue('state_id' in city_dict)
        self.assertEqual(city_dict['__class__'], 'City')

    def test_relationship(self):
        """Test relationship"""
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertEqual(type(City.places), relationship)
            self.assertEqual(City.places.argument, "Place")

    def test_init_method(self):
        """Test __init__ method"""
        city = City(name="New York", state_id="12345")
        self.assertEqual(city.name, "New York")
        self.assertEqual(city.state_id, "12345")


if __name__ == '__main__':
    unittest.main()