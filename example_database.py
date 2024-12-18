import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to interact with the database
cur = conn.cursor()

# Create a table
cur.execute('''CREATE TABLE IF NOT EXISTS users2 (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL)''')

# Insert data into the table
cur.execute("INSERT INTO users2 (name, age) VALUES (?, ?)", ('Alice', 30))
cur.execute("INSERT INTO users2 (name, age) VALUES (?, ?)", ('Bob', 25))

# Commit the changes
conn.commit()

# Query data from the table
cur.execute("SELECT * FROM users2")
rows = cur.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()



