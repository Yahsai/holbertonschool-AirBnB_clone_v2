import unittest
from unittest.mock import patch
import sys
import io
import MySQLdb
from models.review import Review

class TestMySQLReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySQLdb.connect(host="HBNB_MYSQL_HOST",
                                  user="HBNB_MYSQL_USER",
                                  passwd="HBNB_MYSQL_PWD",
                                  db="HBNB_MYSQL_DB")

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        self.review = Review(text="TestReviewText",
                             place_id="TestPlaceID",
                             user_id="TestUserID")
        self.output = io.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_save_review(self):
        with patch('sys.stdin', io.StringIO('')):
            self.review.save()

        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE text='TestReviewText'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
