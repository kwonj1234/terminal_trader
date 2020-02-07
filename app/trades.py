import sqlite3
import os
from .general_class import General

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

class Trades(General):
    dbpath = ""
    tablename = "trades"
    fields = ["pk", "account_pk", "ticker", "volume", "price", "mv", "time"]

    def __init__(self, pk, account_pk, ticker, volume, price, mv, time):
        self.pk = pk
        self.account_pk = account_pk
        self.ticker = ticker
        self.price = price
        self.volume = volume
        self.mv = mv
        self.time = time
    
    # def save(self):
    #     if self.pk is None:
    #         self._insert()
    #     self._update()

    # def _insert(self): 
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """INSERT INTO {} (account_pk, ticker, volume, price, mv, time)
    #             VALUES (?,?,?,?,?,?);""".format(self.tablename)

    #         values = (self.account_pk, self.ticker, self.volume, self.price, \
    #             self.mv, self.time)
    #         c.execute(sql, values)

    # def _update(self): #update accounts that are already in database
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """UPDATE {} SET account_pk = ?, ticker = ?, volume = ?, 
    #             price = ?, mv = ?, time = ?
    #             WHERE pk = ?;""".format(self.tablename)

    #         values = (self.account_pk, self.ticker, self.volume, self.price, \
    #             self.mv, self.time, self.pk)
    #         c.execute(sql, values)

    # @classmethod
    # def select_all(cls, user_pk, ticker = None):
    #     """select all entries from our database based on whether they are complete or not,
    #     or selects all if complete = None"""
    #     with sqlite3.connect(cls.dbpath) as conn:
    #         conn.row_factory = sqlite3.Row 
    #         c = conn.cursor()
    #         if ticker == None:
    #             sql = """SELECT * FROM {} WHERE account_pk = ?;""".format(cls.tablename)
    #             c.execute(sql, (user_pk,))
    #         else:
    #             sql = """SELECT * FROM {} WHERE account_pk = ? and ticker = ?;""".format(cls.tablename)
    #             c.execute(sql, (user_pk, ticker))

    #         rows = c.fetchall() 
    #         return [cls(**row) for row in rows]
