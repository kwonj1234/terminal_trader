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
    print('1) Investments Summary')
    print('2) Purchase shares')
    print('3) Sell shares')
    print('4) Transaction History')
    print('5) Sign Out')
    return input()

#Summary


#Withdraw funds
def withdraw():
    print('\nHow much would you like to withdraw?')
    print('1) $10')
    print('2) $20')
    print('3) $50')
    print('4) $100')
    print('5) Enter Custom Amount')
    return input()

def withdraw_custom():
    print('\nEnter Custom Amount')
    return input()

def withdraw_new_balance(num, new_balance):
    print('\nYou withdrew : $' + "{:.2f}".format(num))
    print('Your new Checking Account balance is : $' + "{:.2f}".format(new_balance))

#Deposit into your account
def deposit():
    print('\nHow much would you like to deposit?')
    return input()

def deposit_new_balance(num, new_balance):
    print('\nYou deposited : $' + "{:.2f}".format(num))
    print('Your Checking Account balance is : $' + "{:.2f}".format(new_balance))

#Transfer money from one account to the other
def transfer_from_account():
    from_account = input('\nWhich account would you like to transfer funds from?\n')
    return from_account

def transfer_to_account():
    to_account = input('\nWhich account would you like to transfer funds to?\n')
    return to_account

def transfer_amount():
    amount = input('\nHow much would you like to transfer?\n')
    return amount

def transfer_new_balance(from_balance, to_balance, from_account, to_account):
    print('\nYour new account balance is')
    print(f'{from_account} : $' + "{:.2f}".format(from_balance))
    print(f'{to_account} : $' + "{:.2f}".format(to_balance))

#Send money to another account
def send_money_account():
    print('\nEnter the account number of the account you want to send money to')
    return input()

def send_money_amount():
    print('\nEnter the amount you want to send')
    return input()

def sent(new_balance, receiver, amount):
    print('\nYou sent $' + "{:.2f}".format(amount) + f" to account number {receiver}")
    print('Your new checking account balance is $' + "{:.2f}".format(new_balance))
    
#Signing Out
def signout():
    print('\nThank you for visiting Herkshire Bathaway\n')

#Bad input responses
def pass_dont_match():
    print("\nPasswords do not match")

def bad_login():
    print("Invalid Username or Password")

def insufficient_funds():
    print("Insufficient funds")

def bad_input():
    print("Invalid Input")

def not_dollar():
    print("Please enter a dollar value")
