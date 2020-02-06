import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

def schema(dbpath = DBPATH):
    with sqlite3.connect(dbpath) as connection:
        c = connection.cursor()

        #create an accounts table
        c.execute("""CREATE TABLE accounts (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                fname VARCHAR,
                lname VARCHAR,
                username VARCHAR,
                password VARCHAR,
                salt VARCHAR(64),
                balance FLOAT
                );""")
        
        #create a positions table
        c.execute("""CREATE TABLE positions (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker VARCHAR,
                lots INTEGER,
                account_pk INTEGER,
                FOREIGN KEY (account_pk) REFERENCES account(pk)
                );""")

        #create a trades table
        c.execute("""CREATE TABLE trades (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                account_pk INTEGER,
                time INTEGER,
                ticker VARCHAR,
                price FLOAT,
                volume FLOAT,
                mv FLOAT, 
                FOREIGN KEY (account_pk) REFERENCES accounts(pk)
                );""") 
                #volume in lots = 100 shares
                #mv = market value 

if __name__ == "__main__":
    schema()