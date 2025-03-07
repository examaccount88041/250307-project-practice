import sqlite3

def get_db_connection():
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully")
    conn.row_factory = sqlite3.Row # accesses rows by column name
    return conn

# main script

email = "admin"
phone = "06723490856230"


with get_db_connection() as conn:
    # check if phone and email already exists
    email_exists = conn.execute('SELECT EXISTS(SELECT 1 FROM customers WHERE email = ?);', (email,)).fetchone()[0]
    phone_exists = conn.execute('SELECT EXISTS(SELECT 1 FROM customers WHERE phone_number = ?);', (phone,)).fetchone()[0]

    # if email is already in database
    if email_exists or phone_exists:
        print("Email or phone number is already associated with an account.")
        # return template login or something
    else:
        print("Creating new customer")
        # add new info to db


