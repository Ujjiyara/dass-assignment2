class RaceManagementModule:
    def __init__(self, crew_mod, inv_mod):
        self.crew = crew_mod
        self.inv = inv_mod
        self.races = []
    def create_race(self, name):
        self.races.append(name)
    def enter_race(self, race_name, driver_name):
        if self.crew.get_role(driver_name) != "driver":
            raise ValueError("Must be a driver.")
        if not self.inv.get_cars():
            raise ValueError("No cars available.")
        return True
