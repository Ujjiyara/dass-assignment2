class InventoryModule:
    def __init__(self):
        self.cash = 0
        self.cars = []
    def add_cash(self, amt):
        self.cash += amt
    def deduct_cash(self, amt):
        if self.cash >= amt:
            self.cash -= amt
            return True
        return False
    def add_car(self, car_name):
        self.cars.append({"name": car_name, "condition": 100})
    def get_cars(self):
        return self.cars
