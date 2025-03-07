import sqlite3
import bcrypt


# connects to database
def get_db_connection():
    conn = sqlite3.connect('../customers.db')
    conn.row_factory = sqlite3.Row # accesses rows by column name
    return conn


def hash_value(plain_value):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_value.encode('utf-8'), salt)
    return hashed


email = input("Enter admin email: ")
password = input("Enter admin password: ")

hashed_email = hash_value(email)
hashed_password = hash_value(password)

print("Creating admin account")

# connect to database
conn = get_db_connection()

# add information to database
conn.execute('''
    INSERT INTO customers (email, password)
    VALUES (?, ?);
''', (hashed_email, hashed_password))

print(f"Hashed email: {hashed_email}")
print(f"Hashed password: {hashed_password}")

if bcrypt.checkpw(email.encode('utf-8'), hashed_email):
    print("Hash is correct")



print("Account creation successful")

conn.commit()
conn.close()