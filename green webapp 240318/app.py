import secrets
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)


# cookie security
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

app.config['SESSION_COOKIE_SECURE'] = True      # Send cookies over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True    # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # CSRF protection


# connects to database
def get_database_connection():

    # use app.instance_path to make path to database folder (very secure probably)
    db_path = os.path.join(app.instance_path, 'customers.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # accesses rows by column name
    return conn

    #   how to use:
    #     conn = get_database_connection()
    #     cursor = conn.cursor()
    #     cursor.execute('SELECT * FROM customers') <- query goes here


# landing page
@app.route('/')
def index():
    return redirect(url_for('home'))


# home page
@app.route('/home')
def home():
    return render_template('home.html')


# login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# login logic
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    # connect to database
    conn = get_database_connection()
    cursor = conn.cursor()

    # check if the email exists in database
    cursor.execute('SELECT * FROM customers WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user and user['password'] == password:  # directly compare passwords
        session['user_id'] = user['id']  # store user id in session
        print("Successful login!")
        conn.close()
        return redirect(url_for('home'))  # redirects after successful login

    else:  # if the email or passwords do not match
        flash("Invalid credentials")
        print("invalid credentials")
        conn.close()
        return redirect(url_for('login'))  # redirect to login page

# logout button
@app.route('/logout')
def logout():
    session.pop('username', None)  # remove cookie
    return redirect(url_for('login'))


app.run()