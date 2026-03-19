import pytest
import random
from moneypoly.dice import Dice

def test_dice_initialization():
    dice = Dice()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0
    
def test_dice_reset():
    dice = Dice()
    # Mock a roll
    dice.die1 = 3
    dice.die2 = 4
    dice.doubles_streak = 1
    dice.reset()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0

def test_dice_roll_bounds():
    dice = Dice()
    seen_values_die1 = set()
    seen_values_die2 = set()
    # We must be able to see a 6 eventually if it's a 6-sided die
    for _ in range(1000):
        dice.roll()
        assert 1 <= dice.die1 <= 6
        assert 1 <= dice.die2 <= 6
        seen_values_die1.add(dice.die1)
        seen_values_die2.add(dice.die2)
        
    assert 6 in seen_values_die1, "Die 1 never rolled a 6 in 1000 rolls, upper bound is broken"
    assert 6 in seen_values_die2, "Die 2 never rolled a 6 in 1000 rolls, upper bound is broken"

def test_dice_doubles_streak():
    dice = Dice()
    # Mock rolls to force doubles behavior
    # Instead of random, let's patch random.randint
    import unittest.mock
    
    with unittest.mock.patch('random.randint') as mock_randint:
        # First roll: Not doubles (2, 3)
        mock_randint.side_effect = [2, 3]
        total = dice.roll()
        assert total == 5
        assert not dice.is_doubles()
        assert dice.doubles_streak == 0
        
        # Second roll: Doubles (4, 4)
        mock_randint.side_effect = [4, 4]
        total = dice.roll()
        assert total == 8
        assert dice.is_doubles()
        assert dice.doubles_streak == 1
        
        # Third roll: Doubles (1, 1)
        mock_randint.side_effect = [1, 1]
        total = dice.roll()
        assert total == 2
        assert dice.is_doubles()
        assert dice.doubles_streak == 2
        
        # Fourth roll: Not doubles (5, 6)
        mock_randint.side_effect = [5, 6]
        total = dice.roll()
        assert total == 11
        assert not dice.is_doubles()
        assert dice.doubles_streak == 0

def test_dice_describe():
    dice = Dice()
    dice.die1 = 3
    dice.die2 = 2
    assert dice.describe() == "3 + 2 = 5"
    
    dice.die1 = 4
    dice.die2 = 4
    assert dice.describe() == "4 + 4 = 8 (DOUBLES)"

def test_dice_repr():
    dice = Dice()
    dice.die1 = 2
    dice.die2 = 5
    dice.doubles_streak = 0
    assert repr(dice) == "Dice(die1=2, die2=5, streak=0)"
