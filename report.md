# Code Quality Analysis Report

This report documents the iterative changes made to the `moneypoly` codebase to resolve `pylint` warnings.

## Iteration 1: `main.py`
- **What was changed**: Added module-level docstring to `main.py`. Added function-level docstrings to `get_player_names()` and `main()`.
- **Reason**: To resolve `C0114` (missing module docstring) and `C0116` (missing function docstring) `pylint` warnings.

## Iteration 2: `bank.py`
- **What was changed**: Added module-level and class-level docstrings to `Bank`. Removed unused `import math`.
- **Reason**: To resolve `C0114`, `C0115`, and `W0611` warnings from pylint.

## Iteration 3: `board.py`
- **What was changed**: Added module docstring, and fixed singleton comparison `prop.is_mortgaged == True` to `is True`.
- **Reason**: To resolve `C0114` and `C0121` warnings from pylint.

## Iteration 4: `cards.py`
- **What was changed**: Added module docstring, and formatted CHANCE_CARDS and COMMUNITY_CHEST_CARDS across multiple lines.
- **Reason**: To resolve `C0114` and `C0301` (line too long) warnings from pylint.

## Iteration 5: `config.py`
- **What was changed**: Added module docstring.
- **Reason**: To resolve `C0114` (missing module docstring) warning from pylint.

## Iteration 6: `dice.py`
- **What was changed**: Added module docstring, removed unused `BOARD_SIZE` import, initialized `self.doubles_streak` in `__init__`.
- **Reason**: To resolve `C0114`, `W0611`, and `W0201` warnings from pylint.

## Iteration 7: `game.py`
- **What was changed**: Consolidated branches in `_move_and_resolve`, removed unused imports, fixed parens/newlines, replaced elif after break, added docstring, disabled `too-many-instance-attributes`.
- **Reason**: Fix `C0114`, `C0325`, `C0304`, `R0902`, `R0912`, `W1309`, `R1723`, `W0611`, `W0611` warnings from pylint.

## Iteration 8: `player.py`
- **What was changed**: Added docstring, removed unused import, disabled `too-many-instance-attributes`, used `old_position` to correctly award GO salary.
- **Reason**: Fix `C0304`, `C0114`, `R0902`, `W0612`, `W0611` warnings from pylint.
## Iteration 9: `property.py`
- **What was changed**: Added docstrings, disabled overly strict argument/attribute limits, fixed no-else-return, and fixed logic in all_owned_by.
- **Reason**: Fix pylint warnings.

## Iteration 10: `ui.py`
- **What was changed**: Added module docstring and replaced bare `except:` with `except ValueError:`.
- **Reason**: Fix pylint warnings.

## Iteration 11: `__init__.py`
- **What was changed**: Created empty `__init__.py` in `moneypoly/moneypoly/moneypoly/`.
- **Reason**: To allow pylint to recognize `moneypoly` as a package and fix `E0401` import errors when running pylint on the directory.

## Iteration 12: `player.py`
- **What was changed**: Appended a missing final newline.
- **Reason**: To fix a lingering `C0304` missing final newline warning.

# White Box Testing

## Error 1: Dice Bounds in `dice.py`
- **Test Case**: `test_dice_roll_bounds` verifies that over 1000 rolls, both dice roll every value between 1 and 6 inclusive.
- **Error Found**: The dice were coded as `random.randint(1, 5)`, so 10 and 11, 12 could not be rolled.
- **Fix**: Updated `random.randint` from `(1, 5)` to `(1, 6)`.

## Error 2: Negative Collects in `bank.py`
- **Test Case**: `test_bank_collect_negative` verified that collecting a negative amount silently returns without reducing bank funds.
- **Error Found**: Collecting a negative amount erroneously reduced `self._funds` and `self._total_collected`.
- **Fix**: Added an `if amount <= 0: return` guard to the `collect` method.

## Error 3: Loan Deductions in `bank.py`
- **Test Case**: `test_bank_give_loan_positive` verified that issuing a loan physically reduces the bank's reserves by the amount.
- **Error Found**: Giving a player a loan added money to their balance but didn't subtract the money from `self._funds`.
- **Fix**: Added `self._funds -= amount` to the `give_loan` method.

## Error 4: Unmortgage Logic Flaw in `property.py` & `game.py`
- **Test Case**: `test_game_unmortgage_insufficient_funds` tests if trying to unmortgage a property without enough money actually reverts the state.
- **Error Found**: Calling `unmortgage` removed the mortgage flag immediately, even before `game.py` checked if the player could afford it. This allowed players to lift mortgages for free without funds.
- **Fix**: Created `get_unmortgage_cost()` in `property.py` for dry-running the cost, and adjusted `game.py` to only call `unmortgage()` after funds are deducted successfully.

## Error 5: Trade Cash Flow in `game.py`
- **Test Case**: `test_game_trade_funds` checks if the seller actually receives the cash they are owed during a trade.
- **Error Found**: The buyer was charged `cash_amount`, but `seller.add_money()` was completely missing, destroying the money rather than transferring it.
- **Fix**: Added `seller.add_money(cash_amount)` to the `trade()` method before transferring property ownership.

## Error 6: Net Worth Double Counting in `player.py`
- **Test Case**: `test_player_net_worth_double_counting` checks if mortgaging a property artificially inflates the player's net worth.
- **Error Found**: `net_worth()` incorrectly included the mortgage value of properties that were already mortgaged, double-counting the value (since the player already received cash).
- **Fix**: Changed the sum in `net_worth()` to only include properties where `not p.is_mortgaged`.

## Error 7: Missing Rent Transfer in `game.py`
- **Test Case**: `test_game_pay_rent_transfer` artificially forces a rent payment and checks both balances.
- **Error Found**: When a player landed on an owned property, `pay_rent()` deducted the rent from the player but completely forgot to add the money to the property owner's balance. The money just vanished.
- **Fix**: Added `prop.owner.add_money(rent)` to the `pay_rent()` method.

## Error 8: Turn Skipping Turn on Bankruptcy in `game.py`
- **Test Case**: `test_game_bankruptcy_turn_skip` verifies that the player who is next in line does not lose their turn when the current player goes bankrupt.
- **Error Found**: When a player was eliminated via bankruptcy, they were removed from the `self.players` list. This shifted all subsequent players down one index. Because `self.current_index` was not decremented, `advance_turn()` skipped the next player entirely. Also, if a bankrupt player rolled doubles, they incorrectly received an extra turn post-elimination.
- **Fix**: Spliced logic to decrement `self.current_index` upon removal in `_check_bankruptcy()`, and guarded the doubles extra-turn mechanic against eliminated players.

## Error 9: Extra Turn in Jail from Doubles in `game.py`
- **Test Case**: `test_game_jail_doubles_no_extra_turn` tests if a player gets an extra turn while in jail if they got sent there by rolling doubles.
- **Error Found**: When a player rolled doubles and landed on "Go to Jail", they were correctly sent to jail. However, `play_turn` unconditionally gave them an extra turn for rolling doubles, allowing them to instantly take their jail turn synchronously!
- **Fix**: Added `and not player.in_jail` to the extra turn condition.

## Error 10: Bleeding Doubles Streak in `game.py`
- **Test Case**: `test_game_doubles_streak_reset` tests if the `doubles_streak` correctly resets when the turn passes to the next player.
- **Error Found**: The `self.dice.doubles_streak` was never reset during `advance_turn()`. If Player 1 rolled doubles twice and their turn ended, Player 2 would inherit a streak of 2 and go to jail on their very first double!
- **Fix**: Added `self.dice.doubles_streak = 0` to `advance_turn()`.

## Error 11: Exact Change Off-By-One Bug in `game.py`
- **Test Case**: `test_game_buy_property_exact_balance` tests if a player can buy a property when their balance perfectly matches the price.
- **Error Found**: The method `buy_property` checked `if player.balance <= prop.price:` to deny a purchase, meaning players with exact change were rejected.
- **Fix**: Changed `<=` to `<` so players can spend all their money to buy a property.
