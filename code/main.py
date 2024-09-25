import urllib.request
import json
import geocoder
from geopy.distance import geodesic
from store import Store
from admin import Admin
import user
from users_list import UserLinkedList
from database_connection import *


# Initialize global variables
def initialize_global_data():
    global my_coords
    ip = geocoder.ip('me')
    my_coords = ip.latlng

    global u_list
    u_list = UserLinkedList()

    global stores
    stores = []

    global admins
    admins = [Admin("Admin", "2", "2")]

initialize_global_data()

def initialize_stores():

    store1 = Store("Green Store", "A store for eco-friendly products")
    store1.add_coupon("10% Off", "10% off on all items", 50, "GREEN10")
    store1.add_coupon("Free Shipping", "Free shipping on orders over $50", 30, "FREESHIP")

    store2 = Store("Tech Recycle", "Recycle your old electronics")
    store2.add_coupon("15% Off", "15% off on electronics", 75, "TECH15")
    store2.add_coupon("Buy 1 Get 1", "Buy one get one free on selected items", 100, "B1G1")

    stores.extend([store1, store2])

initialize_stores()

def fetch_recycling_locations():

    url = "https://geo.salvador.ba.gov.br/arcgis/rest/services/Hosted/cooperativas_p/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    try:
        with urllib.request.urlopen(url) as response:
            return json.load(response)['features']
    except Exception as e:
        print(f"Error fetching recycling locations: {e}")
        return []

def display_recycling_locations():

    features = fetch_recycling_locations()

    # Calculate distance for each feature and store it
    locations_with_distances = []
    for feature in features:
        properties = feature['properties']
        geometry = feature['geometry']
        coordinates = geometry.get('coordinates', [0, 0])
        location_coords = (coordinates[1], coordinates[0])
        distance = geodesic(my_coords, location_coords).kilometers

        locations_with_distances.append((distance, properties, coordinates))

    # Sort by distance (closest to furthest)
    locations_with_distances.sort(key=lambda x: x[0])

    # Display sorted locations
    print("\nRecycling Locations in the City:\n")
    for distance, properties, coordinates in locations_with_distances:
        name = properties.get('nome', 'N/A')
        address = properties.get('endereço', 'N/A')
        contact = properties.get('contato', 'N/A')

        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Contact: {contact}")
        print(f"Coordinates: {coordinates}")
        print(f"Distance from your location: {distance:.2f} km\n")


def sign_up():

    print("Sign Up")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    cpf = input("CPF: ")
    new_user = user.User(name, email, password, cpf)
    
    if save_user_to_db(new_user):
        print("User saved successfully.")
        u_list.append_user(new_user)
    else:
        print("Failed to save user. Please try again.")

def sign_in():

    print("Sign In")
    email = input("Email: ")
    password = input("Password: ")
    user_obj = fetch_user_by_email(email)
    if user_obj and user_obj.verify_password(password):
        print(f"Welcome back, {user_obj.name}!")
        return user_obj
    else:
        print("Invalid credentials.")
        return None

def deliver_trash(user_obj):

    print("Deliver Trash")
    try:
        amount = float(input("Enter the amount of trash delivered (kg): "))
        trash_type = input("Enter the type of trash (plastic/metal/paper/glass/organic): ").lower()
        if trash_type in user_obj.statistics.trash_by_type:
            user_obj.statistics.trash_by_type[trash_type] += amount
            user_obj.statistics.total_trash_amount += amount
            points_earned = int(amount * 10)
            user_obj.statistics.add_points(points_earned)
            print(f"Trash delivered successfully! You earned {points_earned} points.")
        else:
            print("Invalid trash type.")
    except ValueError:
        print("Invalid amount entered.")

def view_statistics(user_obj):

    print(f"Statistics for {user_obj.name}:")
    stats = user_obj.statistics
    print(f"Total trash delivered: {stats.total_trash_amount} kg")
    print(f"Points available: {stats.current_points}")
    print(f"All-time points: {stats.all_time_points}")
    print(f"Points traded: {stats.points_traded}")
    print(f"Number of trades: {stats.number_of_trades}")

def view_ranking_by_trash_amount():

    print("User Ranking:")
    # This section needs actual implementation of user ranking
    u_list.display_rankings()

def view_stores_and_coupons():

    print("Available Stores and Coupons:")
    for store in stores:
        print(f"\nStore: {store.name}\nBio: {store.bio}")
        for coupon_name, coupon in store.coupons.items():
            print(f"  {coupon_name}: {coupon.bio} - {coupon.price} points")

def redeem_coupon(user_obj):

    store_name = input("Enter the store name to redeem a coupon: ")
    for store in stores:
        if store.name == store_name:
            print(f"Coupons available at {store_name}:")
            for coupon_name, coupon in store.coupons.items():
                print(f"{coupon_name} - {coupon.price} points")
            selected_coupon = input("Enter the name of the coupon to redeem: ")
            if store.redeem_coupon(selected_coupon, user_obj):
                print(f"Successfully redeemed {selected_coupon} coupon!")
            return
    print("Store not found.")

def admin_actions():

    print("Admin Actions")
    admin_email = input("Enter admin email: ")
    admin_password = input("Enter admin password: ")
    for admin in admins:
        if admin.email == admin_email and admin.verify_password(admin_password):
            print(f"Welcome, {admin.name}")
            while True:
                action = input("1. Add Store\n2. Remove Store\n3. Logout\nChoose an action: ")
                if action == "1":
                    store_name = input("Store Name: ")
                    store_bio = input("Store Bio: ")
                    stores.append(Store(store_name, store_bio))
                    print(f"Store {store_name} added.")
                elif action == "2":
                    store_name = input("Store Name to remove: ")
                    admin.remove_store(stores, store_name)
                    print(f"Store {store_name} removed.")
                elif action == "3":
                    print("Logging out...")
                    break
        else:
            print("Invalid admin credentials.")

def collection_location_actions():
    login_id = input("Enter the login ID: ")
    login_password = input("Enter the login password: ")
    collection_location_obj = fetch_collection_location_by_login_id(login_id)
    if collection_location_obj:
        if collection_location_obj.login_id == login_id and collection_location_obj.login_password == login_password:
            while True:
                action = input("1. Deliver Trash\n2. View Statistics\n3. Logout\nChoose an action: ")
                if action == "1":
                    collection_location_obj.deliver_trash()
                elif action == "2":
                    print(f"Statistics for {collection_location_obj.name}:")
                    print(f"Total trash received: {collection_location_obj.statistics['total_trash_received']} kg")
                    print("Total trash received by type:")
                    for trash_type, amount in collection_location_obj.statistics['total_trash_received_by_type'].items():
                        print(f"{trash_type.capitalize()}: {amount} kg")
                elif action == "3":
                    print("Logging out...")
        else:
            print("Invalid credentials.")
    else:
        print("Collection location not found.")
def main():

    while True:
        action = input("1. Sign Up\n2. Sign In\n3. Admin Login\n4. View Recycling Locations\n5.Collection Location Login\n6. Exit\nChoose an action: ")
        if action == "1":
            sign_up()
        elif action == "2":
            user_obj = sign_in()
            if user_obj:
                while True:
                    user_action = input("1. Deliver Trash\n2. View Statistics\n3. View Ranking\n4. View Stores and Coupons\n5. Redeem Coupon\n6. Logout\nChoose an action: ")
                    if user_action == "1":
                        deliver_trash(user_obj)
                    elif user_action == "2":
                        view_statistics(user_obj)
                    elif user_action == "3":
                        view_ranking_by_trash_amount()
                    elif user_action == "4":
                        view_stores_and_coupons()
                    elif user_action == "5":
                        redeem_coupon(user_obj)
                    elif user_action == "6":
                        print("Logging out...")
                        break
        elif action == "3":
            admin_actions()
        elif action == "4":
            display_recycling_locations()
        elif action == "5":
            collection_location_actions()
        elif action == "6":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
