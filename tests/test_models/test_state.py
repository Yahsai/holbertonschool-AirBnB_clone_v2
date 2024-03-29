#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest
State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

class TestState(unittest.TestCase):
    """Test the State class"""
    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's as an empty string"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))#!/usr/bin/python3
"""Defines unnittests for models/state.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestState(unittest.TestCase):
    """Unittests for testing the State class."""

    @classmethod
    def setUpClass(cls):
        """State testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and State instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Jose", state_id=cls.state.id)

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """State testing teardown.

        Restore original file.json.
        Delete the FileStorage, DBStorage and State test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/state.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(State.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        st = State()
        self.assertEqual(str, type(st.id))
        self.assertEqual(datetime, type(st.created_at))
        self.assertEqual(datetime, type(st.updated_at))
        self.assertTrue(hasattr(st, "name"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        """Check that relevant DBStorage attributes are non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(State())
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_cities(self):
        """Test reviews attribute."""
        key = "{}.{}".format(type(self.city).__name__, self.city.id)
        self.filestorage._FileStorage__objects[key] = self.city
        cities = self.state.cities
        self.assertTrue(list, type(cities))
        self.assertIn(self.city, cities)

    def test_is_subclass(self):
        """Check that State is a subclass of BaseModel."""
        self.assertTrue(issubclass(State, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.state, State)

    def test_two_models_are_unique(self):
        """Test that different State instances are unique."""
        st = State()
        self.assertNotEqual(self.state.id, st.id)
        self.assertLess(self.state.created_at, st.created_at)
        self.assertLess(self.state.updated_at, st.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = State("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.state.__str__()
        self.assertIn("[State] ({})".format(self.state.id), s)
        self.assertIn("'id': '{}'".format(self.state.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.state.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.state.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.state.name), s)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.state.updated_at
        self.state.save()
        self.assertLess(old, self.state.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `states` \
                         WHERE BINARY name = '{}'".
                       format(self.state.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.state.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        state_dict = self.state.to_dict()
        self.assertEqual(dict, type(state_dict))
        self.assertEqual(self.state.id, state_dict["id"])
        self.assertEqual("State", state_dict["__class__"])
        self.assertEqual(self.state.created_at.isoformat(),
                         state_dict["created_at"])
        self.assertEqual(self.state.updated_at.isoformat(),
                         state_dict["updated_at"])
        self.assertEqual(self.state.name, state_dict["name"])


if __name__ == "__main__":
    unittest.main()
