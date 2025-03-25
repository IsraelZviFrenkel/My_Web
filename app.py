from flask import Flask, render_template, request, flash, url_for, redirect, session
from functools import wraps

import sqlite3

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "my_secret_key"
db_local = 'student.db'

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("You must be logged in to access this page", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/home')
@login_required
def home_page():
    student_data = query_contact_details()
    return render_template('home.html', student_data=student_data)


def query_contact_details():
    connie = sqlite3.connect(db_local)
    c = connie.cursor()
    c.execute("""
    SELECT * FROM contact_details
    """)
    student_data = c.fetchall()
    return student_data


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        student_details = (
            request.form['firstname'],
            request.form['lastname'],
            request.form['street_address'],
            request.form['city']
        )
        insert_student(student_details)
        return render_template('add_success.html')


def insert_student(student_details):
    connie = sqlite3.connect(db_local)
    c = connie.cursor()
    sql_execute_string = 'INSERT INTO contact_details (firstname, lastname, street_address, city) VALUES (?, ?, ?, ?)'
    c.execute(sql_execute_string, student_details)
    connie.commit()
    connie.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            flash("User registered successfully!", "success")
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash("Username already exist!", "danger")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('home_page'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f"<h2>Welcome, {session['user']}!</h2> <a href='/logout'</a>"


@app.route('/logout')
def logout():
    # Remove the user from the session
    session.pop('user', None)

    # Clear all session data
    session.clear()

    # Clear the session cookie
    response = redirect(url_for('login'))
    response.set_cookie('session', '', expires=0)  # Clear the session cookie

    # Flash a logout success message
    flash("Logged out successfully!", "success")

    return response


if __name__ == '__main__':
    app.run()
