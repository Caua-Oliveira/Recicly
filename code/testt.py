
from store import Store
from database_connection import *
from coupon import Coupon
def add_store():
    store_name = input("Enter store name: ")
    store_bio = input("Enter store bio: ")

    # Create Store instance
    store = Store(store_name, store_bio)

    # Reference to the Firebase Realtime Database
    ref = db.reference("stores").child(store.id)

    # Data to store in Firebase
    store_data = {
        "name": store.name,
        "bio": store.bio,
        "times_traded": store.times_traded,
        "points_traded": store.points_traded,
        "coupons": {},  # No coupons yet
    }

    # Push data to Firebase
    ref.set(store_data)
    print(f"Store '{store_name}' added successfully to Firebase!")

def add_coupon_to_store(store_id):
    """Adds a coupon to a specific store in Firebase."""
    # Ask for coupon details
    name = input("Enter coupon name: ")
    bio = input("Enter coupon description: ")
    price = float(input("Enter coupon price (in points): "))
    code = input("Enter coupon code: ")

    # Create a Coupon instance
    coupon = Coupon(name, bio, price, code)

    # Reference to the specific store's coupons in Firebase
    ref = db.reference(f"stores/{store_id}/coupons/{coupon.code}")

    # Data to push to Firebase
    coupon_data = {
        "name": coupon.name,
        "bio": coupon.bio,
        "price": coupon.price,
        "code": coupon.code,
    }

    # Add coupon to Firebase
    ref.set(coupon_data)
    print(f"Coupon '{coupon.name}' added successfully to store with ID '{store_id}'!")

add_coupon_to_store('Papelaria Santanaid')

