from app.accounts import Account
from app.trades import Trades
from app.positions import Positions
from app import view
import os
import random


def run():
    while True:
        choice = view.main_menu()
        if choice == "3": #Exit
            return False
        elif choice == "1": #Create Account
            view.create_account()
            fname = view.first_name()
            lname = view.last_name()
            username = view.new_username()
            password1, password2 = "a","b"
            salt = str(os.urandom(64))

            while password1 != password2:
                password1, password2 = view.create_password()
                if password1 != password2:
                    view.pass_dont_match()
            
            view.new_account()

            #save new account info into database
            new_account = Account(None, fname, lname, username, password1, salt, 0)
            new_account.save()

        elif choice == "2":#log in
            username, password = view.login()

            #Check if login info is correct
            user = Account.validate(username, password)
            if user == False:
                view.bad_login()
            
            view.welcome(user.fname, user.lname)

#TODO I'm up to here


            #Login Menu - Check Balance, Withdraw, Deposit, Open Savings Account
            info = model.Account.login(account_num)
            account_num = model.Account(info["First Name"], info["Last Name"], \
                account_num, info["PIN"], info["checking account"], info["savings account"])
        
            view.welcome(account_num.account_num, account_num.fname, account_num.lname)
            while True:
                choice = view.login_menu()
                if choice == "1": #check balance
                    view.check_balance(info)

                elif choice == "2": #withdraw from checking
                    login_withdrawal(account_num, choice)  #see line 79

                elif choice == "3": #deposit into checking
                    login_deposit(account_num)    #see line 121

                elif choice == "4": #transfer funds
                    login_transfer(account_num)   #see line 134
                
                elif choice == "5": #send money to other accounts
                    login_send_money(account_num)   #see line 165
                    
                elif choice == "6": #create savings
                    yesorno, deposit = view.create_savings()
                    model.Account.open_savings(account_num ,yesorno, float(deposit))
                    model.Account.save(account_num)
                    view.savings_opened(float(deposit))

                elif choice == "7": #sign out
                    view.signout()  
                    return  

                else:
                    view.bad_input()  

        else:
            view.bad_input()

def login_withdrawal(account_num, choice):  #see line 52, withdraw money
    while True:
        choice = view.withdraw()
        #Quick withdrawal 
        if choice.isnumeric() == True:
            if int(choice) in [1,4]:
                #Quick withdrawal options
                list = [10,20,50,100]
                num = list[int(choice) - 1]
                new_balance = model.Account.withdraw(account_num, num)

                #Insufficient funds
                if new_balance == False:
                    view.insufficient_funds()
                    return

                view.withdraw_new_balance(num, new_balance)
                model.Account.save(account_num)

        #Withdraw custom amount
            elif choice == "5":
                num = view.withdraw_custom()

                #error handling
                if num.isnumeric() != True:
                    view.not_dollar()
                    return

                new_balance = model.Account.withdraw(account_num, float(num))
                
                #insufficient funds
                if new_balance == False:
                    view.insufficient_funds()
                    return
                    
                view.withdraw_new_balance(num, new_balance)
                model.Account.save(account_num)
            else:
                view.bad_input()     
        else:
            view.bad_input()

def login_deposit(account_num):   #see line 55
    num = view.deposit()

    #error handling
    while num.isnumeric == False:
        view.not_dollar()
        num = view.deposit()

    num = float(num)
    new_balance = model.Account.deposit(account_num,num)
    view.deposit_new_balance(num, new_balance)
    model.Account.save(account_num)

def login_transfer(account_num):   #see line 57

    from_account = view.transfer_from_account()
    #error handling for non-account inputs
    while from_account != "checking" and from_account != "savings":
        view.bad_transfer()
        from_account = view.transfer_from_account()

    to_account = view.transfer_to_account()
    while to_account != "checking" and to_account != "savings":
        view.bad_transfer()
        to_account = view.transfer_to_account()

    #error handling for non-numeric inputs
    amount = view.transfer_amount()
    while amount.isnumeric() == False:
        view.not_dollar()
        amount = view.transfer_amount()
    
    #convert amount value from string to float
    amount = float(amount)

    #error handling for insufficient funds
    if amount > account_num.transfer_funds[from_account]:
        view.insufficient_funds()
        return

    from_balance, to_balance = model.Account.transfer(account_num, \
        from_account, to_account, amount)
    view.transfer_new_balance(from_balance, to_balance, from_account, to_account)

def login_send_money(account_num):
    #receive inputs as well as error handling
    receiver = view.send_money_account()
    while receiver.isnumeric() == False or len(receiver) > 6 or len(receiver) < 6:
        view.not_account()
        receiver = view.send_money_account()
    
    amount = view.send_money_amount()
    while amount.isnumeric() == False:
        view.not_dollar()
        amount = view.send_money_amount()
    
    while float(amount) >= account_num.checking:
        view.insufficient_funds()
        amount = view.send_money_amount()
        
    amount = float(amount)

    #change checking account balance in class and return new balance
    new_balance = model.Account.send_money(account_num, amount)
    #save new balance 
    model.Account.save_send_money(account_num, receiver, amount)

    #show new balance
    view.sent(new_balance, receiver, amount)
    return

run()