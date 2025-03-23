import sqlite3

def get_db_connection():
    conn = sqlite3.connect('customers.db')
    print("Opened database successfully")
    conn.row_factory = sqlite3.Row # accesses rows by column name
    return conn

# main script

email = "admin"

# connect to database
conn = get_db_connection()
cursor = conn.cursor()

#execute query
cursor.execute('SELECT EXISTS(SELECT 1 FROM customers WHERE email = ?);', (email,))
# fetch result
exists = cursor.fetchone()[0]
print(exists)
