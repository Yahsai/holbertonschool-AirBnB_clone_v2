import unittest
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os

class TestDBStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configura las variables de entorno necesarias para la conexión a la base de datos de prueba
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_MYSQL_USER'] = 'your_mysql_user'
        os.environ['HBNB_MYSQL_PWD'] = 'your_mysql_password'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'your_test_database'
        # Vuelve a cargar el almacenamiento para que utilice la base de datos de prueba
        storage.reload()

    def setUp(self):
        # Limpiar la base de datos antes de cada prueba
        storage.delete()

    def test_create_user(self):
        user = User(email="test@example.com", password="test")
        storage.new(user)
        storage.save()
        self.assertIn(user, storage.all(User).values())

    def test_create_state(self):
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertIn(state, storage.all(State).values())

    # Agrega más pruebas para los otros modelos

    @classmethod
    def tearDownClass(cls):
        # Cierra la conexión a la base de datos de prueba
        storage.close()

if __name__ == '__main__':
    unittest.main()
