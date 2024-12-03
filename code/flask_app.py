from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User
from database_connection import *
from main import view_ranking, fetch_site_statistics, display_recycling_locations, fetch_all_stores_from_db, buy_coupon2


# Flask app with custom templates and static paths
app = Flask(
    __name__,
    template_folder="../templates",  # Adjust path for templates
    static_folder="../static"        # Adjust path for static files
)
app.secret_key = "secret_key"

# Routes for main navigation
@app.route('/')
def start():
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    logged = False
    if session.get('user_id') is not None:
        logged = True
    return render_template('home_page.html', logged=logged)

@app.route('/home', methods=['POST'])
def home():
    return

@app.route('/sair')
def sair():
    session.pop('user_id', None)
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
        return redirect(url_for('home_page', uid=user.id))
    else:
        flash("E-mail ou senha incorretos.", "error")
        return redirect(url_for('login_page'))

@app.route('/rankings')
def rankings_page():
    logged = False
    if session.get('user_id') is not None:
        logged = True
        user_obj = fetch_user_by_id(session['user_id'])
        ranking_data, user_rank = view_ranking(user_obj.id)
    else:
        ranking_data, user_rank = view_ranking('0')

    return render_template('rankings_page.html',
                            ranking_data=ranking_data,
                            user_rank=user_rank,
                            logged=logged)


@app.route('/rankings', methods=['POST'])
def rankings():
    return

@app.route('/places')
def places_page():
    display_recycling_locations()
    return render_template('places_page.html', locations_with_distances=display_recycling_locations())

@app.route('/places', methods=['POST'])
def places():
    return

@app.route('/stores')
def stores_page():
    logged = True
    stores = fetch_all_stores_from_db()
    return render_template('stores_page.html', stores=stores, logged=logged)

@app.route('/stores', methods=['POST'])
def stores():
    return

@app.route('/profile')
def profile_page():
    user_obj = fetch_user_by_id(session.get('user_id'))
    if user_obj:
        user_stats = user_obj.to_dict()
        return render_template('profile_page.html', **user_stats)
    else:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('home_page'))

@app.route('/profile', methods=['POST'])
def profile():
    return

@app.route('/sitestats')
def sitestats_page():
    logged = True
    stats = fetch_site_statistics()
    return render_template('sitestats_page.html', statistics=stats, logged=logged)
@app.route('/sitestats', methods=['POST'])
def sitestats():
    return

@app.route('/buy_coupon')
def buyCoupon(store_name, selected_coupon):
    b = buy_coupon2(store_name, selected_coupon, session.get('user_id'))
    if b:
        flash("Cupom resgatado com sucesso!", "success")
    else:
        flash("Falha ao resgatar o cupom.", "error")
    return


if __name__ == "__main__":
    app.run(debug=True)