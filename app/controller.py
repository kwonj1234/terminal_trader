from app.accounts import Account
from app.trades import Trades
from app.positions import Positions
from app.util import hash_password, get_price
from app import view
import os
import random


def run():
    while True:
        choice = view.main_menu()

        if choice == "3": #Exit
            return 

        elif choice == "1": #Create Account
            view.create_account()
            fname = view.first_name()
            lname = view.last_name()

            #Get username, no repeats
            username = view.new_username()
            while Account.no_repeat_usernames(username) == False:
                view.repeat_username()
                username = view.new_username()
            
            #Get password, getpass is on so make sure it's the correct one by making user put it in twice
            password1, password2 = "a","b"
            salt = str(os.urandom(64))
            while password1 != password2:
                password1, password2 = view.create_password()
                if password1 != password2:
                    view.pass_dont_match()
            #create a hashed salted password
            hashpassword = hash_password(password1 + salt)
            
            initial = view.initial_deposit()
            view.new_account()

            #save new account info into database
            new_account = Account(None, fname, lname, username, hashpassword, salt, initial)
            new_account.save()

        elif choice == "2":#log in
            username, password = view.login()

            #Check if login username is correct
            user = Account.validate(username, password)
            while user == False: #Error handling if username doesn't exist
                view.bad_login()
                username, password = view.login()
                user = Account.validate(username, password)
                
            view.welcome(user.fname, user.lname)

            #Login Menu
            while True:
                choice = view.login_menu()
                if choice == "8": #Sign Out
                    view.signout()
                    return
                
                if choice == "1": #Check Balance
                    view.check_balance(user.balance)
                
                elif choice == "2": #Deposit into balance
                    deposit = view.deposit()
                    #Error handling for non-numeric inputs
                    while deposit.isnumeric() == False:
                        view.not_dollar()
                        deposit = view.deposit()
                    #Add then display new balance
                    user.balance += float(deposit)
                    view.new_balance(user.balance)
                    user.save()
                
                elif choice == "3": #purchase shares
                    purchase_shares(user)   #line 118

                elif choice == "4": #sell shares
                    sell_shares(user)       #line 164 - similar to purchase shares

                elif choice == "5": #current positions
                    position = Positions.select_all(user.pk)
                    for index in range(0,len(position)):
                        current_price = get_price(position[index].ticker)
                        mv = 100 * position[index].shares * current_price
                        view.display_position(position[index].ticker, position[index].shares, current_price, mv)
                    
                elif choice == "6": #transaction history
                    trade = Trades.select_all(user.pk)
                    view.display_header()
                    for index in range(0,len(trade)):
                        view.display_transactions(trade[index].ticker, \
                            trade[index].volume, trade[index].price, \
                                trade[index].mv, trade[index].time)

                elif choice == "7": #get a quote
                    ticker = view.which_stock()
                    price = "error"

                    #exception handling for non-alpha ticker, incorrect ticker
                    while ticker.isalpha() == False or price == "error":
                        if ticker.isalpha() == False:
                            view.not_ticker
                            ticker = view.buy_stock()
                        elif price == "error":
                            try:
                                price = get_price(ticker)
                            except Exception:
                                view.incorrect_ticker()
                                ticker = view.which_stock()
                    ticker = ticker.upper()

                    view.display_price(ticker, price)      

def purchase_shares(user):
    ticker = view.buy_stock()
    price = "error"

    #exception handling for non-alpha ticker, incorrect ticker
    while ticker.isalpha() == False or price == "error":
        if ticker.isalpha() == False:
            view.not_ticker
            ticker = view.buy_stock()
        elif price == "error":
            try:
                price = get_price(ticker)
            except Exception:
                view.incorrect_ticker()
                ticker = view.buy_stock()
    ticker = ticker.upper()

    shares = view.buy_shares()
    #exception handling for shares input
    while shares.isnumeric() == False:
        view.bad_input()
        shares = view.buy_shares()
    shares = float(shares) 

    #market value
    mv = shares*price*100 #shares are in 100 shares
    #confirm the buy order
    confirm = view.confirm_buy(ticker, shares, price, mv)
    if confirm.lower() == "n":
        return
    elif confirm.lower() == "y":
        pass
    else:
        view.bad_input()
        confirm = view.confirm_buy(ticker, shares, price, mv)

    position = user.purchase_shares(ticker, shares, price, mv)
    while position == False:
        view.insufficient_funds
        return
    
    user.balance -= mv
    user.save()

    view.display_buy(ticker, shares, price, user.balance)

def sell_shares(user):
    ticker = view.sell_stock()
    price = "error"

    #exception handling for non-alpha ticker, incorrect ticker
    while ticker.isalpha() == False or price == "error":
        if ticker.isalpha() == False:
            view.not_ticker
            ticker = view.sell_stock()
        elif price == "error":
            try:
                price = get_price(ticker)
            except Exception:
                view.incorrect_ticker()
                ticker = view.sell_stock()
    
    shares = view.sell_shares()
    #exception handling for shares input
    while shares.isnumeric() == False:
        view.bad_input()
        shares = view.sell_shares()
    shares = float(shares) 

    #market value
    mv = shares*price*100 #shares are in 100 shares
    #confirm the sell order
    confirm = view.confirm_sell(ticker, shares, price, mv)
    if confirm.lower() == "n":
        return
    elif confirm.lower() == "y":
        pass
    else:
        view.bad_input()
        confirm = view.confirm_sell(ticker, shares, price, mv)
    
    position_status = False
    while position_status == False:
        position = user.sell_shares(ticker, shares, price, mv)
        if position == "no shares":
            view.no_positions(ticker)
        elif position == "insufficient shares":
            view.insufficient_shares(ticker)
        else:
            position_status = True

    user.balance += mv
    user.save()

    view.display_sell(ticker, shares, price, user.balance)

