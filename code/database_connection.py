import firebase_admin
from firebase_admin import credentials, db
import user
from user_statistics import *

# Initialize Firebase app (you'll need to replace 'path/to/serviceAccountKey.json' with your actual path)
cred = credentials.Certificate("reciclagem-d96e3-firebase-adminsdk-omcdz-0eeb40815c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reciclagem-d96e3-default-rtdb.firebaseio.com/'
})


def save_user_to_db(user):
    try:
        # Check if a user with the same CPF exists
        user_ref = db.reference('users').child(user.cpf)
        if user_ref.get() is not None:
            print(f"Error: User with CPF {user.cpf} already exists.")
            return False

        # Check if the email is already used by another user
        users_ref = db.reference('users').get()
        for key, user_data in users_ref.items():
            if user_data.get('email') == user.email:
                print(f"Error: Email {user.email} is already in use.")
                return False

        # If the user does not exist, save the new user
        user_ref.set({
            'name': user.name,
            'email': user.email,
            'password': user.password.decode('utf-8'),
            'is_active': user.is_active
        })
        return True
    except Exception as e:
        print(f"Error saving user to database: {e}")
        return False


def fetch_user_by_email(email):
    try:
        users_ref = db.reference('users')
        users = users_ref.get()
        for cpf, user_data in users.items():
            if user_data['email'] == email:
                stats_data = user_data.get('statistics', {})

                statistics = UserStatistics()
                statistics.total_trash_amount = stats_data.get('total_trash_amount', 0)
                statistics.trash_by_type = stats_data.get('trash_by_type', {
                    'plastic': 0,
                    'metal': 0,
                    'paper': 0,
                    'glass': 0,
                    'organic': 0
                })
                statistics.all_time_points = stats_data.get('all_time_points', 0)
                statistics.current_points = stats_data.get('current_points', 0)
                statistics.points_traded = stats_data.get('points_traded', 0)
                statistics.number_of_trades = stats_data.get('number_of_trades', 0)

                return user.User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'].encode('utf-8'),
                    cpf=cpf,
                    is_active=user_data['is_active'],
                    statistics=statistics
                )
        return None
    except Exception as e:
        print(f"Error fetching user from database: {e}")
        return None

def update_user_in_db(user):
    try:
        user_ref = db.reference(f'users/{user.cpf}')
        user_ref.update({
            'name': user.name,
            'email': user.email,
            'password': user.password.decode('utf-8'),
            'is_active': user.is_active,
            'statistics': user.statistics.to_dict(),  # Add statistics here
        })
        return True
    except Exception as e:
        print(f"Error updating user in database: {e}")
        return False

def delete_user_from_db(cpf):
    try:
        user_ref = db.reference(f'users/{cpf}')
        user_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting user from database: {e}")
        return False

def fetch_collection_location_by_login_id(login_id):
    try:
        locations_ref = db.reference('collection_locations')
        locations = locations_ref.get()
        for location_id, location_data in locations.items():
            if location_data['login_id'] == login_id:
                return location_data  # You might want to create a CollectionLocation class and return an instance
        return None
    except Exception as e:
        print(f"Error fetching collection location from database: {e}")
        return None