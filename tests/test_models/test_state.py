#!/usr/bin/python3
""" """
import unittest
from models.state import State
from models.city import City
from models.base_model import BaseModel
from os import getenv
from datetime import datetime
from sqlalchemy.orm import relationship


class TestState(unittest.TestCase):
    """Test cases for the State class"""

    def setUp(self):
        """Set up testing environment"""
        self.state = State()
        self.city = City()

    def tearDown(self):
        """Tear down testing environment"""
        del self.state
        del self.city

    def test_inheritance(self):
        """Test inheritance"""
        self.assertIsInstance(self.state, BaseModel)
        self.assertIsInstance(self.city, BaseModel)

    def test_attributes(self):
        """Test attributes"""
        self.assertTrue(hasattr(self.state, 'id'))
        self.assertTrue(hasattr(self.state, 'created_at'))
        self.assertTrue(hasattr(self.state, 'updated_at'))
        self.assertTrue(hasattr(self.state, 'name'))
        self.assertTrue(hasattr(self.state, 'cities'))

        self.assertTrue(hasattr(self.city, 'id'))
        self.assertTrue(hasattr(self.city, 'created_at'))
        self.assertTrue(hasattr(self.city, 'updated_at'))
        self.assertTrue(hasattr(self.city, 'name'))
        self.assertTrue(hasattr(self.city, 'state_id'))

    def test_defaults(self):
        """Test default values"""
        self.assertEqual(self.state.name, "")
        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)
        self.assertIsInstance(self.city.created_at, datetime)
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_str_representation(self):
        """Test __str__ representation"""
        self.assertEqual(str(self.state), "[State] ({}) {}".format(
            self.state.id, self.state.__dict__))
        self.assertEqual(str(self.city), "[City] ({}) {}".format(
            self.city.id, self.city.__dict__))

    def test_to_dict_method(self):
        """Test to_dict method"""
        state_dict = self.state.to_dict()
        self.assertEqual(type(state_dict), dict)
        self.assertTrue('id' in state_dict)
        self.assertTrue('created_at' in state_dict)
        self.assertTrue('updated_at' in state_dict)
        self.assertTrue('name' in state_dict)
        self.assertTrue('cities' in state_dict)
        self.assertEqual(state_dict['__class__'], 'State')

        city_dict = self.city.to_dict()
        self.assertEqual(type(city_dict), dict)
        self.assertTrue('id' in city_dict)
        self.assertTrue('created_at' in city_dict)
        self.assertTrue('updated_at' in city_dict)
        self.assertTrue('name' in city_dict)
        self.assertTrue('state_id' in city_dict)
        self.assertEqual(city_dict['__class__'], 'City')

    def test_property(self):
        """Test property"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(self.state.cities, [])
            self.assertIsInstance(self.state.cities, list)
        else:
            self.assertEqual(type(self.state.cities), relationship)
            self.assertEqual(self.state.cities[0], self.city)

    def test_close_method(self):
        """Test close method"""
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertTrue(hasattr(self.state, 'close'))
            self.assertIsInstance(self.state.close, method)


if __name__ == '__main__':
    unittest.main()
