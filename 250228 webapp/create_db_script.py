import csv
import sqlite3


def create_table():

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS products_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    desc TEXT NOT NULL,
                    cost TEXT NOT NULL,
                    category TEXT NOT NULL);
                    ''')

    with open('resources/product_data.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # skip header row
        next(csv_reader)

        # insert each row into table SECURELY (why is it secure?)

        for row in csv_reader:
            cursor.execute('''
                INSERT INTO products_table (name, desc, cost, category)
                values (?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3]))

    conn.commit()
    conn.close()
