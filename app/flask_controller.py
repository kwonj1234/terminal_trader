from flask import Flask, render_template, request, redirect, session, jsonify
from accounts import Account
from positions import Positions
from trades import Trades
from util import hash_password, get_price
import random
import string
import os

app = Flask(__name__)
app.secret_key('dcvfbyh65ervtynuj890oiuyntbtvrefwd21qwasce4356789oiuytredcsfgbhnyhg4f323456789iuytrecasdfgbnm')

@app.route('/homepage', methods = ["GET", "POST"])
def homepage():
    if request.method == "GET":
        return render_template('homepage.html')
    else:
        username = request.form.get['username']
        password = request.form.get['password']

        user = Account.validate(username, password)

        if user:
            return redirect("/login_menu")
        else:
            return render_template("login.html",
                                    message = "Username or Password is incorrect")

@app.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    if request.method == "GET":
        return render_template('create_account.html')
    else:
        fname = request.form.get['fname']
        lname = request.form.get['lname']

        username = request.form.get['username']
        #get username, no repeats
        if Account.no_repeat_usernames(username) is False:
            return render_template('create_account.html',
                                    message = "Username already in use")
        
        password1 = request.form['password1']
        password2 = request.form['password2']
        #get  password, password cannot be seen so make sure they typed it correctly
        if password1 != password2:
            return render_template('create_account.html',
                                    message = "Passwords do not match")
        #create a hashed salted password
        salt = str(os.urandom(64))
        hashpassword = hash_password(password1 + salt)
        #get initial deposit
        initial = request.form['deposit']
        #create account and save to database
        new_account = Account(None, fname, lname, username, hashpassword,
                        salt, initial)
        new_account.save()

        return render_template('homepage.html', message = "Account successfully created")

# @app.route('/login_menu', methods = ['GET', 'POST'])
# def login_menu():


if __name__=="__main__":
    app.run(debug=True)