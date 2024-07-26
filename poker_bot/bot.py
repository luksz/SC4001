import pypokerengine
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from collections import defaultdict

class Player:
    def __init__(self, name: str, stack_size: int):
        self.name = name
        self.stack_size = stack_size
        self.hand = []

    def set_hand(self, cards: list[str]):
        self.hand = cards

    def get_hand(self) -> list[str]:
        return self.hand

class PokerGame:
    def __init__(self):
        self.players = []
        self.community_cards = []
        self.pot = 0
        self.current_bets = defaultdict(int)
        self.total_bets = defaultdict(int)

    def add_player(self, name: str, stack_size: int):
        player = Player(name, stack_size)
        self.players.append(player)

    def add_community_cards(self, cards: list[str]):
        if all(is_valid_card(card) for card in cards):
            self.community_cards = cards
        else:
            print("Invalid community cards. Please enter cards in the correct format.")

    def add_cards(self, player_name: str, cards: list[str]):
        if len(cards) != 2:
            print("Error: Each player must have exactly two cards.")
            return
        player_found = False
        for player in self.players:
            if player.name == player_name:
                player_found = True
                if all(is_valid_card(card) for card in cards):
                    player.set_hand(cards)
                else:
                    print("Invalid player cards. Please enter cards in the correct format.")
                break
        if not player_found:
            print(f"Error: Player '{player_name}' does not exist. Cannot add cards to a non-existent player.")

    def update_stack_size(self, player_name: str, stack_size: int):
        player_found = False
        for player in self.players:
            if player.name == player_name:
                player.stack_size = stack_size
                player_found = True
                break
        if not player_found:
            print(f"Error: Player '{player_name}' does not exist.")

    def add_bet(self, player_name: str, amount: int):
        player_found = False
        for player in self.players:
            if player.name == player_name:
                if player.stack_size < amount:
                    print(f"Error: Player '{player_name}' does not have enough chips.")
                    return
                player.stack_size -= amount
                self.pot += amount
                self.current_bets[player_name] += amount
                self.total_bets[player_name] += amount
                player_found = True
                break
        if not player_found:
            print(f"Error: Player '{player_name}' does not exist.")

    def calculate_ev(self, player_name: str) -> float | None:
        try:
            community_cards = gen_cards(self.community_cards) if self.community_cards else []
            player_hand = []
            player_found = False
            
            print(f"Debug: Community cards - {self.community_cards}")
            print(f"Debug: Players - {[player.name for player in self.players]}")
            
            for player in self.players:
                if player.name == player_name:
                    player_hand = gen_cards(player.get_hand())
                    player_found = True
                    break
            if not player_found:
                print(f"Error: Player '{player_name}' does not exist.")
                return None

            print(f"Debug: Player hand for {player_name} - {player_hand}")
            
            nb_simulation = 1000
            win_rate = estimate_hole_card_win_rate(nb_simulation, len(self.players), player_hand, community_cards)
            
            print(f"Debug: Win rate - {win_rate}")
            
            if player_name not in self.total_bets:
                print(f"Error: Player '{player_name}' does not have any bets recorded.")
                return None

            total_bet = self.total_bets[player_name]
            ev = (win_rate * self.pot) - total_bet
            
            print(f"Debug: Total bet for {player_name} - {total_bet}")
            print(f"Debug: Calculated EV for {player_name} - {ev}")
            
            return ev
        except KeyError as e:
            print(f"Error in calculate_ev: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in calculate_ev: {e}")
            return None

    def reset_game(self):
        self.pot = 0
        self.current_bets = defaultdict(int)
        self.total_bets = defaultdict(int)
        self.community_cards = []
        for player in self.players:
            player.hand = []

    def show_info(self):
        print("\nCurrent Game Information:")
        print(f"Pot size: {self.pot}")
        print(f"Community Cards: {' '.join(self.community_cards)}")
        for player in self.players:
            print(f"\nPlayer: {player.name}")
            print(f"Stack Size: {player.stack_size}")
            print(f"Hand: {' '.join(player.get_hand())}")
            print(f"Current Bet: {self.current_bets[player.name]}")
            print(f"Total Bet: {self.total_bets[player.name]}")

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

if __name__ == "__main__":
    def main():
        game = PokerGame()
        while True:
            print("\nMenu:")
            print("1. Add player")
            print("2. Update player stack size")
            print("3. Add cards to player")
            print("4. Add community cards")
            print("5. Set pot size")
            print("6. Add bet")
            print("7. Calculate EV")
            print("8. Reset game")
            print("9. Show game info")
            print("10. Exit")
            command = input("Select an option (1-10): ").strip()

            if command == '1':
                name = input("Enter player name: ").strip()
                stack_size = int(input("Enter stack size: ").strip())
                game.add_player(name, stack_size)
            elif command == '2':
                name = input("Enter player name: ").strip()
                stack_size = int(input("Enter new stack size: ").strip())
                game.update_stack_size(name, stack_size)
            elif command == '3':
                name = input("Enter player name: ").strip()
                cards = input("Enter cards (e.g., AS KS): ").strip().upper().split()
                game.add_cards(name, cards)
            elif command == '4':
                cards = input("Enter community cards (e.g., 2H 3D 7S): ").strip().upper().split()
                game.add_community_cards(cards)
            elif command == '5':
                pot_size = int(input("Enter current pot size: ").strip())
                game.pot = pot_size
            elif command == '6':
                name = input("Enter player name: ").strip()
                amount = int(input("Enter bet amount: ").strip())
                game.add_bet(name, amount)
            elif command == '7':
                name = input("Enter player name: ").strip()
                ev = game.calculate_ev(name)
                if ev is not None:
                    print(f"Expected EV for {name}: {ev}")
                else:
                    print("Could not calculate EV due to an error.")
            elif command == '8':
                game.reset_game()
                print("Game reset.")
            elif command == '9':
                game.show_info()
            elif command == '10':
                break
            else:
                print("Unknown command. Try again.")

    main()
