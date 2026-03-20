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

def test_integration_mechanic_repair_mission():
    sys = StreetRaceManager()
    sys.inv.add_car("RX7")
    sys.inv.get_cars()[0]["condition"] = 50
    sys.reg.register("Tej")
    sys.crew.assign_role("Tej", "mechanic", 85)
    sys.mission.start_mission("mechanic", 2000)
    assert sys.inv.get_cars()[0]["condition"] == 100

def test_integration_police_and_shop():
    sys = StreetRaceManager()
    sys.inv.cash = 50000
    sys.shop.buy_car("Supra", 40000)
    assert sys.inv.cash == 10000
    sys.police.heat = 100
    lost = sys.police.raid_hideout()
    assert lost == 5000
    assert sys.inv.cash == 5000

def test_integration_full_system_simultaneous_workflow():
    sys = StreetRaceManager()
    
    # 1. Registration & Crew (Must check Registration under the hood)
    sys.reg.register("Vince")
    sys.crew.assign_role("Vince", "driver", 85)
    sys.reg.register("Jesse")
    sys.crew.assign_role("Jesse", "mechanic", 95)
    
    # 2. Add base cash and Shop
    sys.inv.cash = 100000
    sys.shop.buy_car("Subaru BRZ", 25000)
    assert sys.inv.cash == 75000
    
    # 3. Race & Inventory Access
    sys.race.create_race("Redline Run")
    sys.race.enter_race("Redline Run", "Vince")
    
    # 4. Results & Damage
    sys.results.record_result("Vince", 15000)
    assert sys.inv.cash == 90000
    assert sys.inv.get_cars()[0]["condition"] == 90 # Damaged from race
    
    # 5. Police Raid
    sys.police.heat = 100
    sys.police.raid_hideout() # Takes half (45000)
    assert sys.inv.cash == 45000
    
    # 6. Mission Planning & Mechanic Auto-Repair (Uses Crew, fixes Inventory)
    sys.mission.start_mission("mechanic", 5000)
    assert sys.inv.cash == 50000 # 45k + 5k
    assert sys.inv.get_cars()[0]["condition"] == 100 # Mechanics restored car 100%

def test_integration_edge_cases_and_negative_branches():
    sys = StreetRaceManager()
    
    # 1. Registration repeat false block
    sys.reg.register("Han")
    assert sys.reg.register("Han") is False
    
    # 2. Crew assignment for unregistered
    with pytest.raises(ValueError):
        sys.crew.assign_role("Nobody", "driver", 50)
    
    # 3. Race enter without cars block
    sys.reg.register("Sean")
    sys.crew.assign_role("Sean", "driver", 80)
    with pytest.raises(ValueError):
        sys.race.enter_race("Drift King", "Sean")
        
    # 4. Results with empty car inventory (should not crash)
    sys.results.record_result("Sean", 1000)
    assert sys.inv.cash == 1000
    
    # 5. Police raid with low heat
    sys.police.heat = 40
    assert sys.police.raid_hideout() == 0
    assert sys.inv.cash == 1000
    
    # 6. Shop purchase without enough cash
    with pytest.raises(ValueError):
        sys.shop.buy_car("Skyline", 90000)
    
    # 7. Inventory deduction without enough cash
    assert sys.inv.deduct_cash(5000) is False

