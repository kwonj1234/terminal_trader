from getpass import getpass

def main_menu():
    print()
    print("Welcome to Terminal Trader\n")
    print("What would you like to do today")
    print("1) Create Account")
    print("2) Log in")
    print("3) Quit")
    return input("> ")

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
def input_credentials():
    print("\nPlease enter your Username and Password")
    return (input("\nUsername: "), getpass("Password: "))

def welcome(fname, lname):
    print(f'\nHello {fname} {lname}')

def login_menu():
    print('\nWhat would you like to do today?')
    print('1) Check Balance')
    print('2) Deposit')
    print('3) Withdraw')
    print('4) Purchase lots')
    print('5) Sell lots')
    print('6) Current Positions')
    print('7) Transaction History')
    print('8) Check Current Price of Stock')
    print('9) Edit Account')
    print('10) Sign Out')
    return input("> ")

#1) Check Balance
def check_balance(balance):
    print(f"\nYour current balance is $" + "{:.2f}".format(balance))

#2) Deposit
def deposit():
    return input("\nHow much would you like to deposit into your account?\n>$")

def new_balance(new_balance):
    print("\nYour new account balance is $" + "{:.2f}".format(new_balance))

#3) Withdraw
def withdraw():
    return input("\n How much would you like to withdraw from your account?\n>$")

#4) purchase shares
def buy_stock():
    return input("\nWhat stock would you like to purchase lots from?\n(Input the ticker)\n> ")

def buy_lots():
    return input("\nHow many lots would you like to purchase?\n(1 lot = 100 shares)\n> ")

def confirm_buy(ticker, lots, price, mv, current_balance):
    print(f"\nConfirm buy order of {lots} lots of {ticker} at ${price} per share")
    print("Market value of $" + "{:.2f}".format(mv))
    print("Current Balance of $" + "{:.2f}".format(current_balance))
    print("[y/n]")
    return input("> ")

def display_buy(ticker, lots, price, new_balance):
    print(f"\nSuccesfully bought {lots} lots of {ticker} at ${price} per share")
    print("Your new balance is $" + "{:.2f}".format(new_balance))

#5) sell shares
def sell_stock():
    return input("\nWhat stock would you like to sell lots from?\n(Input the ticker)\n> ")

def sell_lots():
    return input("\nHow many lots would you like to sell?\n(1 lot = 100 shares)\n> ")

def confirm_sell(ticker, lots, price, mv, current_balance):
    print(f"\nConfirm sell order of {lots} lots of {ticker} at ${price} per share")
    print("Market value of $" + "{:.2f}".format(mv))
    print("Current Balance of $" + "{:.2f}".format(current_balance))
    print("[y/n]")
    return input("> ")

def display_sell(ticker, lots, price, new_balance):
    print(f"\nSuccesfully sold {lots} lots of {ticker} at ${price} per share")
    print("Your new balance is $" + "{:.2f}".format(new_balance))

#6) display positions
def display_position(ticker, lots, current_price, mv, profitorloss):
    print(f"\n{ticker} : {lots} lots")
    print(f"Market Value : ${mv}, Current Price : ${current_price}")
    if profitorloss < 0:
        print("Loss : ${0:.2f}\n".format(abs(profitorloss)))
    elif profitorloss > 0:
        print("Profit : ${0:.2f}\n".format(profitorloss))
    else:
        print("No gains or loss")
#7) display transactions
def display_header():
    print("\nTime Stamp          Ticker  Volume   Price        Market Value")

def display_transactions(ticker, lots, price, mv, time):
    print(f"{time} : {ticker},    {lots},    ${price},    ${mv}")

#8) Get a quote, see current price
def which_stock():
    print("\nWhich stock would you like to see the current price of?")
    print("(Input the ticker)")
    return input("> ")
    
def display_price(ticker, current_price):
    print(f"\n{ticker} : ${current_price}")

#9) Edit Account
def edit_account_menu():
    print("\n1) Change username")
    print("2) Change password")
    print("3) Cancel")
    return input("> ")

def change_username():
    return input("Enter new username: ")

def no_change():
    print("Why did you click change if you weren't going to change anything? Idiot, try again")

def change_password():
    return getpass("Enter new password: "), getpass("Enter password again: ")

#10) Signing Out
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
