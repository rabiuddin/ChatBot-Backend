import mysql.connector
from mysql.connector import Error
from src.app.config.config import Config

config = Config()

class DatabaseConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    def create_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=config.get_mysql_host(),
                    user=config.get_mysql_user(),
                    password=config.get_mysql_password(),
                    database=config.get_mysql_db(),
                    port=config.get_mysql_port()
                )
                if self.connection.is_connected():
                    print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")
        return self.connection