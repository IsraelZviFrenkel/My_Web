@app.route('/register', methods=['GRT'], '[POST')
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
            retuen
            redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash("Username already exist!", "danger")
    return render_template('register.html')
