from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
from database_connection import *

import os

# Flask app with custom templates and static paths
app = Flask(
    __name__,
    template_folder="../templates",  # Adjust path for templates
    static_folder="../static"        # Adjust path for static files
)
app.secret_key = "your_secret_key"

@app.route('/')
def home():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Fetch user from database
    user = fetch_user_by_email(email)
    if user and user.verify_password(password):
        session['user_id'] = user.id  # Save user in session
        flash("Login bem-sucedido!", "success")
        return redirect(url_for('dashboard', uid=user.id))
    else:
        flash("Email ou senha incorretos. Tente novamente.", "error")
        return redirect(url_for('home'))

@app.route('/dashboard/<uid>')
def dashboard(uid):
    user = fetch_user_by_id(uid)
    return f"<h1>Bem-vindo, {user.name}!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
