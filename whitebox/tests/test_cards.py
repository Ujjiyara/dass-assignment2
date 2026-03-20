import pytest
from moneypoly.cards import CardDeck

def test_cards_recycle_when_empty():
    deck = CardDeck([{"action": "test", "value": 1, "description": "test"}])
    card1 = deck.draw()
    assert card1 is not None
    # BUG TRIGGER: Assuming deck recycles, the next draw should be the same card
    card2 = deck.draw()
    assert card2 is not None, "Deck ran out of cards instead of recycling!"
    assert card1 == card2

def test_cards_are_shuffled():
    from moneypoly.game import Game
    from moneypoly.cards import CHANCE_CARDS
    # Verify decks are shuffled on game start
    game = Game(["P1"])
    is_same = True
    for i in range(len(CHANCE_CARDS)):
        drawn = game.chance_deck.draw()
        if drawn != CHANCE_CARDS[i]:
            is_same = False
            break
    assert not is_same, "Decks were not shuffled during game initialization"
