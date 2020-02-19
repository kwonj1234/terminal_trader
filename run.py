import os
from app import Account, Positions, Trades, run
from app import app as flask_app

DIR = os.path.dirname(__file__)
DBFILENAME = "teller.db"
DBPATH = os.path.join(DIR, 'data', DBFILENAME)

Account.dbpath = DBPATH
Positions.dbpath = DBPATH
Trades.dbpath = DBPATH

if __name__ == "__main__":
    flask_app.run(debug=True)