import random

from card_game import *

class Black_Jack(Card_Game):

    def __init__(self, number_decks):
        """ Black_Jack (number_decks)
        """
        self.number_decks = number_decks
        self.game_deck    = Card_Game.get_new_decks(self, self.number_decks)
        self.dealer       = Black_Jack.Dealer(self)
        self.players      = []

    def add_player(self, player):
        self.players.append(player)

    def hand_value(self, hand):
        total = 0
        aces  = 0
        for card in hand:
            if card.name == 'Ace': aces += 1
            total += card.value
        while total > 21:
            if aces:
                total -= 10
                aces  -= 1
            else:
                break
        return total

    def play(self, testPlay=False, standValue=17):
        num_busted = 0
        if len(self.players) == 0:
            print "No players have joined the game yet"
            return

        # Deal first two cards to everyone
        for i in [0, 1]:
            # Deal cards to players
            for player in self.players:
                card = self.dealer.deal()
                print "'%s' gets: %s" % (player.name, card)
                player.hand.append(card)
            # Deal the dealer's cards
            card = self.dealer.deal()
            if i == 0:
                print "Dealer gets: %s\n" % card
            else:
                print "Dealer gets: 'Hole card'\n"
            self.dealer.hand.append(card)

        # Allow each player to play in turn
        for player in self.players:
            player.hands_played += 1
            print ''
            total = self.hand_value(player.hand)
            if total == 21:
                self.has_BJ = True
                print "'%s' has Black Jack!" % player.name
                next
            else:
                self.has_BJ = False

            while True:
                print "'%s' has: %i" % (
                    player.name, self.hand_value(player.hand)
                    )
                if testPlay:
                    if self.hand_value(player.hand) < standValue:
                        ans = '' # Indicate 'hit'
                    else:
                        ans = 'n'
                else:
                    ans = raw_input('Hit ? ("n" for no, null for yes) ')
                if len(ans) == 0:
                    card = self.dealer.deal()
                    print "'%s' gets: %s" % (player.name, card)
                    player.hand.append(card)
                    total = self.hand_value(player.hand)
                    if total > 21:
                        player.losses += 1
                        num_busted    += 1
                        print "'%s' has %i - Busted!" % (player.name, total)
                        break
                else:
                    print "'%s' stands with: %i" % (
                        player.name, self.hand_value(player.hand)
                        )
                    break

        # Dealer finishes his/her turn
        dealers_total = self.hand_value(self.dealer.hand)
        if dealers_total == 21:
            self.dealer.has_BJ = True
        else:
            self.dealer.has_BJ = False

        print "Dealer's first card was %s" % self.dealer.hand[0]
        if num_busted < len(self.players):
            print "Dealer's hole card is   %s" % self.dealer.hand[1]
            if self.dealer.has_BJ:
                print "Dealer has Black Jack!"
        else:
            print "Dealer's hole card was %s" % self.dealer.hand[1]
            if self.dealer.has_BJ:
                print "Dealer had Black Jack!"
            else:
                print "Dealer had %i" % dealers_total
            # Dealer picks up cards before next play round
            self.dealer.take_cards()
            return

        while True:
            if dealers_total > 21:
                print "Dealer Busted!"
                break
            elif dealers_total < 18:
                # Dealer hits on 'soft' 17
                card = self.dealer.deal()
                print "Dealer gets: %s\n" % card
                self.dealer.hand.append(card)
                dealers_total = self.hand_value(self.dealer.hand)
            else:
                if not self.dealer.has_BJ:
                    print "Dealer stands with: %i" % dealers_total
                break

        # Check if any non-busted players win
        for player in self.players:
            player_total = self.hand_value(player.hand)
            if player_total < 22:
                # Resolve Black Jacks
                if self.dealer.has_BJ or player.has_BJ:
                    if not self.dealer.has_BJ:
                        player.wins += 1
                        print "'%s' Wins with Black Jack!" % player.name
                        print player
                    elif not player.has_BJ:
                        player.losses += 1
                        print "'%s' Losses to Dealer's Black Jack!" % player.name
                        print player
                    else:
                        player.pushes += 1
                        print "'%s' Push! (tied Black Jacks)" % player.name
                else:
                    # Resolve non Black Jack cases
                    if player_total > dealers_total or dealers_total > 21:
                        player.wins += 1
                        print "'%s' Wins!" % player.name
                        print player
                    elif player_total == dealers_total:
                        player.pushes += 1
                        print "'%s' Push! (tie)" % player.name
                    else:
                        player.losses += 1
                        print "'%s' Losses!" % player.name
                        print player
            else:
                print "'%s' previously busted" % player.name

        # Dealer picks up cards before next play round
        self.dealer.take_cards()

    class Dealer():

        def __init__(self, BJ_instance):
            random.shuffle(BJ_instance.game_deck)
            self.hand         = []
            self.discard_pile = []
            self.game         = BJ_instance

        def deal(self):
            if len(self.game.game_deck) < ((self.game.number_decks * 52) / 4):
                print "Reshuffling..."
                self.game.game_deck += self.discard_pile
                self.discard_pile    = []
                random.shuffle(self.game.game_deck)
            card = self.game.game_deck.pop()
            return card

        def take_cards(self):
            for player in self.game.players:
                self.discard_pile += player.hand
                player.hand = []
            self.discard_pile += self.hand
            self.hand = []

class Player(Black_Jack):

    def __init__(self, name, game):
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
        card = self.game.dealer.deal()
        self.hand.append((card))

    def stats(self):
        print "'%s's Wins: %i (%.2f%%), Losses: %i (%.2f%%), pushes: %i (%.2f%%)" % (
            self.name,
            self.wins,   (self.wins*100.0)/self.hands_played,
            self.losses, (self.losses*100.0)/self.hands_played,
            self.pushes, (self.pushes*100.0)/self.hands_played
            )

    def __str__(self):
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
