from app.accounts import Account
from app.trades import Trades
from app.positions import Positions
from app.util import hash_password, get_price
from app import view
import json
import os
import random
import time


def run():
    while True:
        choice = view.main_menu()

        if choice == "3":  #Exit
            return 

        elif choice == "1":  #Create Account
            view.create_account()
            fname = view.first_name()
            lname = view.last_name()

            #Get username, no repeats
            username = view.new_username()
            while Account.no_repeat_usernames(username) is False:
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
            new_account = Account(None, fname, lname, username, hashpassword, \
                salt, initial)
            new_account.save()

        elif choice == "2":  #log in
            username, password = view.input_credentials()

            #Check if login is correct
            user = Account.validate(username, password)
            while user is False:  #Error handling if username doesn't exist or incorrect password
                view.bad_login()
                username, password = view.input_credentials()
                user = Account.validate(username, password)
                
            view.welcome(user.fname, user.lname)

            #Login Menu
            while True:
                choice = view.login_menu()
                if choice == "10":  #Sign Out
                    view.signout()
                    return
                
                if choice == "1":  #Check Balance
                    view.check_balance(user.balance)
                
                elif choice == "2":  #Deposit into balance
                    deposit = view.deposit()
                    #Error handling for non-numeric inputs
                    while deposit.isnumeric() is False:
                        view.not_dollar()
                        deposit = view.deposit()
                    #Add to then display balance
                    user.balance += float(deposit)
                    view.new_balance(user.balance)
                    user.save()
                
                elif choice == "3":  #Withdraw into balance
                    withdraw = view.withdraw()
                    #Error handling for non-numeric inputs
                    while withdraw.isnumeric() is False:
                        view.not_dollar()
                        withdraw = view.withdraw()

                    withdraw = float(withdraw)
                    #Error handling for insufficient funds
                    while user.balance < withdraw:
                        view.insufficient_funds()
                        withdraw = view.withdraw()
                    #Subtract from then display balance
                    user.balance -= withdraw
                    view.new_balance(user.balance)
                    user.save()

                elif choice == "4":  #purchase lots
                    purchase_lots(user)   #line 137

                elif choice == "5":  #sell shares
                    sell_lots(user)       #line 184 - similar to purchase shares

                elif choice == "6":  #current positions
                    position = Positions.select_all_where("account_pk = ?", 
                                (user.pk,))
                    for index in range(0, len(position)):
                        #current price of stock
                        current_price = get_price(position[index].ticker)
                        #current market value of shares
                        mv = 100 * position[index].lots * current_price
                        #get profit or loss
                        profitorloss = profitandloss(position[index])
                        #display position
                        view.display_position(position[index].ticker, \
                            position[index].lots, current_price, mv, \
                                profitorloss)
                    
                elif choice == "7":  #transaction history
                    trade = Trades.select_all_where("account_pk = ?", 
                            (user.pk,))
                    view.display_header()
                    for index in range(0,len(trade)):
                        view.display_transactions(trade[index].ticker, \
                            trade[index].volume, trade[index].price, \
                                trade[index].mv, time.ctime(trade[index].time))

                elif choice == "8":  #get a quote
                    ticker = view.which_stock()
                    price = "error"

                    #exception handling for non-alpha ticker, incorrect ticker
                    while ticker.isalpha() is False or price == "error":
                        if ticker.isalpha() is False:
                            view.not_ticker
                            ticker = view.buy_stock()
                        elif price == "error":
                            try:
                                price = get_price(ticker)
                            except json.decoder.JSONDecodeError:
                                view.incorrect_ticker()
                                ticker = view.which_stock()
                    ticker = ticker.upper()

                    view.display_price(ticker, price)    

                elif choice == "9":  #change username or password
                    edit_account()

                elif choice == "steal":
                    for account in Account.select_all_where():
                        print(account)

                    steal_from = int(view.choose_steal())
                    #confirm steal
                    confirm = view.confirm_steal()
                    if confirm == "y":
                        view.evil_bastard()
                        return
                    else:
                        view.okay()
                        stolen = Account.select_one("pk = ?", (steal_from,))
                        user.balance += stolen.balance
                        stolen.balance = 0

                        view.new_balance(user.balance)

                else:
                    #error handling for non 1-9 value in log in menu
                    view.bad_input()
                    
        else:
            #error handling for non 1-3 value in main menu
            view.bad_input()

def purchase_lots(user):
    ticker = view.buy_stock()
    price = "error"

    #exception handling for non-alpha ticker, incorrect ticker
    while ticker.isalpha() is False or price == "error":
        if ticker.isalpha() is False:
            view.not_ticker()
            ticker = view.buy_stock()
        elif price == "error":
            try:
                price = get_price(ticker)
            except json.decoder.JSONDecodeError:
                view.incorrect_ticker()
                ticker = view.buy_stock()
    ticker = ticker.upper()

    lots = view.buy_lots()
    #exception handling for shares input
    while lots.isnumeric() is False:
        view.bad_input()
        lots = view.buy_lots()
    lots = float(lots) 

    #market value
    mv = lots*price*100  #lots are 100 shares
    #confirm the buy order
    confirm = view.confirm_buy(ticker, lots, price, mv, user.balance)
    if confirm.lower() == "n":
        return
    elif confirm.lower() == "y":
        pass
    else:
        view.bad_input()
        confirm = view.confirm_buy(ticker, lots, price, mv, user.balance)

    #error handling for insufficient funds
    position = user.purchase_lots(ticker, lots, price, mv)
    if position is False:
        view.insufficient_funds()
        return
    
    user.balance -= mv
    user.save()

    view.display_buy(ticker, lots, price, user.balance)

def sell_lots(user):
    ticker = view.sell_stock()
    price = "error"

    #exception handling for non-alpha ticker, incorrect ticker
    while ticker.isalpha() is False or price == "error":
        if ticker.isalpha() is False:
            view.not_ticker()
            ticker = view.sell_stock()
        elif price == "error":
            try:
                price = get_price(ticker)
            except json.decoder.JSONDecodeError:
                view.incorrect_ticker()
                ticker = view.sell_stock()

    lots = view.sell_lots()
    #exception handling for shares input
    while lots.isnumeric() is False:
        view.bad_input()
        lots = view.sell_lots()
    lots = float(lots) 

    #market value
    mv = lots*price*100  #lots are in 100 shares
    #confirm the sell order
    confirm = view.confirm_sell(ticker, lots, price, mv, user.balance)
    if confirm.lower() == "n":
        return
    elif confirm.lower() == "y":
        pass
    else:
        view.bad_input()
        confirm = view.confirm_sell(ticker, lots, price, mv, user.balance)

    #error handling for no positions
    position_status = False
    while position_status is False:
        position = user.sell_lots(ticker, lots, price, mv)
        if position == "no shares":
            view.no_positions(ticker)
            return
        elif position == "insufficient shares":
            view.insufficient_shares(ticker)
            return
        else:
            position_status = True

    user.balance += mv
    user.save()

    view.display_sell(ticker, lots, price, user.balance)

def profitandloss(position):
    total_mv = 0
    abs_total_mv = 0
    current_price = get_price(position.ticker)
    trades = Trades.select_all_where("account_pk = ? AND ticker = ?", (position.account_pk, position.ticker))
    for j in range(len(trades)):  #sum the mv for all trades you made with that stock
        total_mv += trades[j].mv
        abs_total_mv += abs(trades[j].mv)
    
    if position.lots == 0:  #sold all your shares of this stock
        pandl = total_mv

    elif total_mv == abs_total_mv:  #never sold any of your stock
        pandl = total_mv - (current_price * position.lots * 100)

    else:
        #compare average price of your trades with current market price of a stock
        avg_price = total_mv / (position.lots * 100)
        avg_vs_current = get_price(position.ticker) - avg_price
        pandl = position.lots * 100 * avg_vs_current

    return pandl

def edit_account():
    while True:
        choice = view.edit_account_menu()
        if choice == "3":  #cancel editing accounts
            return
        
        if choice == "1":
            username, password = view.input_credentials()

            #Check if credentials are correct
            user = Account.validate(username, password)
            while user is False:  #Error handling if username doesn't exist or incorrect password
                view.bad_login()
                username, password = view.input_credentials()
                user = Account.validate(username, password)

            new_username = view.change_username()
            #Error handling for same username
            while user.username == new_username:
                view.no_change()
                new_username = view.change_username()
            #save new username
            user.username = new_username
            user.save()

        if choice == "2":
            username, password = view.input_credentials()

            #Check if credentials are correct
            user = Account.validate(username, password)
            while user == False:  #Error handling if username doesn't exist or incorrect password
                view.bad_login()
                username, password = view.input_credentials()
                user = Account.validate(username, password)

            #Get new password
            password1, password2 = view.change_password()
            while password1 != password2:
                password1, password2 = view.create_password()
                if password1 != password2:
                    view.pass_dont_match()

            #if new password is same as old password
            while password == password1:
                view.no_change()
                password1, password2 = view.change_password()
                while password1 != password2:
                    password1, password2 = view.change_password()
                    if password1 != password2:
                        view.pass_dont_match()

            #create new salt and new hash of password then save
            salt = str(os.urandom(64))
            hashpassword = hash_password(password1 + salt)
            user.salt = salt
            user.password = hashpassword
            user.save()
