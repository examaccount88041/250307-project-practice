import sqlite3
import bcrypt

column_name = input("Enter name of column bitch: ")

# function to hash
def hash_value(plain_value):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_value.encode('utf-8'), salt)
    return hashed

# connect to database
conn = sqlite3.connect('../customers.db')
cursor = conn.cursor()

# retrieve rows with selected column
cursor.execute(f'SELECT id, {column_name} FROM customers')
rows = cursor.fetchall()

# loop through rows and hash specified column
for row in rows:
    user_id = row[0]
    print(f"User ID: {user_id}")
    plain_value = row[1]
    print(f"Plain Value: {plain_value}")

    # hash selected column value
    hashed_value = hash_value(plain_value)
    print(f"Hashed Value: {hashed_value}")

    # update database
    cursor.execute(f'UPDATE customers set {column_name}=?', (hashed_value,))

conn.commit()
conn.close()