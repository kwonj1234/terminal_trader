import sqlite3
import os
import time
from .util import hash_password, get_price
from .trades import Trades
from .positions import Positions
from .general_class import General

class Account(General):
    dbpath = ""
    tablename = "accounts"
    fields = ["pk", "fname", "lname", "username", "password", "salt", "balance"]

    def __init__(self, pk, fname, lname, username, password, salt, balance):
        self.pk = pk
        self.fname = fname 
        self.lname = lname
        self.username = username
        self.password = password
        self.salt = salt
        self.balance = balance

    # def save(self):
    #     if self.pk is None:
    #         self._insert()
    #     self._update()

    # def _insert(self): #inset new account if it doesn't exist
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """INSERT INTO {} (fname, lname, username, password, salt, balance)
    #             VALUES (?,?,?,?,?,?);""".format(self.tablename)

    #         values = (self.fname, self.lname, self.username, self.password, self.salt, self.balance)
    #         c.execute(sql, values)

    # def _update(self): #update accounts that are already in database
    #     with sqlite3.connect(self.dbpath) as conn:
    #         c = conn.cursor()
    #         sql = """UPDATE {} SET 
    #             fname = ?, 
    #             lname = ?, 
    #             username = ?, 
    #             password = ?,
    #             salt = ?,
    #             balance = ?
    #             WHERE pk = ?;""".format(self.tablename)

    #         values = (self.fname, self.lname, self.username, self.password, self.salt, self.balance, self.pk)
    #         c.execute(sql, values)

    # @classmethod
    # def select_one(cls, pk):
    #     #selects one entry from the database
    #     with sqlite3.connect(cls.dbpath) as conn:
    #         conn.row_factory = sqlite3.Row
    #         c = conn.cursor()

    #         sql = f"""SELECT * FROM {cls.tablename} WHERE pk =?;"""
    #         c.execute(sql, (pk,))
    #         row = c.fetchone()
    #         return cls(**row)
    
    @classmethod
    def no_repeat_usernames(cls,username): #make sure people don't have duplicate usernames
        with sqlite3.connect(cls.dbpath) as conn:
            c = conn.cursor()

            sql = f"""SELECT username FROM {cls.tablename}"""
            c.execute(sql)
            current_users = c.fetchall()
            if username in [user[0] for user in current_users]:
                return False
            return True

    @classmethod
    def validate(cls, username, password):
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            sql = f"""SELECT * FROM {cls.tablename} WHERE username == ?"""

            #check username
            c.execute(sql, (username,))
            user = c.fetchone()

            #if username does not exist
            if user is None:
                return False
            user = cls(**user)

            #check password
            login_pass = password + user.salt
            login_pass = hash_password(login_pass)

            #if password is incorrect
            if login_pass != user.password:
                return False
            
            return user

    def purchase_lots(self, ticker, lots, price, mv): 
        #lots are by 100 shares!
        #Error handling for insufficient funds
        if self.balance < mv:
            return False

        #Enter trade and position in tables
        ticker = ticker.upper()
        position = Positions.select_one("account_pk = ? AND ticker = ?", 
                    (self.pk, ticker))
        if position == False: #returns false if the position does not exist
            position = Positions(None, ticker, lots, self.pk)

        else:
            position.lots += lots
        trade = Trades(None, self.pk, ticker, lots, price, mv, time.time())
        position.save()
        trade.save()

        return position

    def sell_lots(self, ticker, lots, price, mv):
        #shares are by 100!
        price = -1*price #negative numbers represent sales in the database
        mv = -1*mv
        #Enter trade and position in tables
        ticker = ticker.upper()
        position = Positions.select_one("account_pk = ? AND ticker = ?", 
                    (self.pk, ticker))
        if position == False:
            return "no shares"
        elif position.lots < lots:
            return "insufficient shares"
        else:
            position.lots -= lots

        trade = Trades(None, self.pk, ticker, lots, -1*price, mv, time.time())
        position.save()
        trade.save()
        return position
        
    
    # @classmethod
    # def validate_password(cls, username, password)

    def __repr__(self):
        return f"<{self.pk} , {self.username}>"
