import pytest
from moneypoly.board import Board

def test_board_luxury_tax():
    board = Board()
    assert board.get_tile_type(38) == "luxury_tax", "Tile 38 should be luxury_tax, not income_tax!"
    assert board.get_tile_type(4) == "income_tax"

def test_board_properties():
    board = Board()
    assert len(board.properties) == 22 # Standard board has 22 properties
    assert board.properties[0].name == "Mediterranean Avenue"
    
def test_board_get_property_at():
    board = Board()
    prop = board.get_property_at(1)
    assert prop.name == "Mediterranean Avenue"
    
    assert board.get_property_at(0) is None # Go tile
