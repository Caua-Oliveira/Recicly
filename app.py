from flask import Flask, jsonify, request
from user import fetch_user_by_email

app = Flask(__name__)


@app.route('/user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    user = fetch_user_by_email(email)
    if user:
        print(user.password)
        user_data = {
            'name': user.name,
            'email': user.email,
            'password': str(user.password),
            'cpf': user.cpf,
            'is_active': bool(user.is_active)
        }

        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
