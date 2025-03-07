import sqlite3

conn = sqlite3.connect('../customers.db')
cursor = conn.cursor()

while True:

    flag = True
    while flag:

        user_input = input("User ID to delete: ")

        if user_input == "quit":
            conn.close()

        try:
            user_input = int(user_input)
            flag = False
        except ValueError:
            print("Please enter an integer")

    cursor.execute("DELETE FROM customers WHERE id = ?", (user_input,))
    print(cursor.rowcount, "records deleted")

    conn.commit()