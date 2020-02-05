import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "~/kaiju/terminal_trader/data/teller.db")

class Trades:
    dbpath = ""
    tablename = "trades"

    def __init__(self, pk, account_pk, ticker, volume, price, mv, time):
        self.pk = pk
        self.account_pk = account_pk
        self.ticker = ticker
        self.price = price
        self.volume = volume
        self.mv = mv
        self.time = time
    
    def save(self):
        if self.pk is None:
            self._insert()
        self._update()

    def _insert(self): 
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """INSERT INTO {} (account_pk, ticker, volume, price, mv, time)
                VALUES (?,?,?,?,?,?);""".format(self.tablename)

            values = (self.account_pk, self.ticker, self.volume, self.price, \
                self.mv, self.time)
            c.execute(sql, values)

    def _update(self): #update accounts that are already in database
        with sqlite3.connect(self.dbpath) as conn:
            c = conn.cursor()
            sql = """UPDATE {} SET account_pk = ?, ticker = ?, volume = ?, 
                price = ?, mv = ?, time = ?
                WHERE pk = ?;""".format(self.tablename)

            values = (self.account_pk, self.ticker, self.volume, self.price, \
                self.mv, self.time, self.pk)
            c.execute(sql, values)
