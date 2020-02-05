from getpass import getpass

def main_menu():
    print()
    print("Welcome to Terminal Trader\n")
    print("What would you like to do today")
    print("1) Create Account")
    print("2) Log in")
    print("3) Quit")
    return input()

#Create Account
def create_account():
    print("\nThank you for choosing to open an account with Herkshire Bathaway!")

def first_name():
    print("Please enter your first name: ")
    return input()

def last_name():
    print("\nPlease enter your last name: ")
    return input()

def new_username():
    print("\nPlease create a username: ")
    return input()

def create_password():
    password1 = getpass("\nPlease enter a password")
    password2 = getpass("\nPlease re-enter your password")
    return password1, password2

def initial_deposit():
    return input("\nHow much would you like to deposit?\n")

def new_account():
    print("\nThank you for opening an accout with Herkshire Bathaway!")

#Login
def login():
    print("\nPlease enter your Username and Password")
    return (input("\nUsername: "), getpass("Password: "))

def welcome(fname, lname):
    print(f'\nHello {fname} {lname}')

def login_menu():
    print('\nWhat would you like to do today?')
    print('1) Check Balance')
    print('2) Deposit')
    print('3) Purchase shares')
    print('4) Sell shares')
    print('5) Current Positions')
    print('6) Transaction History')
    print('7) Check Current Price of Stock')
    print('8) Sign Out')
    return input()

#1) Check Balance
def check_balance(balance):
    print(f"\nYour current balance is $" + "{:.2f}".format(balance))

#2) Deposit
def deposit():
    return input("\nHow much would you like to deposit into your account?\n")

def new_balance(new_balance):
    print("\nYour new account balance is $" + "{:.2f}".format(new_balance))

#3) purchase shares
def buy_stock():
    return input("\nWhat stock would you like to purchase shares from?\n(Input the ticker)\n")

def buy_shares():
    return input("\nHow many shares would you like to purchase?\n(1 = 100 shares)\n")

def confirm_buy(ticker, shares, price, mv):
    print(f"\nConfirm buy order of {shares} shares of {ticker} at ${price} per share")
    print("Market value of $" + "{:.2f}".format(mv))
    print("[y/n]")
    return input()

def display_buy(ticker, shares, price, new_balance):
    print(f"\nSuccesfully bought {shares} shares of {ticker} at ${price} per share")
    print("Your new balance is $" + "{:.2f}".format(new_balance))

#4) sell shares
def sell_stock():
    return input("\nWhat stock would you like to sell shares from?\n(Input the ticker)\n")

def sell_shares():
    return input("\nHow many shares would you like to sell?\n(1 = 100 shares)\n")

def confirm_sell(ticker, shares, price, mv):
    print(f"\nConfirm sell order of {shares} shares of {ticker} at ${price} per share")
    print("Market value of $" + "{:.2f}".format(mv))
    print("[y/n]")
    return input()

def display_sell(ticker, shares, price, new_balance):
    print(f"\nSuccesfully sold {shares} shares of {ticker} at ${price} per share")
    print("Your new balance is $" + "{:.2f}".format(new_balance))

#Signing Out
def signout():
    print('\nThank you for visiting Herkshire Bathaway\n')

#Bad input responses
def pass_dont_match():
    print("\nPasswords do not match")

def bad_login():
    print("Invalid Username or Password")

def repeat_username():
    print("\nUsername is already in use")
    print("Please choose another username")

def insufficient_funds():
    print("Insufficient funds")

def not_ticker():
    print("Please input a ticker")

def incorrect_ticker():
    print("Ticker was inputted incorrectly")

def bad_input():
    print("Invalid Input")

def not_dollar():
    print("Please enter a dollar value")

def no_positions(ticker):
    print(f"You do not have any shares of {ticker}")

def insufficient_shares(ticker):
    print(f"Insufficient shares of {ticker}")
