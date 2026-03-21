import pytest
from moneypoly.game import Game

def test_game_bankruptcy_turn_skip():
    game = Game(["Player1", "Player2", "Player3"])
    p1 = game.players[0]
    p2 = game.players[1]
    p3 = game.players[2]
    
    assert game.current_player() == p1
    
    # Force bankruptcy on p1
    p1.deduct_money(p1.balance + 100)
    assert p1.is_bankrupt()
    
    # Mock roll so they don't roll doubles and don't land on Chance
    import unittest.mock
    import builtins
    with unittest.mock.patch('moneypoly.dice.Dice.is_doubles', return_value=False), \
         unittest.mock.patch('moneypoly.dice.Dice.roll', return_value=3), \
         unittest.mock.patch('builtins.input', return_value='s'):
        game.play_turn()
        
    # p1 should be eliminated
    assert len(game.players) == 2
    assert p1 not in game.players
    
    # The next player should be Player2
    # BUG TRIGGER: Because p1 was removed, p2 shifted to index 0, but advance_turn incremented to index 1 (Player3)
    assert game.current_player() == p2, "Turn skipped! The next player should be Player2, but it was skipped."
