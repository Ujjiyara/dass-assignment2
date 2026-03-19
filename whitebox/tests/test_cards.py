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
