from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from code.user import User
from code.database_connection import *
from code.main import view_ranking, fetch_site_statistics, display_recycling_locations, fetch_all_stores_from_db, buy_coupon2

# Flask app with custom templates and static paths
app = Flask(
    __name__,
    template_folder="../templates",  # Adjust path for templates
    static_folder="../static"        # Adjust path for static files
)
app.secret_key = "secret_key"

# ------------------------------
# Helper Functions
# ------------------------------
def is_logged_in():
    """Check if a user is logged in."""
    return session.get('user_id') is not None

# ------------------------------
# Routes
# ------------------------------

# Home and Navigation
@app.route('/')
def start():
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    logged = is_logged_in()
    return render_template('home_page.html', logged=logged)

@app.route('/sair')
def sair():
    session.pop('user_id', None)
    return redirect(url_for('home_page'))

# User Authentication
@app.route('/register')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email-signup']
    password = request.form['password-signup']

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

    user = fetch_user_by_email(email)
    if user and user.verify_password(password):
        session['user_id'] = user.id
        return redirect(url_for('home_page'))
    else:
        flash("E-mail ou senha incorretos.", "error")
        return redirect(url_for('login_page'))

# Rankings
@app.route('/rankings')
def rankings_page():
    logged = is_logged_in()
    user_id = session.get('user_id', '0')
    ranking_data, user_rank = view_ranking(user_id)

    return render_template(
        'rankings_page.html',
        ranking_data=ranking_data,
        user_rank=user_rank,
        logged=logged
    )

# Recycling Locations
@app.route('/places')
def places_page():
    locations = display_recycling_locations()
    return render_template('places_page.html', locations_with_distances=locations)

# Stores and Coupons
@app.route('/stores')
def stores_page():
    logged = is_logged_in()
    stores = fetch_all_stores_from_db()
    return render_template('stores_page.html', stores=stores, logged=logged)

@app.route('/buy_coupon', methods=['POST'])
def buy_coupon():
    data = request.json
    store_name = data.get('store_name')
    selected_coupon = data.get('selected_coupon')
    user_id = session.get('user_id')

    success, code = buy_coupon2(store_name, selected_coupon, user_id)
    if success:
        return jsonify({'message': f'Cupom resgatado com sucesso!\nCode: {code}'}), 200
    else:
        return jsonify({'message': 'Falha ao resgatar o cupom.'}), 400

# Profile
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    user_obj = fetch_user_by_id(user_id)
    if user_obj:
        user_stats = user_obj.to_dict()
        return render_template('profile_page.html', **user_stats)
    else:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('home_page'))

# Site Statistics
@app.route('/sitestats')
def sitestats_page():
    logged = is_logged_in()
    stats = fetch_site_statistics()
    return render_template('sitestats_page.html', statistics=stats, logged=logged)


if __name__ == "__main__":
    app.run()
