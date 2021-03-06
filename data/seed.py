import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

def seed(dbpath = DBPATH):
    with sqlite3.connect(dbpath) as connection:
        c = connection.cursor()

        sql = ("""INSERT INTO accounts (
            fname, lname, username, password, salt, balance
            ) VALUES (
            ?,?,?,?,?,?);""")
        # values = ("1", "2", "3", "4", "5". "6")
        c.execute(sql)

        sql = ("""INSERT INTO positions (
            ticker, shares, account_pk 
            ) VALUES (
            ?,?,?);""")
        # values = ("1", "2", "3")
        c.execute(sql)

        sql = ("""INSERT INTO trades (
            account_pk, time, ticker, price, volume, mv
            ) VALUES (
            ?,?,?,?,?,?);""")
        # values = ("1", "2", "3", "4", "5", "6")
        c.execute(sql)
    
if __name__ == "__main__":
    seed()
