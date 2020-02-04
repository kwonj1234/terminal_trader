import sqlite3
import os
from .util import hash_password

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "~/kaiju/terminal_trader/data/teller.db")

class Account:
    dbpath = "../data/teller.db"
    tablename = "accounts"

    def __init__(self, pk, fname, lname, username, password, salt, balance):
        self.pk = pk
        self.fname = fname 
        self.lname = lname
        self.username = username
        self.password = hash_password(password + salt)
        self.salt = salt
        self.balance = balance

    def save(self):
        if self.pk is None:
            self._insert()
        self._update()

    def _insert(self): #inset new account if it doesn't exist
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """INSERT INTO {} (fname, lname, username, password, balance)
                VALUES (?,?,?,?,?);""".format(self.tablename)

            values = (self.fname, self.lname, self.username, self.password, self.balance)
            c.execute(sql, values)

    def _update(self): #update accounts that are already in database
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """UPDATE {} SET 
                fname = ?, 
                lname = ?, 
                username = ?, 
                password = ?,
                balance = ?
                WHERE pk = ?;""".format(self.tablename)

            values = (self.fname, self.lname, self.username, self.password, self.balance, self.pk)
            c.execute(sql, values)

    @classmethod
    def select_one(cls, pk):
        #selects one entry from the database
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} WHERE pk =?;"""
            c.execute(sql, (pk,))
            row = c.fetchone()
            return cls(**row)

    @classmethod
    def validate(cls, username, password):
        password = hash_password(password)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            sql = f"""SELECT * FROM {cls.tablename} WHERE username == ? AND password == ?"""

            c.execute(sql, (username,password))
            user = c.fetchone()
            #if username or password is incorrect, return false
            if len(user) == 0: #this doesn't work
                return False
            return cls(**user)

    def __repr__(self):
        return f"<{self.pk} , {self.username}>"
