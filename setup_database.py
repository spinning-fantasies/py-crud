import sqlite3

def create_table():
    connection = sqlite3.connect('listings.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            location TEXT NOT NULL,
            image TEXT,
            deleted INTEGER DEFAULT 0
        )
    ''')

    # Insert sample data
    cursor.executemany('''
        INSERT INTO listings (title, description, price, location, image)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('Cozy Apartment', 'A beautiful apartment in the heart of the city.', 100.0, 'City Center', '/static/uploads/apartment.jpg'),
        ('Spacious Villa', 'A luxurious villa with a stunning view.', 250.0, 'Mountain Resort', '/static/uploads/villa.jpg'),
        ('Beach House', 'A charming beach house just steps away from the ocean.', 150.0, 'Beachside', '/static/uploads/beach_house.jpg')
    ])

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_table()
