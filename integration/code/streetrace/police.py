class PoliceModule:
    def __init__(self, inv_mod):
        self.inv = inv_mod
        self.heat = 0
    def raid_hideout(self):
        if self.heat > 50:
            lost = self.inv.cash // 2
            self.inv.deduct_cash(lost)
            self.heat = 0
            return lost
        return 0
