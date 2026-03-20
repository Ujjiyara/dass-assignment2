import pytest
from main import StreetRaceManager


def test_integration_driver_race_registration():
    sys = StreetRaceManager()
    sys.reg.register("Dom")
    sys.crew.assign_role("Dom", "driver", 90)
    sys.inv.add_car("Charger")
    assert sys.race.enter_race("Street Sprint", "Dom") is True
