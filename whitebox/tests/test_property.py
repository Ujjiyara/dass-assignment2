import pytest
from moneypoly.property import Property, PropertyGroup
from moneypoly.player import Player

def test_property_initialization():
    group = PropertyGroup("Test Group", "Blue")
    prop = Property("Boardwalk", 39, 400, 50, group=group)
    assert prop.name == "Boardwalk"
    assert prop.price == 400
    assert prop.base_rent == 50
    assert prop.mortgage_value == 200
    assert not prop.is_mortgaged
    assert prop.group == group
    assert prop in group.properties

def test_property_rent():
    group = PropertyGroup("Test Group", "Blue")
    prop1 = Property("Park Place", 37, 350, 35, group=group)
    prop2 = Property("Boardwalk", 39, 400, 50, group=group)
    player = Player("Test")
    prop1.owner = player
    
    # Rent without full group
    assert prop1.get_rent() == 35
    
    # Rent with full group
    prop2.owner = player
    assert prop1.get_rent() == 70
    
    # Rent when mortgaged
    prop1.mortgage()
    assert prop1.get_rent() == 0

def test_property_mortgage_and_unmortgage():
    prop = Property("Baltic", 3, 60, 4)
    assert prop.mortgage() == 30
    assert prop.is_mortgaged
    
    # Second mortgage attempt returns 0
    assert prop.mortgage() == 0
    
    # Unmortgage
    cost = prop.unmortgage()
    assert cost == int(30 * 1.1)
    assert not prop.is_mortgaged
    
    # Second unmortgage attempt returns 0
    assert prop.unmortgage() == 0
    
def test_property_is_available():
    prop = Property("Oriental", 6, 100, 6)
    assert prop.is_available()
    
    player = Player("Test")
    prop.owner = player
    assert not prop.is_available()

def test_property_group_methods():
    group = PropertyGroup("Railroads", "Black")
    prop1 = Property("Reading", 5, 200, 25)
    prop2 = Property("Penn", 15, 200, 25)
    
    group.add_property(prop1)
    group.add_property(prop2)
    
    assert group.size() == 2
    
    p1 = Player("P1")
    p2 = Player("P2")
    
    prop1.owner = p1
    assert not group.all_owned_by(p1)
    
    prop2.owner = p1
    assert group.all_owned_by(p1)
    
    prop2.owner = p2
    counts = group.get_owner_counts()
    assert counts[p1] == 1
    assert counts[p2] == 1
    
    assert repr(group) == "PropertyGroup('Railroads', 2 properties)"
