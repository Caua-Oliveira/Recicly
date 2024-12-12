import firebase_admin
from firebase_admin import credentials, db
import code.user
from code.user_statistics import *
from code.store import Store
from code.coupon import Coupon
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
firebase_cert_path = os.path.join(base_dir, "firebase_recicly_example.json")
cred = credentials.Certificate(firebase_cert_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reciclagem-d96e3-default-rtdb.firebaseio.com/'
})


def save_user_to_db(user):
    try:
        # Reference to the counter node for unique IDs
        counter_ref = db.reference('counter')

        # Get the current counter value or initialize it if it doesn't exist
        current_id = counter_ref.get()
        if current_id is None:
            current_id = 0

        # Increment the counter
        new_id = current_id + 1
        counter_ref.set(new_id)  # Save the updated counter value

        # Reference for the new user using the unique ID
        user_ref = db.reference('users').child(str(new_id))

        # Check if the email is already used by another user
        users_ref = db.reference('users').get()
        if users_ref:
            for key, user_data in users_ref.items():
                if user_data.get('email') == user.email:
                    print(f"Error: Email {user.email} is already in use.")
                    return False

        # If the email is unique, save the new user
        user_ref.set({
            'id': new_id,
            'name': user.name,
            'email': user.email,
            'password': user.password.decode('utf-8'),
            'is_active': user.is_active
        })
        return True
    except Exception as e:
        print(f"Error saving user to database: {e}")
        return False
def fetch_all_users_from_db():
    try:
        users_ref = db.reference('users')
        users_data = users_ref.get()
        users = []
        for id, user_data in users_data.items():
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

            user_obj = code.user.User(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'].encode('utf-8'),
                id=id,
                is_active=user_data['is_active'],
                statistics=statistics
            )
            users.append(user_obj)
        return users
    except Exception as e:
        print(f"Error fetching users from database: {e}")
        return []

def fetch_user_by_email(email):
    try:

        users_ref = db.reference('users')
        users = users_ref.get()

        for id, user_data in users.items():
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

                return code.user.User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'].encode('utf-8'),
                    id=id,
                    is_active=user_data['is_active'],
                    statistics=statistics
                )
        return None
    except Exception as e:
        print(f"Error fetching user from database: {e}")
        return None


def fetch_user_by_id(user_id):
    try:
        users_ref = db.reference('users')
        user_data = users_ref.child(user_id).get()

        if user_data:
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

            # Return a User object with the fetched data
            return code.user.User(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'].encode('utf-8'),
                id=user_id,
                is_active=user_data['is_active'],
                statistics=statistics
            )

        return None

    except Exception as e:
        print(f"Error fetching user by ID from database: {e}")
        return None


def update_user_in_db(user):
    try:
        user_ref = db.reference(f'users/{user.id}')
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

def fetch_all_stores_from_db():
    try:
        stores_ref = db.reference('stores')
        stores_data = stores_ref.get()
        stores = []

        for store_id, store_data in stores_data.items():
            store_name = store_data['name']
            store_bio = store_data['bio']
            times_traded = store_data['times_traded']
            points_traded = store_data['points_traded']

            store_obj = Store(store_name=store_name, store_bio=store_bio)
            store_obj.id = store_id
            store_obj.times_traded = times_traded
            store_obj.points_traded = points_traded

            coupons_data = store_data['coupons']
            for coupon_name, coupon_data in coupons_data.items():
                coupon_obj = Coupon(
                    name=coupon_data['name'],
                    bio=coupon_data['bio'],
                    price=coupon_data['price'],
                    code=coupon_data['code']
                )
                store_obj.coupons[coupon_name] = coupon_obj

            stores.append(store_obj)

        return stores

    except KeyError as e:
        print(f"Missing expected field in store data: {e}")
        return []
    except Exception as e:
        print(f"Error fetching stores from database: {e}")
        return []

def fetch_site_statistics():
    try:
        users_ref = db.reference('users')
        users_data = users_ref.get()
        total_trash_amount = 0
        trash_by_type = {
            'plastic': 0,
            'metal': 0,
            'paper': 0,
            'glass': 0,
            'organic': 0
        }
        all_time_points = 0
        current_points = 0
        points_traded = 0
        number_of_trades = 0

        for id, user_data in users_data.items():
            stats_data = user_data.get('statistics', {})
            total_trash_amount += stats_data.get('total_trash_amount', 0)
            for trash_type, amount in stats_data.get('trash_by_type', {}).items():
                if trash_type in trash_by_type:
                    trash_by_type[trash_type] += amount

            # Accumulate points and trade statistics
            all_time_points += stats_data.get('all_time_points', 0)
            current_points += stats_data.get('current_points', 0)
            points_traded += stats_data.get('points_traded', 0)
            number_of_trades += stats_data.get('number_of_trades', 0)

        site_statistics = {
            'total_trash_amount': total_trash_amount,
            'trash_by_type': trash_by_type,
            'all_time_points': all_time_points,
            'current_points': current_points,
            'points_traded': points_traded,
            'number_of_trades': number_of_trades
        }
        return site_statistics

    except Exception as e:
        print(f"Error fetching site statistics: {e}")
        return {
            'total_trash_amount': 0,
            'trash_by_type': {
                'plastic': 0,
                'metal': 0,
                'paper': 0,
                'glass': 0,
                'organic': 0
            },
            'all_time_points': 0,
            'current_points': 0,
            'points_traded': 0,
            'number_of_trades': 0
        }



