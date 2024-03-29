#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import unittest
import MySQLdb

class TestStateCreation(unittest.TestCase):
    def setUp(self):
        # Establecer la conexión con la base de datos de prueba
        self.db = MySQLdb.connect(host="localhost",
                                  user="your_mysql_user",
                                  passwd="your_mysql_password",
                                  db="your_test_database")
        self.cursor = self.db.cursor()

    def tearDown(self):
        # Cerrar la conexión con la base de datos
        self.db.close()

    def test_create_state(self):
        # Obtener el número de registros actual en la tabla states
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Ejecutar el comando para crear un nuevo estado "California"
        self.cursor.execute("INSERT INTO states (name) VALUES ('California')")
        self.db.commit()

        # Obtener el número de registros nuevamente después de la ejecución del comando
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]

        # Comparar los recuentos antes y después de la ejecutar el comando
        self.assertEqual(final_count - initial_count, 1)

if __name__ == '__main__':
    unittest.main()
