#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import user
from models.base_model import BaseModel
import pep8
import unittest
User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""
    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Test that User has attr email, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        if models.storage_t == 'db':
            self.assertEqual(user.email, None)
        else:
            self.assertEqual(user.email, "")

    def test_password_attr(self):
        """Test that User has attr password, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        if models.storage_t == 'db':
            self.assertEqual(user.password, None)
        else:
            self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """Test that User has attr first_name, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.first_name, None)
        else:
            self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Test that User has attr last_name, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.last_name, None)
        else:
            self.assertEqual(user.last_name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))#!/usr/bin/python3
"""Defines unnittests for models/user.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestUser(unittest.TestCase):
    """Unittests for testing the User class."""

    @classmethod
    def setUpClass(cls):
        """User testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and User instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.user = User(email="poppy@holberton.com", password="betty98")

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """User testing teardown.

        Restore original file.json.
        Delete the FileStorage, DBStorage and User test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.user
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/user.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(User.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        us = User(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "email"))
        self.assertTrue(hasattr(us, "password"))
        self.assertTrue(hasattr(us, "first_name"))
        self.assertTrue(hasattr(us, "last_name"))
        self.assertTrue(hasattr(us, "places"))
        self.assertTrue(hasattr(us, "reviews"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_email_not_nullable(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_is_subclass(self):
        """Check that User is a subclass of BaseModel."""
        self.assertTrue(issubclass(User, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.user, User)

    def test_two_models_are_unique(self):
        """Test that different User instances are unique."""
        us = User(email="a", password="a")
        self.assertNotEqual(self.user.id, us.id)
        self.assertLess(self.user.created_at, us.created_at)
        self.assertLess(self.user.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = User("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.user.__str__()
        self.assertIn("[User] ({})".format(self.user.id), s)
        self.assertIn("'id': '{}'".format(self.user.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.user.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.user.updated_at)), s)
        self.assertIn("'email': '{}'".format(self.user.email), s)
        self.assertIn("'password': '{}'".format(self.user.password), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old = self.user.updated_at
        self.user.save()
        self.assertLess(old, self.user.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("User." + self.user.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.user.updated_at
        self.user.save()
        self.assertLess(old, self.user.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `users` \
                         WHERE BINARY email = '{}'".
                       format(self.user.email))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.user.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        user_dict = self.user.to_dict()
        self.assertEqual(dict, type(user_dict))
        self.assertEqual(self.user.id, user_dict["id"])
        self.assertEqual("User", user_dict["__class__"])
        self.assertEqual(self.user.created_at.isoformat(),
                         user_dict["created_at"])
        self.assertEqual(self.user.updated_at.isoformat(),
                         user_dict["updated_at"])
        self.assertEqual(self.user.email, user_dict["email"])
        self.assertEqual(self.user.password, user_dict["password"])


if __name__ == "__main__":
    unittest.main()
