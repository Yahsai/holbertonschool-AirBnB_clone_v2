#!/usr/bin/python3
""" """
import unittest
from models.review import Review
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from datetime import datetime


class TestReview(unittest.TestCase):
    """Test cases for the Review class"""

    def setUp(self):
        """Set up testing environment"""
        self.review = Review()

    def tearDown(self):
        """Tear down testing environment"""
        del self.review

    def test_inheritance(self):
        """Test inheritance"""
        self.assertIsInstance(self.review, BaseModel)

    def test_attributes(self):
        """Test attributes"""
        self.assertTrue(hasattr(self.review, 'id'))
        self.assertTrue(hasattr(self.review, 'created_at'))
        self.assertTrue(hasattr(self.review, 'updated_at'))
        self.assertTrue(hasattr(self.review, 'text'))
        self.assertTrue(hasattr(self.review, 'place_id'))
        self.assertTrue(hasattr(self.review, 'user_id'))

    def test_defaults(self):
        """Test default values"""
        self.assertEqual(self.review.text, "")
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")

    def test_to_dict_method(self):
        """Test to_dict method"""
        review_dict = self.review.to_dict()
        self.assertEqual(type(review_dict), dict)
        self.assertTrue('id' in review_dict)
        self.assertTrue('created_at' in review_dict)
        self.assertTrue('updated_at' in review_dict)
        self.assertTrue('text' in review_dict)
        self.assertTrue('place_id' in review_dict)
        self.assertTrue('user_id' in review_dict)
        self.assertEqual(review_dict['__class__'], 'Review')

    def test_init_method(self):
        """Test __init__ method"""
        review = Review(text="Great place!", place_id="12345", user_id="54321")
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.place_id, "12345")
        self.assertEqual(review.user_id, "54321")


if __name__ == '__main__':
    unittest.main()