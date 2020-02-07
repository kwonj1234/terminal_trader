import sqlite3
import os
from .util import get_price
from .general_class import General

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

class Positions(General):
    dbpath = ""
    tablename = "positions"
    fields = ["pk", "ticker", "lots", "account_pk"]

    def __init__(self, pk, ticker, lots, account_pk):
        self.pk = pk
        self.ticker = ticker
        self.lots = lots
        self.account_pk = account_pk

    # def save(self):
    #     if self.pk is None:
    #         self._insert()
    #     self._update()

    # def _insert(self): 
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """INSERT INTO {} (ticker, lots, account_pk)
    #             VALUES (?,?,?);""".format(self.tablename)

    #         values = (self.ticker, self.lots, self.account_pk)
    #         c.execute(sql, values)

    # def _update(self): 
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """UPDATE {} SET ticker = ?, lots = ?, account_pk = ?
    #             WHERE pk = ?;""".format(self.tablename)

    #         values = (self.ticker, self.lots, self.account_pk, self.pk)
    #         c.execute(sql, values)

    # @classmethod
    # def select_one(cls, ticker, account_pk):
    #     with sqlite3.connect(cls.dbpath) as conn:
    #         conn.row_factory = sqlite3.Row
    #         c = conn.cursor()
    #         sql = f"""SELECT * FROM {cls.tablename} WHERE ticker = ? and account_pk = ?"""
    #         c.execute(sql, (ticker, account_pk))
    #         position = c.fetchone()

    #         #if position does not exist, return false
    #         if position is None :
    #             return False
  
    #         return cls(**position)

    # @classmethod
    # def select_all(cls, user_pk):
    #     """select all entries from our database based on whether they are complete or not,
    #     or selects all if complete = None"""
    #     with sqlite3.connect(cls.dbpath) as conn:
    #         conn.row_factory = sqlite3.Row 
    #         c = conn.cursor()

    #         sql = """SELECT * FROM {} WHERE account_pk = ?;""".format(cls.tablename)
    #         c.execute(sql, (user_pk,))

    #         rows = c.fetchall() 
    #         return [cls(**row) for row in rows]
    
    def __repr__(self):
        return f"<{self.pk}, {self.ticker}>"