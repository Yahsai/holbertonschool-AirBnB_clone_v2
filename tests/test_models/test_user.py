#!/usr/bin/python3
""" Unittest for user module"""
import unittest
from models.user import User
from models.base_model import BaseModel
from models.place import Place
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from datetime import datetime


class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    def setUp(self):
        """Set up testing environment"""
        self.user = User()
        self.place = Place()
        self.review = Review()

    def tearDown(self):
        """Tear down testing environment"""
        del self.user
        del self.place
        del self.review

    def test_inheritance(self):
        """Test inheritance"""
        self.assertIsInstance(self.user, BaseModel)
        self.assertIsInstance(self.place, BaseModel)
        self.assertIsInstance(self.review, BaseModel)

    def test_attributes(self):
        """Test attributes"""
        self.assertTrue(hasattr(self.user, 'id'))
        self.assertTrue(hasattr(self.user, 'created_at'))
        self.assertTrue(hasattr(self.user, 'updated_at'))
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))
        self.assertTrue(hasattr(self.user, 'places'))
        self.assertTrue(hasattr(self.user, 'reviews'))

        self.assertTrue(hasattr(self.place, 'id'))
        self.assertTrue(hasattr(self.place, 'created_at'))
        self.assertTrue(hasattr(self.place, 'updated_at'))
        self.assertTrue(hasattr(self.place, 'user_id'))

        self.assertTrue(hasattr(self.review, 'id'))
        self.assertTrue(hasattr(self.review, 'created_at'))
        self.assertTrue(hasattr(self.review, 'updated_at'))
        self.assertTrue(hasattr(self.review, 'user_id'))

    def test_defaults(self):
        """Test default values"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertIsNone(self.user.first_name)
        self.assertIsNone(self.user.last_name)

        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.review.user_id, "")

        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)
        self.assertIsInstance(self.place.created_at, datetime)
        self.assertIsInstance(self.place.updated_at, datetime)
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_to_dict_method(self):
        """Test to_dict method"""
        user_dict = self.user.to_dict()
        self.assertEqual(type(user_dict), dict)
        self.assertTrue('id' in user_dict)
        self.assertTrue('created_at' in user_dict)
        self.assertTrue('updated_at' in user_dict)
        self.assertTrue('email' in user_dict)
        self.assertTrue('password' in user_dict)
        self.assertTrue('first_name' in user_dict)
        self.assertTrue('last_name' in user_dict)
        self.assertTrue('places' in user_dict)
        self.assertTrue('reviews' in user_dict)
        self.assertEqual(user_dict['__class__'], 'User')

    def test_relationships(self):
        """Test relationships"""
        self.assertEqual(type(User.places), relationship)
        self.assertEqual(User.places.argument, Place)
        self.assertEqual(User.reviews.argument, Review)

    def test_init_method(self):
        """Test __init__ method"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertIsNone(self.user.first_name)
        self.assertIsNone(self.user.last_name)

        user = User(email="test@example.com", password="password",
                    first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")


if __name__ == '__main__':
    unittest.main()