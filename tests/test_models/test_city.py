#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""

from datetime import datetime
import inspect
import models
from models import city
from models.base_model import BaseModel
import pep8
import unittest
City = city.City


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertIsNot(city.__doc__, None,
                         "city.py needs a docstring")
        self.assertTrue(len(city.__doc__) >= 1,
                        "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(City.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCity(unittest.TestCase):
    """Test the City class"""
    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_name_attr(self):
        """Test that City has attribute name, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        if models.storage_t == 'db':
            self.assertEqual(city.name, None)
        else:
            self.assertEqual(city.name, "")

    def test_state_id_attr(self):
        """Test that City has attribute state_id, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        if models.storage_t == 'db':
            self.assertEqual(city.state_id, None)
        else:
            self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        c = City()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in c.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = City()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))#!/usr/bin/python3
"""Defines unnittests for models/city.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestCity(unittest.TestCase):
    """Unittests for testing the City class."""

    @classmethod
    def setUpClass(cls):
        """City testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage, City and State instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """City testing teardown.

        Restore original file.json.
        Delete the FileStorage, DBStorage, City and State test instances.
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
        p = style.check_files(["models/city.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        ct = City()
        self.assertEqual(str, type(ct.id))
        self.assertEqual(datetime, type(ct.created_at))
        self.assertEqual(datetime, type(ct.updated_at))
        self.assertTrue(hasattr(ct, "__tablename__"))
        self.assertTrue(hasattr(ct, "name"))
        self.assertTrue(hasattr(ct, "state_id"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        """Check that relevant DBStorage attributes are non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(
                state_id=self.state.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(name="San Jose"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_state_relationship_deletes(self):
        """Test delete cascade in City-State relationship."""
        st = State(name="Georgia")
        self.dbstorage._DBStorage__session.add(st)
        self.dbstorage._DBStorage__session.commit()
        ct = City(name="Atlanta", state_id=st.id)
        self.dbstorage._DBStorage__session.add(ct)
        self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.delete(st)
        self.dbstorage._DBStorage__session.commit()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cities WHERE BINARY name = 'Atlanta'")
        query = cursor.fetchall()
        cursor.close()
        self.assertEqual(0, len(query))

    def test_is_subclass(self):
        """Check that City is a subclass of BaseModel."""
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.city, City)

    def test_two_models_are_unique(self):
        """Test that different City instances are unique."""
        ct = City()
        self.assertNotEqual(self.city.id, ct.id)
        self.assertLess(self.city.created_at, ct.created_at)
        self.assertLess(self.city.updated_at, ct.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        ct = City("1", id="5", created_at=dt.isoformat())
        self.assertEqual(ct.id, "5")
        self.assertEqual(ct.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.city.__str__()
        self.assertIn("[City] ({})".format(self.city.id), s)
        self.assertIn("'id': '{}'".format(self.city.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.city.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.city.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.city.name), s)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old = self.city.updated_at
        self.city.save()
        self.assertLess(old, self.city.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("City." + self.city.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.city.updated_at
        self.state.save()
        self.city.save()
        self.assertLess(old, self.city.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `cities` \
                         WHERE BINARY name = '{}'".
                       format(self.city.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.city.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        city_dict = self.city.to_dict()
        self.assertEqual(dict, type(city_dict))
        self.assertEqual(self.city.id, city_dict["id"])
        self.assertEqual("City", city_dict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         city_dict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         city_dict["updated_at"])
        self.assertEqual(self.city.name, city_dict["name"])
        self.assertEqual(self.city.state_id, city_dict["state_id"])


if __name__ == "__main__":
    unittest.main()
