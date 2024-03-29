#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

from datetime import datetime
import inspect
import models
from models import review
from models.base_model import BaseModel
import pep8
import unittest
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Test the Review class"""
    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attr place_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.place_id, None)
        else:
            self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.user_id, None)
        else:
            self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if models.storage_t == 'db':
            self.assertEqual(review.text, None)
        else:
            self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))#!/usr/bin/python3
"""Defines unnittests for models/review.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestReview(unittest.TestCase):
    """Unittests for testing the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review testing setup.
        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and Review instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id,
                            user_id=cls.user.id)

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Review testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Review test instances.
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
        del cls.user
        del cls.place
        del cls.review
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/review.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        us = Review(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "text"))
        self.assertTrue(hasattr(us, "place_id"))
        self.assertTrue(hasattr(us, "user_id"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                place_id=self.place.id, user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", place_id=self.place.id))
            self.dbstorage._DBStorage__session.commit()

    def test_is_subclass(self):
        """Check that Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.review, Review)

    def test_two_models_are_unique(self):
        """Test that different Review instances are unique."""
        us = Review(email="a", password="a")
        self.assertNotEqual(self.review.id, us.id)
        self.assertLess(self.review.created_at, us.created_at)
        self.assertLess(self.review.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = Review("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.review.__str__()
        self.assertIn("[Review] ({})".format(self.review.id), s)
        self.assertIn("'id': '{}'".format(self.review.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.review.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.review.updated_at)), s)
        self.assertIn("'text': '{}'".format(self.review.text), s)
        self.assertIn("'place_id': '{}'".format(self.review.place_id), s)
        self.assertIn("'user_id': '{}'".format(self.review.user_id), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old = self.review.updated_at
        self.review.save()
        self.assertLess(old, self.review.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Review." + self.review.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.review.updated_at
        self.state.save()
        self.city.save()
        self.user.save()
        self.place.save()
        self.review.save()
        self.assertLess(old, self.review.updated_at)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `reviews` \
                         WHERE BINARY text = '{}'".
                       format(self.review.text))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.review.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        review_dict = self.review.to_dict()
        self.assertEqual(dict, type(review_dict))
        self.assertEqual(self.review.id, review_dict["id"])
        self.assertEqual("Review", review_dict["__class__"])
        self.assertEqual(self.review.created_at.isoformat(),
                         review_dict["created_at"])
        self.assertEqual(self.review.updated_at.isoformat(),
                         review_dict["updated_at"])
        self.assertEqual(self.review.text, review_dict["text"])
        self.assertEqual(self.review.place_id, review_dict["place_id"])
        self.assertEqual(self.review.user_id, review_dict["user_id"])


if __name__ == "__main__":
    unittest.main()
