import pytest
from moneypoly.game import Game

@pytest.fixture
def default_game():
    return Game(["Player 1", "Player 2", "Player 3"])

def test_community_chest_birthday_force_payment(default_game):
    game = default_game
    p1, p2, p3 = game.players[0], game.players[1], game.players[2]
    
    p2_bal_before = p2.balance
    p3_bal_before = p3.balance
    p1_bal_before = p1.balance
    
    p2.deduct_money(p2.balance - 5)
    
    game._apply_card(p1, {"action": "birthday", "value": 10, "description": "bday"})
    
    assert p2.balance == 5 - 10
    assert p3.balance == p3_bal_before - 10
    assert p1.balance == p1_bal_before + 20
