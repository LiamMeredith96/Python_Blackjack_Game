import random


# Represents a single playing card, with a suit and rank.
class Card:

    def __init__(self, suit, rank):
        self.suit = suit   # Spades, clubs, hearts, diamonds.
        self.rank = rank   # dict: {"rank": "Ace", "value": 11}.

    def __str__(self):
        # Human-readable version of the playing card.
        return f"{self.rank['rank']} of {self.suit}"


# Represents a full deck (52) of playing cards.
class Deck:

    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
                {"rank" : "Ace", "value" : 11},
                {"rank" : "2", "value" : 2},
                {"rank" : "3", "value" : 3},
                {"rank" : "4", "value" : 4},
                {"rank" : "5", "value" : 5},
                {"rank" : "6", "value" : 6},
                {"rank" : "7", "value" : 7},
                {"rank" : "8", "value" : 8},
                {"rank" : "9", "value" : 9},
                {"rank" : "10", "value" : 10},
                {"rank" : "Jack", "value" : 10},
                {"rank" : "Queen", "value" : 10},
                {"rank" : "King", "value" : 10},
            ]

        # Builds the full deck.
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    # Shuffles the deck randomly.
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    # Deal up to `number` cards from the deck. Returns a list of Card instances.
    # If the deck doesn't have enough cards left, fewer cards will be returned.
    def deal(self, number):
        cards_dealt = []
        for x in range (number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt
    

# Represents the dealer's and and player's hands.
class Hand:

    def __init__(self, dealer=False):
        self.cards = []   # List of card objects.
        self.value = (0)   
        self.dealer = dealer   # True if this is the dealer's hand.

    # Adds a list of cards to the hand.
    def add_card(self, card_list):
        self.cards.extend(card_list)

    # Calculate the value of the hand. Aces are counted as 11 by default, but if the total is > 21, we treat one Ace as 1 instead (subtract 10).
    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "Ace":
                has_ace = True

        # If there's an Ace and we're bust, the Ace is treated as 1 instead of 11.
        if has_ace and self.value > 21:   
            self.value -= 10

    # Returns the value of the hand.
    def get_value(self):
        self.calculate_value()
        return self.value
    
    # Checks if the hand is blackjack (value==21).
    def is_blackjack(self):
        self.calculate_value()
        return self.value == 21 and len(self.cards) == 2
    
    # Prints the hand. Dealer's first card can be hidden unless show_all_dealer_cards is True, or dealer has blackjack.
    def display(self, show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand: ''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print("hidden")
            else:
                print(card)
        
        # Shows the total value only for the player.
        if not self.dealer:
            print("Value", self.get_value())
        print()


# Main blackjack game controller.
class Game:

    #Runs one of more rounds of blackjack.
    def play(self):
        game_number = 0
        games_to_play = 0

        # Asks for input on how many games to play, validating input.
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play?"))
            except:
                print("You must enter a number.")

        # Loops over each game.
        while game_number < games_to_play:
            game_number += 1

            # Creates and shuffles a fresh deck each game.
            deck = Deck()
            deck.shuffle()

            # Creates hands for player and dealer.
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # Initially two cards each
            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            # Checks if there's a blackjack (immediate winner).
            if self.check_winner(player_hand, dealer_hand):
                continue
            
            # Player's turn: hit or stand.
            choice = ""
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Would you like to hit or stand?: ").lower()
                print()

                # Validating input.
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please choose 'Hit' or 'Stand' (or H/S) ").lower()
                    print()

                # If player chooses 'hit', deal one more card and show hand.
                if choice in ["h", "hit"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
            
            # Checks again for bust or blackjack aftr player's turn.
            if self.check_winner(player_hand, dealer_hand):
                continue
            
            # Dealers' turn: must hit until value of cards is at least 17.
            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            # Reveal dealer's hand.
            dealer_hand.display(show_all_dealer_cards=True)

            # Final winner check and results display.
            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final results")
            print("Your hand: ", player_hand_value)
            print("Dealer's hand: ", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print("\nThanks for playing!")
            
    # Determine and print the current game state / winner. 
    # If game_over is False, this is called mid-game to check for busts/blackjacks.
    # If game_over is True, compare final hand values to determine the winner.
    def check_winner(self, player_hand, dealer_hand, game_over=False):

        if not game_over:
            if player_hand.get_value() > 21:
                print("You've gone bust, dealer wins!")
                return True
            elif dealer_hand.get_value() > 21:
                print("The dealer's gone bust, you win!")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have blackjack, it's a tie.")
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack, you win!")
                return True
            elif dealer_hand.is_blackjack():
                print("The dealer has blackjack, you lose!")
                return True
        else:
            # End of game comparison
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win!")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("It's a tie.")
            else:
                print("Dealer wins!")
            return True
        return False


g = Game()
g.play()