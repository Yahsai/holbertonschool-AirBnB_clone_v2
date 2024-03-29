#!/usr/bin/python3
""" """
import unittest
from models.place import Place
from models.review import Review
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float
from os import getenv


class TestPlace(unittest.TestCase):
    """Test cases for the Place class"""

    def setUp(self):
        """Set up testing environment"""
        self.place = Place()

    def tearDown(self):
        """Tear down testing environment"""
        del self.place

    def test_inheritance(self):
        """Test inheritance"""
        self.assertIsInstance(self.place, BaseModel)

    def test_attributes(self):
        """Test attributes"""
        self.assertTrue(hasattr(self.place, 'id'))
        self.assertTrue(hasattr(self.place, 'created_at'))
        self.assertTrue(hasattr(self.place, 'updated_at'))
        self.assertTrue(hasattr(self.place, 'city_id'))
        self.assertTrue(hasattr(self.place, 'user_id'))
        self.assertTrue(hasattr(self.place, 'name'))
        self.assertTrue(hasattr(self.place, 'description'))
        self.assertTrue(hasattr(self.place, 'number_rooms'))
        self.assertTrue(hasattr(self.place, 'number_bathrooms'))
        self.assertTrue(hasattr(self.place, 'max_guest'))
        self.assertTrue(hasattr(self.place, 'price_by_night'))
        self.assertTrue(hasattr(self.place, 'latitude'))
        self.assertTrue(hasattr(self.place, 'longitude'))
        self.assertTrue(hasattr(self.place, 'amenity_ids'))

    def test_defaults(self):
        """Test default values"""
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertIsNone(self.place.description)
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)
        self.assertIsNone(self.place.latitude)
        self.assertIsNone(self.place.longitude)
        self.assertEqual(self.place.amenity_ids, [])

    def test_relationships(self):
        """Test relationships"""
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertEqual(type(Place.reviews), relationship)
            self.assertEqual(type(Place.amenities), relationship)
            self.assertEqual(Place.reviews.argument, Review)
            self.assertEqual(Place.amenities.argument.__name__, "Amenity")
        else:
            self.assertTrue(hasattr(Place, 'reviews'))
            self.assertTrue(hasattr(Place, 'amenities'))

    def test_review_property(self):
        """Test review property"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(self.place.reviews, [])
            self.assertIsInstance(self.place.reviews, list)

    def test_amenities_property(self):
        """Test amenities property"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertEqual(self.place.amenities, [])
            self.assertIsInstance(self.place.amenities, list)

    def test_amenities_setter(self):
        """Test amenities setter"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            amenity = "Amenity"
            self.place.amenities = amenity
            self.assertEqual(self.place.amenities, [amenity])

if __name__ == '__main__':
    unittest.main()