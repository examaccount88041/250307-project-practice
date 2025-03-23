import csv
import sqlite3

def create_table():

    conn = sqlite3.connect('../customers.db')
    cursor = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    forename TEXT NULL,
                    surname TEXT NULL,
                    email TEXT NOT NULL,
                    address TEXT NULL,
                    city TEXT NULL,
                    postcode TEXT NULL,
                    phone_number TEXT NULL,
                    password TEXT NOT NULL
                )''')

    with open('../resources/customers.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # skip header row
        next(csv_reader)

        # insert each row into table
        for row in csv_reader:
            cursor.execute('''
                            INSERT INTO customers (forename, surname, email, address, city, postcode, phone_number, password)
                            values (?,?,?,?,?,?,?,?)
                            ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    conn.commit()
    conn.close()

    print("successful")

create_table()