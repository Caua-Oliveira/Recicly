from code.coupon import Coupon

class Store:
    def __init__(self, store_name, store_bio):
        self.name = store_name
        self.bio = store_bio
        self.id = store_name+"id"
        self.coupons = {}  
        self.times_traded = 0
        self.points_traded = 0

    def redeem_coupon(self, coupon_name, user):
        for coupon_code, coupon_obj in self.coupons.items():
            if coupon_obj.name.strip().lower() == coupon_name.lower():
                if user.statistics.remove_points(coupon_obj.price):
                    self.times_traded += 1
                    self.points_traded += coupon_obj.price
                    print(f"Código do cupom: {coupon_obj.code}")
                    return True, coupon_obj.code

        print("Falha na transação. Cupom não encontrado ou pontos insuficientes.")
        return False

    def add_coupon(self, name, bio, price, code):
        self.coupons[name] = Coupon(name, bio, price, code)

    def remove_coupon(self, name):
        if name in self.coupons:
            del self.coupons[name]

    def update_store_bio(self, new_bio):
        self.bio = new_bio

    def __str__(self):
        return f"Loja: {self.name}, Descricao: {self.bio}, Cupons: {len(self.coupons)}"
