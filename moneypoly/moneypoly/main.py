"""
Main entry point for the MoneyPoly game.
"""
from moneypoly.game import Game


def get_player_names():
    """
    Prompt the user to enter player names.
    Returns a list of stripped player names.
    """
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names


def main():
    """
    Initialize and run the MoneyPoly game loop.
    Handles startup configuration and game interruptions.
    """
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
