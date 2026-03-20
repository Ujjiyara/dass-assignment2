from streetrace.registration import RegistrationModule
from streetrace.crew_management import CrewManagementModule
from streetrace.inventory import InventoryModule
from streetrace.race_management import RaceManagementModule
from streetrace.results import ResultsModule
from streetrace.mission_planning import MissionPlanningModule
from streetrace.police import PoliceModule
from streetrace.shop import ShopModule

class StreetRaceManager:
    """Facade integrating all StreetRace modules into a unified system."""
    def __init__(self):
        self.reg = RegistrationModule()
        self.crew = CrewManagementModule(self.reg)
        self.inv = InventoryModule()
        self.race = RaceManagementModule(self.crew, self.inv)
        self.results = ResultsModule(self.inv)
        self.mission = MissionPlanningModule(self.crew, self.inv)
        self.police = PoliceModule(self.inv)
        self.shop = ShopModule(self.inv)

if __name__ == "__main__":
    system = StreetRaceManager()
    print("StreetRace Manager CLI initialized and perfectly integrated.")
