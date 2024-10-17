import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database setup
DATABASE = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows us to treat rows like dicts
    return conn


# Initialize database with a users table
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Route to display users and form to add new user
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Insert user data into database
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        return redirect(url_for('index'))

    # Fetch all users from the database
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return render_template('index.html', users=users)


# Route to delete a user
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
