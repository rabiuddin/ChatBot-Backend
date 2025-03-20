import mysql.connector
from mysql.connector import Error
from src.app.config.config import Config

config = Config()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
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
                    cursor = self.connection.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Chats (
                            ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            title TEXT NULL,
                            createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Messages (
                        ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        ChatID INT(11) NOT NULL,
                        HumanMessage TEXT NULL,
                        AIMessage TEXT NULL,
                        CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (ChatID) REFERENCES Chats(ID) ON DELETE CASCADE
                    );
                    """)
                else:
                    print("Failed to connect to MySQL DB")
            except Error as e:
                print(f"The error '{e}' occurred")
                self.connection = None
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")