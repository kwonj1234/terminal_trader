import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "~/kaiju/terminal_trader/data/teller.db")

class Trades:
    dbpath = DBPATH
    pass