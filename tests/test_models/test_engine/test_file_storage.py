import unittest
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os

class TestFileStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configura las variables de entorno necesarias para la prueba
        os.environ['HBNB_ENV'] = 'test'
        # Reinicia el almacenamiento para que utilice el archivo de prueba
        storage.reload()

    def setUp(self):
        # Limpiar el archivo de almacenamiento antes de cada prueba
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
        # No necesitamos hacer nada aquí ya que no hay nada que cerrar
        pass

if __name__ == '__main__':
    unittest.main()
