import pytest
from moneypoly.bank import Bank
from moneypoly.config import BANK_STARTING_FUNDS
from moneypoly.player import Player

def test_bank_initialization():
    bank = Bank()
    assert bank.get_balance() == BANK_STARTING_FUNDS
    assert bank.loan_count() == 0
    assert bank.total_loans_issued() == 0

def test_bank_collect_positive():
    bank = Bank()
    initial = bank.get_balance()
    bank.collect(500)
    assert bank.get_balance() == initial + 500
    assert bank._total_collected == 500

def test_bank_collect_negative():
    bank = Bank()
    initial = bank.get_balance()
    bank.collect(-200)
    # Collect says: Negative amounts are silently ignored.
    assert bank.get_balance() == initial, "Bank balance changed when collecting a negative amount!"
    assert bank._total_collected == 0, "Total collected changed for a negative amount!"

def test_bank_pay_out_positive():
    bank = Bank()
    initial = bank.get_balance()
    amount = bank.pay_out(200)
    assert amount == 200
    assert bank.get_balance() == initial - 200

def test_bank_pay_out_negative():
    bank = Bank()
    initial = bank.get_balance()
    amount = bank.pay_out(-100)
    assert amount == 0
    assert bank.get_balance() == initial

def test_bank_pay_out_insufficient_funds():
    bank = Bank()
    with pytest.raises(ValueError):
        bank.pay_out(BANK_STARTING_FUNDS + 100)

def test_bank_give_loan_positive(capsys):
    bank = Bank()
    player = Player("Test")
    initial_bank = bank.get_balance()
    initial_player = player.balance
    
    bank.give_loan(player, 1000)
    
    assert player.balance == initial_player + 1000
    # The bank's funds are currently not being subtracted in give_loan?
    # Let's check: "The bank's own funds are reduced accordingly."
    # The code: player.add_money(amount); self._loans_issued.append...
    # Wait, the bank's own funds are NEVER reduced in the code!
    assert bank.get_balance() == initial_bank - 1000, "Bank funds were not reduced after giving a loan!"
    assert bank.loan_count() == 1
    assert bank.total_loans_issued() == 1000
    
    captured = capsys.readouterr()
    assert "Bank issued a $1000 emergency loan to Test" in captured.out

def test_bank_give_loan_negative():
    bank = Bank()
    player = Player("Test")
    initial_bank = bank.get_balance()
    initial_player = player.balance
    
    bank.give_loan(player, -500)
    
    assert player.balance == initial_player
    assert bank.get_balance() == initial_bank
    assert bank.loan_count() == 0

def test_bank_summary(capsys):
    bank = Bank()
    bank.collect(100)
    bank.summary()
    captured = capsys.readouterr()
    assert "Bank reserves" in captured.out
    assert "Total collected: $100" in captured.out

def test_bank_repr():
    bank = Bank()
    assert repr(bank) == f"Bank(funds={BANK_STARTING_FUNDS})"
