import logging
import sqlite3


class SQLiteCore:

    def __init__(self, db_location):
        logging.basicConfig(filename='data/DB.log', filemode='w', level=logging.DEBUG,
                            format='%(asctime)s-%(levelname)s-%(message)s')
        self.cursor = None
        self.connection = None
        self.db_location = db_location

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_location, check_same_thread=True)
            logging.debug('Connection to DB successful!')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logging.error(f"Rise exception: {e}")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def select(self, query):
        self.create_connection()
        self.cursor.execute(query)
        logging.info(f'Execute SELECT QUERY with argument "{query}"')
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    def update(self, query):
        self.create_connection()
        self.cursor.execute(query)
        logging.info(f'Execute UPDATE QUERY with argument "{query}"')
        self.connection.commit()
        self.close_connection()

    def insert(self, query):
        self.create_connection()
        self.cursor.execute(query)
        logging.info(f'Execute INSERT QUERY with argument "{query}"')
        self.connection.commit()
        self.close_connection()
