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

    def __repr__(self):
        return f"<{self.pk}, {self.ticker}>"
