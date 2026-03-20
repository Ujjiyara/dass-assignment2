import pytest
from main import StreetRaceManager


def test_integration_driver_race_registration():
    sys = StreetRaceManager()
    sys.reg.register("Dom")
    sys.crew.assign_role("Dom", "driver", 90)
    sys.inv.add_car("Charger")
    assert sys.race.enter_race("Street Sprint", "Dom") is True

def test_integration_missing_driver():
    sys = StreetRaceManager()
    sys.inv.add_car("Civic")
    with pytest.raises(ValueError):
        sys.race.enter_race("Street Sprint", "Brian")

def test_integration_race_completion_and_prize():
    sys = StreetRaceManager()
    sys.inv.cash = 0
    sys.inv.add_car("Silvia")
    sys.results.record_result("Letty", 5000)
    assert sys.inv.cash == 5000
    assert sys.inv.get_cars()[0]["condition"] == 90

def test_integration_mission_role_validation():
    sys = StreetRaceManager()
    with pytest.raises(ValueError):
        sys.mission.start_mission("strategist", 1000)
    sys.reg.register("Mia")
    sys.crew.assign_role("Mia", "strategist", 80)
    assert sys.mission.start_mission("strategist", 1000) is True
