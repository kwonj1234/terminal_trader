import json
import hashlib
import requests #import requests library from python so that you can communicate with API's

SALT = "drg64st6hbs6g4a1".encode()

def hash_password(password):

    hashed_pw = hashlib.sha512(password.encode() + SALT).hexdigest()

    return hashed_pw

def get_price(ticker):
    # get price from IEX Cloud API
    with open("app/token.json", 'r') as json_file:
        tokens = json.load(json_file)
        token = tokens["publishable"]

    response = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={token}')
    data = response.json()
    
    return data["latestPrice"]
