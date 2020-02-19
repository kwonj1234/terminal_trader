from flask import Flask, render_template, request, redirect, session, jsonify
from app.accounts import Account
from app.positions import Positions
from app.trades import Trades
from app.util import hash_password, get_price
import random
import string
import os

app = Flask(__name__)
app.secret_key = '34fewth54r454fh522345676jyhrvsbtj6hfd98doicnl'

@app.route('/homepage', methods = ["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template('homepage.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = Account.validate(username, password)
        print(user)
        if user is False:
            return render_template("homepage.html",
                                    message = "Username or Password is incorrect")
        else:
            session['username'] = username
            session['balance'] = user.balance
            session['fname'] = user.fname
            session['lname'] = user.lname
            session['pk'] = user.pk
            session['password'] = password
            session['salt'] = user.salt

            return redirect("/login_menu")

@app.route('/login_menu', methods = ['GET'])
def login_menu():
    if "username" in session:
        return render_template("login_menu.html")
    else:
        return redirect("/homepage")
        
@app.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    if request.method == "GET":
        return render_template('create_account.html')
    else:
        fname = request.form.get('fname')
        lname = request.form.get('lname')

        username = request.form.get('username')
        #get username, no repeats
        if Account.no_repeat_usernames(username) is False:
            return render_template('create_account.html',
                                    message = "Username already in use")
        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #get  password, password cannot be seen so make sure they typed it correctly
        if password1 != password2:
            return render_template('create_account.html',
                                    message = "Passwords do not match")
        #create a hashed salted password
        salt = str(os.urandom(64))
        hashpassword = hash_password(password1 + salt)
        #get initial deposit
        initial = request.form.get('deposit')
        #create account and save to database
        new_account = Account(None, fname, lname, username, hashpassword,
                        salt, initial)
        new_account.save()

        return redirect('/homepage')

if __name__=="__main__":
    app.run(debug=True)