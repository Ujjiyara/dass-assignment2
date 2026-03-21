class ShopModule:
    def __init__(self, inv_mod):
        self.inv = inv_mod
    def buy_car(self, car_name, price):
        if self.inv.deduct_cash(price):
            self.inv.add_car(car_name)
            return True
        raise ValueError("Not enough cash.")
