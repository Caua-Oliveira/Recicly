
from code.database_connection import *
from code.coupon import Coupon
def add_store():
    store_name = input("Nome da loja: ")
    store_bio = input("Bio da loja: ")

    store = Store(store_name, store_bio)

    ref = db.reference("stores").child(store.id)

    store_data = {
        "name": store.name,
        "bio": store.bio,
        "times_traded": store.times_traded,
        "points_traded": store.points_traded,
        "coupons": {},
    }

    ref.set(store_data)

def add_coupon_to_store(store_id):
    name = input("Nome do cupom: ")
    bio = input("Descrição do cupom: ")
    price = float(input("Preço do cupom em pontos: "))
    code = input("Código do cupom: ")

    coupon = Coupon(name, bio, price, code)

    ref = db.reference(f"stores/{store_id}/coupons/{coupon.code}")

    coupon_data = {
        "name": coupon.name,
        "bio": coupon.bio,
        "price": coupon.price,
        "code": coupon.code,
    }
    ref.set(coupon_data)




