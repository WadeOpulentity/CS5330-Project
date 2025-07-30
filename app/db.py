import mysql.connector
from flask import g
from config import DB_USERNAME, DB_PASSWORD, DB_NAME

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
