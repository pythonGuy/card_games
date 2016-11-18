import random

from card_game import *

class Baccarat(Card_Game):

    def __init__(self, number_decks):
        """ Baccarat (number_decks)
        """
        self.number_decks = number_decks
        self.game_deck    = Card_Game.get_new_decks(self, self.number_decks)
        self.dealer       = Baccarat.Dealer(self)
        self.players      = []

    def add_player(self, player):
        """ add_player
            Adds a play to the game
        """
        self.players.append(player)

    def hand_value(self, hand):
        """ hand_value
            Returns the value of a hand according to Barrarat
        """
        total = 0
        for card in hand:
            if card.value <= 9:
                total += card.value
        total = int(str(total)[-1])
        return total

    def play(self):
        """ play
            Plays one round of Baccarat
        """
        if len(self.players) == 0:
            print "No players have joined the game yet"
            return

        # Deal first two cards to player
        for i in [0, 1]:
            # Deal cards to players
            for player in self.players:
                card = self.dealer.deal()
                print "%s gets: %s" % (player.name, card)
                player.hand.append(card)

        # Deal the dealer's cards
        for i in [0, 1]:
            card = self.dealer.deal()
            print "Dealer gets: %s" % card
            self.dealer.hand.append(card)

        # Update games played by player
        for player in self.players:
            player.hands_played += 1

        # Get totals
        player_total  = player.hand_value(player.hand)
        dealers_total = self.hand_value(self.dealer.hand)
        player_drew   = False
        print "%s total: %s" % (player.name, player_total)
        print "Dealer total: %s\n" % dealers_total
        if player_total <= 5:
            card = self.dealer.deal()
            draw_card = card
            player.hand.append(card)
            print "%s gets: %s" % (player.name, card)
            player_total = player.hand_value(player.hand)
            player_drew  = True
        if dealers_total < 3:
            card = self.dealer.deal()
            print "Dealer gets: %s" % card
            self.dealer.hand.append(card)
            dealers_total = self.hand_value(self.dealer.hand)
        elif dealers_total == 6:
            if draw_card == 6 or draw_card == 7:
                card = self.dealer.deal()
                print "Dealer gets: %s" % card
                self.dealer.hand.append(card)
                dealers_total = self.hand_value(self.dealer.hand)
        elif dealers_total == 5:
            if (not player_drew) or (draw_card > 3 and draw_card < 8):
                card = self.dealer.deal()
                print "Dealer gets: %s" % card
                self.dealer.hand.append(card)
                dealers_total = self.hand_value(self.dealer.hand)
        elif dealers_total == 4:
            if (not player_drew) or (draw_card > 1 and draw_card < 8):
                card = self.dealer.deal()
                print "Dealer gets: %s" % card
                self.dealer.hand.append(card)
                dealers_total = self.hand_value(self.dealer.hand)
        elif dealers_total == 3:
            if (not player_drew) or (draw_card == 9 or draw_card < 8):
                card = self.dealer.deal()
                print "Dealer gets: %s" % card
                self.dealer.hand.append(card)
                dealers_total = self.hand_value(self.dealer.hand)

        print "\nFinal %s total: %s" % (player.name, player_total)
        print "Final %s total: %s" % ("Dealer", dealers_total)

        if player_total > dealers_total:
            print "%s wins" % player.name
            player.wins += 1
        elif player_total < dealers_total:
            print "Dealer wins"
        else:
            print "Game is a 'Tie'"
        self.dealer.take_cards()

    class Dealer():
        """ Dealer
            
            Class for dealer data and methods
        """
        def __init__(self, BJ_instance):
            """ __init__

            Makes a instance of a Baccarat game
            """
            random.shuffle(BJ_instance.game_deck)
            self.hand         = []
            self.discard_pile = []
            self.game         = BJ_instance

        def deal(self):
            """ deal

                Deals from the deck of cards, reshuffling when cards
                remaining less than 25%
            """
            if len(self.game.game_deck) < ((self.game.number_decks * 52) / 4):
                print "Reshuffling..."
                self.game.game_deck += self.discard_pile
                self.discard_pile    = []
                random.shuffle(self.game.game_deck)
            card = self.game.game_deck.pop()
            return card

        def take_cards(self):
            """ take_cards

                Take cards from players returning them to the deck
            """
            for player in self.game.players:
                self.discard_pile += player.hand
                player.hand = []
            self.discard_pile += self.hand
            self.hand = []

class Player(Baccarat):
    """ Player

        Player class
    """

    def __init__(self, name, game):
        """ __init__

            Make and initialize a play instance
        """
        self.name         = name
        self.game         = game
        self.has_BJ       = False
        self.wins         = 0
        self.losses       = 0
        self.pushes       = 0
        self.hands_played = 0
        self.hand         = []
        game.add_player(self)

    def hit(self):
        """ hit

            Request a 'hit' from the dealer
        """
        card = self.game.dealer.deal()
        self.hand.append((card))

    def stats(self):
        """ stats

            Print players statistics
        """
        print "'%s's Wins: %i (%.2f%%), Losses: %i (%.2f%%), pushes: %i (%.2f%%)" % (
            self.name,
            self.wins,   (self.wins*100.0)/self.hands_played,
            self.losses, (self.losses*100.0)/self.hands_played,
            self.pushes, (self.pushes*100.0)/self.hands_played
            )

    def __str__(self):
        """ __str__

            Return a string representation of the player
        """
        total = 0
        aces  = 0
        s1    = "%s's card total:" % self.name
        s2    = ""
        for c in self.hand:
            if c.name == 'Ace': aces += 1
            total += c.value
            s2  += "\n\t%s" % c
        if total == 0:
            return s1 + " 0, Holding no cards"
        if total > 21:
            if aces:
                total  -= 10
                aces -= 1

        return "%s %i, cards:%s" % (s1, total, s2)
