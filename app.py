from flask import Flask, render_template, redirect, url_for, request, session , jsonify
import sqlite3
import os
import time , os
from coinbasepayment import create_payment


app = Flask(__name__)
app.secret_key = 'srfxdz'

def getchecksum():
    time.sleep(0)



def clear():
    os.system('cls')


@app.route('/')
def home():
    return redirect(url_for('login'))

def connect_to_db(db_name="user_data.db"):
    """Connects to the SQLite database or creates a new one if it doesn't exist."""
    is_new_db = not os.path.exists(db_name)
    conn = sqlite3.connect(db_name)
    if is_new_db:
        print(f"Database '{db_name}' created successfully!")
    else:
        print(f"Connected to existing database '{db_name}'.")
    return conn

def create_table():
    """Creates the users table if it doesn't exist."""
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Create the table at application startup
create_table()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate user
        with connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json  # Parse the JSON data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required.'}), 400

        try:
            # Add user to the database
            with connect_to_db() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            
            # Replace the following with your payment creation function, if applicable
            url = '/login'  # Redirect URL after registration
            return jsonify({'url': url}), 200
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard view, accessible only to logged-in users."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/catalog/<int:catalog_id>')
def catalog(catalog_id):
    """Catalog view, accessible only to logged-in users."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template(f'catalog{catalog_id}.html', username=session['username'])

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
