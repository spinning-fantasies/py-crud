from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'listings.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM listings WHERE deleted = 0')
    listings = cursor.fetchall()
    connection.close()
    return render_template('index.html', listings=listings)

@app.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        location = request.form['location']

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO listings (title, description, price, location) VALUES (?, ?, ?, ?)',
                       (title, description, price, location))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('create_listing.html')

@app.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
def edit_listing(listing_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        location = request.form['location']

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('UPDATE listings SET title = ?, description = ?, price = ?, location = ? WHERE id = ?',
                       (title, description, price, location, listing_id))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))
    else:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM listings WHERE id = ?', (listing_id,))
        listing = cursor.fetchone()
        connection.close()

        return render_template('edit_listing.html', listing=listing)

@app.route('/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('UPDATE listings SET deleted = 1 WHERE id = ?', (listing_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
