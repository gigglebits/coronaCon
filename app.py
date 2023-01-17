"""Application entry point."""
from flask import Flask, render_template, request, url_for, flash, session
import sys
sys.path.insert(0, './modules')
from account_management import *
#from forms import *
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import os

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = '_5#y2LF4Q8z*n*xec]/'
app.config['UPLOAD_FOLDER'] = './static/images/tmp/'

@login_manager.user_loader
def load_user(user_id):
    user = load_user_helper(user_id)
    return user

@app.route('/', methods=['GET','POST'])
@login_required
def hello_moto():
    return render_template("home.html", userName = current_user.userID)

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    #check for POST submition of form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("Username: " + username + " Password: " + password)

        user_object = login(username, password)
        print(user_object)
        if user_object != None:
            login_user(user_object)
            return render_template('home.html', userName = current_user.userID)
        else:
            flash('Invalid credentials please try again.') #this and the line above need to be tested one might work hopefully
            return render_template("login.html")
    return render_template("login.html")

"""
@app.route('/createAccount', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        action = registration(username, email,  password)
        #check here to see if the email and username has already been used by performing a query
        #if the above query is true flash the below message and direct back to the signup page using:
        #return redirect(url_for('app.createAccount'))
        #flash('Email address already exists')
        #create a new user with the form data and hash the password so the plaintext version isn't saved this is where we canc all the method in forms.py
        #add the new user to the database
        if action == 409:
            flash('Username already exists')
            return render_template('register.html')
        elif action == 410:
            flash('Email address already exists')
            return render_template("register.html")
        else:
            flash('Thank you for creating your account '+username)
            return render_template("login.html")
    return render_template("register.html")

"""

@app.errorhandler(500)
def pageNotFound(error):
    flash('Please login or create an account first')
    return render_template("login.html")