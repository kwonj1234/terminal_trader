import os
from app import Account, Positions, Trades, run

DIR = os.path.dirname(__file__)
DBFILENAME = "teller.db"
DBPATH = os.path.join(DIR, 'data', DBFILENAME)

Account.dbpath = DBPATH
Positions.dbpath = DBPATH
Trades.dbpath = DBPATH

if __name__ == "__main__":
    run()