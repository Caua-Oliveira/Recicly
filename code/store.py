from coupon import Coupon

class Store:
    def __init__(self, store_name, store_bio):
        self.name = store_name
        self.bio = store_bio
        self.id = store_name+"id"
        self.coupons = {}  
        self.times_traded = 0
        self.points_traded = 0

    def redeem_coupon(self, coupon_name, user):
        # Search for the coupon by name
        for coupon_code, coupon_obj in self.coupons.items():
            if coupon_obj.name.strip().lower() == coupon_name.lower():
                # Check if the user has enough points to redeem the coupon
                if user.statistics.remove_points(coupon_obj.price):
                    # Update store statistics
                    self.times_traded += 1
                    self.points_traded += coupon_obj.price
                    print(f"Código do cupom: {coupon_obj.code}")
                    return True  # Coupon successfully redeemed

        print("Falha na transação. Cupom não encontrado ou pontos insuficientes.")
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
        return f"Loja: {self.name}, Descricao: {self.bio}, Cupons: {len(self.coupons)}"
