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

cursor.execute('''
    INSERT INTO listings (title, description, price, location)
    VALUES ('Cozy Apartment', 'A beautiful apartment in the heart of the city.', 100.0, 'City Center'),
           ('Spacious Villa', 'A luxurious villa with a stunning view.', 250.0, 'Mountain Resort'),
           ('Beach House', 'A charming beach house just steps away from the ocean.', 150.0, 'Beachside')
''')

connection.commit()
connection.close()
