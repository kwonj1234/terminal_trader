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
