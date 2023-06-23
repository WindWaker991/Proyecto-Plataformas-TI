import psycopg2
import os
from dotenv import load_dotenv

# Class to connect to the database
class DBConnection:
    load_dotenv()
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user, password=self.password)

    def execute_query(self, query, params):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def close(self):
        self.conn.close()
    

