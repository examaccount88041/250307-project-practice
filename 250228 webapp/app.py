from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import secrets
import bcrypt

app = Flask(__name__)

# create secret key
secretkey = secrets.token_hex(16)
app.secret_key = secretkey

# connects to database
def get_db_connection():
    conn = sqlite3.connect('customers.db')
    conn.row_factory = sqlite3.Row # accesses rows by column name
    return conn

# function to hash data
def hash_value(plain_value):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_value.encode('utf-8'), salt)
    return hashed

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def loginpage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    # connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # check if the email exists in database
    cursor.execute('SELECT * FROM customers WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user:
        # get the stored hashed passwords from the database
        stored_hash = user['password']

        # compare entered password with stored hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            # passwords match
            session['user_id'] = user['id']
            print("Successfully logged in!")
            conn.close()
            return redirect(url_for('home'))
        else:
            # if passwords do not match
            flash('Invalid credentials')
            print('Invalid password')
            conn.close()
            return redirect(url_for('login'))

    else: # if the email or passwords do not match
        flash("Invalid credentials")
        print("invalid email")
        print(user)
        conn.close()
        return redirect(url_for('login'))


@app.route('/register',methods=['GET'])
def registerpage():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():


    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    email = request.form.get('email', None)
    address = request.form.get('address', None)
    city = request.form.get('city', None)
    postcode = request.form.get('postcode', None)
    phone = request.form.get('phone', None)
    password = request.form.get('password', None)

    # hashes necessary data
    password = hash_value(password)



    # check if phone and email already exists
    with get_db_connection() as conn:
        email_exists = \
        conn.execute('SELECT EXISTS(SELECT 1 FROM customers WHERE email = ?);', (email,)).fetchone()[0]
        phone_exists = \
        conn.execute('SELECT EXISTS(SELECT 1 FROM customers WHERE phone_number = ?);', (phone,)).fetchone()[0]


    # if email or phone is already in database
    if email_exists or phone_exists:
        print("Email or phone number is already associated with an account.")
        return redirect(url_for('register'))

    else:
        print("Creating new customer")

        # connect to database
        conn = get_db_connection()
        # add information to database
        conn.execute('''
            INSERT INTO customers (forename, surname, email, address, city, postcode, phone_number, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        ''', (first_name, last_name, email, address, city, postcode, phone, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

"so we just sit in "
