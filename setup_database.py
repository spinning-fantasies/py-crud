import sqlite3

connection = sqlite3.connect('listings.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        location TEXT NOT NULL,
        deleted INTEGER DEFAULT 0
    )
''')

connection.commit()
connection.close()
