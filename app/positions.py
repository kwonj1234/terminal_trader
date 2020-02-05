import sqlite3
import os
from .util import get_price

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

class Positions:
    dbpath = ""
    tablename = "positions"

    def __init__(self, pk, ticker, shares, account_pk):
        self.pk = pk
        self.ticker = ticker
        self.shares = shares
        self.account_pk = account_pk

    def save(self):
        if self.pk is None:
            self._insert()
        self._update()

    def _insert(self): 
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """INSERT INTO {} (ticker, shares, account_pk)
                VALUES (?,?,?);""".format(self.tablename)

            values = (self.ticker, self.shares, self.account_pk)
            c.execute(sql, values)

    def _update(self): 
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """UPDATE {} SET ticker = ?, shares = ?, account_pk = ?
                WHERE pk = ?;""".format(self.tablename)

            values = (self.ticker, self.shares, self.account_pk, self.pk)
            c.execute(sql, values)

    @classmethod
    def select_one(cls, ticker):
        with sqlite3.connect(cls.dbpath) as conn:
            c = conn.cursor()
            sql = f"""SELECT * FROM {cls.tablename} WHERE ticker == ?"""

            c.execute(sql, (ticker,))
            position = c.fetchall()
            #if position does not exist, return false
            if len(position) == 0 :
                return False

            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(sql, (ticker,))
            position = c.fetchone()
            position = cls(**position)
            return position
    
    def __repr__(self):
        return f"<{self.pk}, {self.ticker}>"