class ResultsModule:
    def __init__(self, inv_mod):
        self.inv = inv_mod
    def record_result(self, winner_name, prize):
        self.inv.add_cash(prize)
        if self.inv.get_cars():
            self.inv.get_cars()[0]["condition"] -= 10 # Simulate damage
        return True
