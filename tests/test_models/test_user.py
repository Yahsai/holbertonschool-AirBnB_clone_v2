import unittest
import MySQLdb

class TestMySQLUser(unittest.TestCase):
    def setUp(self):
        # Establecer la conexión con la base de datos de prueba
        self.db = MySQLdb.connect(host="HBNB_MYSQL_HOST",
                                  user="HBNB_MYSQL_USER",
                                  passwd="HBNB_MYSQL_PWD",
                                  db="HBNB_MYSQL_DB")
        self.cursor = self.db.cursor()

    def tearDown(self):
        # Cerrar la conexión con la base de datos
        self.db.close()

    def test_create_user(self):
        # Obtener el número de registros actual en la tabla users
        self.cursor.execute("SELECT COUNT(*) FROM users")
        initial_count = self.cursor.fetchone()[0]

        # Ejecutar el comando de consola para crear un nuevo usuario
        # Por ejemplo, podrías ejecutar un comando INSERT INTO aquí

        # Obtener el número de registros nuevamente después de ejecutar el comando
        self.cursor.execute("SELECT COUNT(*) FROM users")
        final_count = self.cursor.fetchone()[0]

        # Verificar si se agregó un nuevo registro
        self.assertEqual(final_count - initial_count, 1)

if __name__ == '__main__':
    unittest.main()
