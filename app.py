import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATABASE = 'listings.db'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


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

        # Handle image upload
        image_url = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'/static/uploads/{filename}'  # Store the image URL in the database

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO listings (title, description, price, location, image) VALUES (?, ?, ?, ?, ?)',
                       (title, description, price, location, image_url))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    return render_template('create_listing.html')


@app.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
def edit_listing(listing_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM listings WHERE id = ?', (listing_id,))
    listing = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        location = request.form['location']

        # Handle image upload
        image_url = listing['image']
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'/static/uploads/{filename}'  # Store the updated image URL in the database

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('UPDATE listings SET title = ?, description = ?, price = ?, location = ?, image = ? WHERE id = ?',
                       (title, description, price, location, image_url, listing_id))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

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
    if not os.path.exists(DATABASE):
        with app.app_context():
            from setup_database import create_table

            create_table()

    app.run(debug=True)
