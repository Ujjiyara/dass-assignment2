import pytest
from moneypoly.game import Game

@pytest.fixture
def default_game():
    return Game(["Player 1", "Player 2", "Player 3"])

def test_free_parking_tax_pool(default_game):
    game = default_game
    p1 = game.players[0]
    initial_p1_bal = p1.balance
    
    # Move to income tax (position 4)
    game._move_and_resolve(p1, 4)
    assert game.bank.tax_pool == 200
    
    # Move to free parking (position 20)
    p1.position = 20
    game._move_and_resolve(p1, 0)
    
    assert game.bank.tax_pool == 0
    assert p1.balance == initial_p1_bal - 200 + 200
