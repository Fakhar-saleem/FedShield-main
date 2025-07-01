import sqlite3

# Connect to the SQLite database (or create a new one if it doesn't exist)



def search_user_by_name(val,no):
    if val=="1":
        table_name="Admins"
    else:
        table_name="Users"
    try:
        number = no
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Execute the SQL query to search for a user by name
        if '"' in no or "'" in no:
            number = no.replace('"', '').replace("'", '')

        cursor.execute(f"SELECT * FROM {table_name} WHERE PAno={number}")
        # Fetch the result
        result = cursor.fetchone()
        if result:
            cursor.close()
            conn.close()
            return result
        else:
            print("User not found.")
            cursor.close()
            conn.close()
            return 0

    except sqlite3.Error as e:
        cursor.close()
        conn.close()
        print("SQLite error:", e)
