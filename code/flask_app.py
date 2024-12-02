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

# Routes for main navigation
@app.route('/')
def start():
    return render_template('home_page.html')

@app.route('/home')
def home_page():
    print(session.get('user_id'))
    if session.get('user_id') == '2':
        session['user_id'] = 'none'
    if session.get('user_id') == 'none':
        return render_template('home_page.html')
    return redirect(url_for('logged_home_page'))

@app.route('/home', methods=['POST'])
def home():
    return

@app.route('/sair')
def sair():
    session['user_id'] = 'none'
    return redirect(url_for('home_page'))

@app.route('/register')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email-signup']
    password = request.form['password-signup']

    # Create a new user
    new_user = User(name, email, password)
    if save_user_to_db(new_user):
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login_page'))
    else:
        flash("Erro ao cadastrar usuário. Tente novamente.", "error")
        return redirect(url_for('register_page'))

@app.route('/login')
def login_page():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Fetch user from database
    user = fetch_user_by_email(email)
    if user and user.verify_password(password):
        session['user_id'] = user.id  # Save user in session
        return redirect(url_for('logged_home_page', uid=user.id))
    else:
        flash("E-mail ou senha incorretos.", "error")
        return redirect(url_for('login_page'))

@app.route('/logged')
def logged_home_page():
    return render_template('logged_home_page.html')

@app.route('/logged', methods=['POST'])
def logged():
    return

@app.route('/rankings')
def rankings_page():
    ranking_data = [
        {
            'name': 'João Silva',
            'trash_amount': 45.5,  # in kilograms
            'points': 1250,
            'user_id': 1
        },
        {
            'name': 'Maria Santos',
            'trash_amount': 38.2,
            'points': 1100,
            'user_id': 2
        },
        {
            'name': 'Pedro Oliveira',
            'trash_amount': 52.7,
            'points': 1450,
            'user_id': 3
        },
        {
            'name': 'Ana Souza',
            'trash_amount': 29.6,
            'points': 850,
            'user_id': 4
        },
        {
            'name': 'Carlos Eduardo',
            'trash_amount': 61.3,
            'points': 1700,
            'user_id': 5
        }
    ]

    # Example of user_rank structure
    user_rank = {
        'name': 'Current User',
        'trash_amount': 35.8,
        'points': 1000,
        'position': 6,  # User's current ranking
        'user_id': 41
    }
    user_rank = {
        'name': 'Caua Oliveira',  # Assuming you have a username attribute
        'trash_amount': 35.8,
        'points': 1000,
        'position': 6,  # This would be calculated based on actual ranking
        'user_id': 41
    }
    return render_template('rankings_page.html',
                           ranking_data=ranking_data,
                           user_rank=user_rank)

@app.route('/rankings', methods=['POST'])
def rankings():
    return
@app.route('/profile')
def profile_page():
    user_obj = fetch_user_by_id(session.get('user_id'))
    user_stats = user_obj.to_dict()
    if user_obj:
        return render_template('profile_page.html', **user_stats)
    else:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('home_page'))

@app.route('/profile', methods=['POST'])
def profile():
    return

@app.route('/dashboard/<uid>')
def dashboard(uid):
    user = fetch_user_by_id(uid)
    if user:
        return f"<h1>Bem-vindo, {user.name}!</h1>"
    else:
        return "Usuário não encontrado.", 404

if __name__ == "__main__":
    app.run(debug=True)