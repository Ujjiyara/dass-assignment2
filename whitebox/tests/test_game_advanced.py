import pytest
from moneypoly.game import Game
from moneypoly.property import Property

def test_game_jail_doubles_no_extra_turn():
    game = Game(["Player1", "Player2"])
    p1 = game.players[0]
    
    p1.position = 28 # 2 tiles from Go To Jail (30)
    
    import unittest.mock
    
    # We patch random.randint to roll 1 and 1
    with unittest.mock.patch('random.randint', return_value=1), \
         unittest.mock.patch('builtins.input', return_value='0'):
        # Choice '0' in menu corresponds to Roll
        game.play_turn()
        
    assert p1.in_jail
    
    # BUG TRIGGER: They rolled doubles, so the game skips advance_turn and grants an extra turn!
    assert game.current_player() != p1, "Player received an extra turn after going to jail on doubles!"

def test_game_doubles_streak_reset():
    game = Game(["Player1", "Player2"])
    game.dice.doubles_streak = 2
    game.advance_turn()
    
    # BUG TRIGGER: doubles_streak bleeds to next player because it is not cleared!
    assert game.dice.doubles_streak == 0, "Doubles streak was not reset on turn end!"

def test_game_buy_property_exact_balance():
    game = Game(["P1"])
    p1 = game.players[0]
    prop = Property("Test", 1, 100, 10)
    
    p1.balance = 100
    
    success = game.buy_property(p1, prop)
    
    # BUG TRIGGER: P1 has exactly $100 for a $100 property. The game checks `<=`, preventing the purchase.
    assert success is True
    assert prop.owner == p1, "Player could not buy property with exact change!"
