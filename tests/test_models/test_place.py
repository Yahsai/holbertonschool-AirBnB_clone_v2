import unittest
from unittest.mock import patch
import sys
import io
import MySQLdb
from models.place import Place

class TestMySQLPlace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySQLdb.connect(host="localhost",
                                 user="your_mysql_user",
                                 passwd="your_mysql_password",
                                 db="your_test_database")

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        self.place = Place(city_id="TestCityID", user_id="TestUserID",
                           name="TestPlace", description="TestDescription",
                           number_rooms=2, number_bathrooms=1,
                           max_guest=4, price_by_night=100.0,
                           latitude=0.0, longitude=0.0)
        self.output = io.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_save_place(self):
        with patch('sys.stdin', io.StringIO('')):
            self.place.save()

        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM places WHERE name='TestPlace'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
