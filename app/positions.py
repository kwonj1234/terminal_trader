import sqlite3
import os
from .util import get_price

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "teller.db")

class Positions:
    dbpath = DBPATH
    tablename = "positions"

    def __init__(self, pk, ticker, shares, account_pk):
        self.pk = pk
        self.ticker = ticker
        self.shares = shares
        self.account_pk = account_pk

    