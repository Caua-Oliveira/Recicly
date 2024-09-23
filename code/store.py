from coupon import Coupon

class Store:
    def __init__(self, store_name, store_bio):
        self.name = store_name
        self.bio = store_bio
        self.coupons = {}  
        self.times_traded = 0
        self.points_traded = 0

    def redeem_coupon(self, coupon_name, user):
        if coupon_name in self.coupons:
            coupon = self.coupons[coupon_name]
            if user.statistics.remove_points(coupon.price):
                self.times_traded += 1
                self.points_traded += coupon.price
                print(f"Coupon code: {coupon.code}")
                return True
        print("Transaction failed.")
        return False

    def add_coupon(self, name, bio, price, code):
        self.coupons[name] = Coupon(name, bio, price, code)

    def modify_coupon(self, name, bio=None, price=None, code=None):
        if name in self.coupons:
            if bio:
                self.coupons[name].bio = bio
            if price:
                self.coupons[name].price = price
            if code:
                self.coupons[name].code = code

    def remove_coupon(self, name):
        if name in self.coupons:
            del self.coupons[name]

    def update_store_bio(self, new_bio):
        self.bio = new_bio

    def __str__(self):
        return f"Store: {self.name}, Bio: {self.bio}, Coupons: {len(self.coupons)}"
