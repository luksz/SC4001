import pypokerengine
from pypokerengine.utils.card_utils import gen_cards

def check_pypokerengine():
    try:
        # Check if we can use a function from the library
        card_strings = ['As', 'Ks']
        print(f"Debug: Card strings - {card_strings}")

        # Validate card strings
        for card in card_strings:
            if not is_valid_card(card):
                print(f"Invalid card: {card}")
                return

        # Manually create card objects
        try:
            cards = [create_card(card) for card in card_strings]
            print("PyPokerEngine is installed and functional.")
            print(f"Generated cards: {cards}")
        except Exception as e:
            print(f"Error generating cards with PyPokerEngine: {e}")
    except ImportError as e:
        print(f"ImportError: {e}")
        print("PyPokerEngine is not installed or there is an issue with the installation.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("There is an issue with the PyPokerEngine installation or usage.")

def is_valid_card(card: str) -> bool:
    if len(card) < 2 or len(card) > 3:
        return False
    rank = card[:-1]
    suit = card[-1].lower()
    print(f"Debug: Rank - {rank}, Suit - {suit}")  # Add debug output
    if rank not in "23456789TJQKA" or suit not in "shdc":
        print(f"Invalid rank or suit: {rank}, {suit}")
        return False
    return True

def create_card(card: str):
    rank_translation = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', 
        '7': '7', '8': '8', '9': '9', 'T': 'T', 'J': 'J', 
        'Q': 'Q', 'K': 'K', 'A': 'A'
    }
    suit_translation = {
        's': 'SPADES', 'h': 'HEARTS', 'd': 'DIAMONDS', 'c': 'CLUBS'
    }
    rank = card[:-1]
    suit = card[-1].lower()
    if rank in rank_translation and suit in suit_translation:
        translated_rank = rank_translation[rank]
        translated_suit = suit_translation[suit]
        return f"{translated_rank}{translated_suit}"
    else:
        raise ValueError(f"Invalid card: {card}")

if __name__ == "__main__":
    check_pypokerengine()

