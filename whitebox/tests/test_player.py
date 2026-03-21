import pytest
from moneypoly.player import Player
from moneypoly.property import Property

def test_player_net_worth_double_counting():
    player = Player("Test")
    prop = Property("TestProp", 1, 100, 10) # Mortgage value 50
    prop.owner = player
    player.add_property(prop)
    
    initial_net_worth = player.net_worth()
    
    # Player takes mortgage
    payout = prop.mortgage()
    player.add_money(payout) 
    
    # BUG TRIGGER: Net worth shouldn't change just by mortgaging (cash +50, unmortgaged property value -50)
    assert player.net_worth() == initial_net_worth, "Net worth incorrectly increased when mortgaging a property!"
