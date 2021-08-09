'''
Handles database stuff
TODO: Replace with a more serious db, make async, etc
'''
import sqlite3
import os

from currencies import Currency

DB_NAME = "database.db" #TODO: Move to external config file or allow supplying via parameter

def db_init():
    '''Initializes/reinitializes the db if we have no users'''
    db_connection = db_get_connection()
    if db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")\
        .fetchone() is None:
        print("Initializing DB...")
        with open(os.path.join(os.path.dirname(__file__),'schema.sql')) as file:
            db_connection.executescript(file.read())
            db_connection.commit()
    else: # For quick testing, lets just print the valid user ids. Usually you'd just do this with a DB client
        db_cursor = db_connection.execute("SELECT uuid FROM users")
        rows = db_cursor.fetchall()
        print("Registered user uuids:")
        print(rows)
    db_return_connetion(db_connection)

def db_get_connection():
    '''
    Opens a connection to the db and returns a cursor. Remember to always close these!
    TODO: Pooling
    '''
    db_connection = sqlite3.connect(DB_NAME)
    # We want to commit manually so we can abort transactions in the middle without them getting half commited
    db_connection.isolation_level = None
    db_connection.execute("PRAGMA foreign_keys = 1")
    return db_connection

def db_return_connetion(db_connection):
    '''
    Releases the resources for the cursor
    TODO: Pooling
    '''
    db_connection.close()

def db_balance_table_name(currency: Currency):
    return currency.name+"_balances"
