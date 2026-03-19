import pytest
from moneypoly.game import Game
from moneypoly.property import Property
from moneypoly.player import Player

def test_game_unmortgage_insufficient_funds():
    game = Game(["Test"])
    player = game.players[0]
    prop = Property("Boardwalk", 39, 400, 50)
    prop.owner = player
    player.add_property(prop)
    
    # Mortgage it
    prop.mortgage()
    assert prop.is_mortgaged
    
    # Player cannot afford (cost is 200 * 1.1 = 220, balance is 1500)
    # Deduct to 100
    player.deduct_money(player.balance - 100)
    assert player.balance == 100
    
    result = game.unmortgage_property(player, prop)
    assert not result
    
    # BUG TRIGGER: It should still be mortgaged since the player didn't have enough money!
    assert prop.is_mortgaged, "Property was unmortgaged even though player had insufficient funds!"

def test_game_trade_funds():
    game = Game(["Seller", "Buyer"])
    seller = game.players[0]
    buyer = game.players[1]
    
    prop = Property("Baltic", 3, 60, 4)
    prop.owner = seller
    seller.add_property(prop)
    
    initial_seller_balance = seller.balance
    
    success = game.trade(seller, buyer, prop, cash_amount=500)
    assert success
    
    assert buyer.balance == 1500 - 500
    # BUG TRIGGER: Seller didn't receive the cash!
    assert seller.balance == initial_seller_balance + 500, "Seller did not receive the cash from the trade!"

def test_game_pay_rent_transfer():
    game = Game(["Owner", "Renter"])
    owner = game.players[0]
    renter = game.players[1]
    
    prop = Property("Boardwalk", 39, 400, 50)
    prop.owner = owner
    owner.add_property(prop)
    
    initial_owner_balance = owner.balance
    initial_renter_balance = renter.balance
    
    game.pay_rent(renter, prop)
    
    assert renter.balance == initial_renter_balance - 50
    # BUG TRIGGER: Owner never receives the money!
    assert owner.balance == initial_owner_balance + 50, "Owner did not receive the rent money!"

