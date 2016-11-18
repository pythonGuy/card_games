class Card(object):

    def __init__(self, name, suit, value):
        self.name  = name
        self.suit  = suit
        self.value = value
        if suit[0] == 'S' or suit[0] == 'C':
            self.color = 'Black'
        else:
            self.color = 'Red'

    def __str__(self):
        return "(%s of %s)" % (self.name, self.suit)

class Card_Game(object):
    deck = ( Card('Ace',   'Spades', 11),
             Card('King',  'Spades', 10),
             Card('Queen', 'Spades', 10),
             Card('Jack',  'Spades', 10),
             Card('10', 'Spades', 10),
             Card('9',  'Spades', 9),
             Card('8',  'Spades', 8),
             Card('7',  'Spades', 7),
             Card('6',  'Spades', 6),
             Card('5',  'Spades', 5),
             Card('4',  'Spades', 4),
             Card('3',  'Spades', 3),
             Card('2',  'Spades', 2),
             Card('Ace',   'Clubs', 11),
             Card('King',  'Clubs', 10),
             Card('Queen', 'Clubs', 10),
             Card('Jack',  'Clubs', 10),
             Card('10', 'Clubs', 10),
             Card('9',  'Clubs', 9),
             Card('8',  'Clubs', 8),
             Card('7',  'Clubs', 7),
             Card('6',  'Clubs', 6),
             Card('5',  'Clubs', 5),
             Card('4',  'Clubs', 4),
             Card('3',  'Clubs', 3),
             Card('2',  'Clubs', 2),
             Card('Ace',   'Hearts', 11),
             Card('King',  'Hearts', 10),
             Card('Queen', 'Hearts', 10),
             Card('Jack',  'Hearts', 10),
             Card('10', 'Hearts', 10),
             Card('9',  'Hearts', 9),
             Card('8',  'Hearts', 8),
             Card('7',  'Hearts', 7),
             Card('6',  'Hearts', 6),
             Card('5',  'Hearts', 5),
             Card('4',  'Hearts', 4),
             Card('3',  'Hearts', 3),
             Card('2',  'Hearts', 2),
             Card('Ace',   'Diamonds', 11),
             Card('King',  'Diamonds', 10),
             Card('Queen', 'Diamonds', 10),
             Card('Jack',  'Diamonds', 10),
             Card('10', 'Diamonds', 10),
             Card('9',  'Diamonds', 9),
             Card('8',  'Diamonds', 8),
             Card('7',  'Diamonds', 7),
             Card('6',  'Diamonds', 6),
             Card('5',  'Diamonds', 5),
             Card('4',  'Diamonds', 4),
             Card('3',  'Diamonds', 3),
             Card('2',  'Diamonds', 2)
            )

    def get_new_decks(self, number_new_decks):
        game_deck = [i for i in Card_Game.deck]
        for i in range(number_new_decks - 1):
            game_deck += game_deck
        return game_deck
