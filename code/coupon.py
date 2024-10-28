class Coupon:
    def __init__(self, name, bio, price, code):
        self.name = name
        self.bio = bio
        self.price = price
        self.code = code

    def __str__(self):
        return f"Cupom: {self.name}, Descricao: {self.bio}, Preco: {int(self.price)}, Code: {self.code}"
