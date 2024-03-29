import unittest
from unittest.mock import patch
import sys
import io
import MySQLdb
from console import HBNBCommand

class TestMySQLConsole(unittest.TestCase):
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
        self.console = HBNBCommand()
        self.output = io.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_create_city(self):
        command = "create City name=\"TestCity\" state_id=\"TestState\""
        with patch('sys.stdin', io.StringIO(command + '\n')):
            self.console.cmdloop()

        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities WHERE name='TestCity'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
