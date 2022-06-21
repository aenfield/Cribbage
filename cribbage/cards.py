import collections

# I based some of the cards impl off of ideas and code in the O'Reilly "Fluent Python" book.

class Deck:
    ranks = list('A') + [str(n) for n in range(2, 11)] + list('JQK')
    suits = list('SHDC')

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    # to support random.shuffle
    def __setitem__(self, key, value):
        # key is the index position in the deck, value is the Card instance
        self._cards[key] = value

    def draw_hand(self, size):
        hand = self._cards[:size]
        del self._cards[:size]
        # TODO should handle case when deck is empty - won't (ever?) happen in cribbage so I won't worry about it now (or maybe calling code should handle?)
        return hand


class Hand:
    def __init__(self, cards):
        self._cards = cards

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    @staticmethod
    def from_specs(specs):
        return Hand([Card.from_spec(spec) for spec in specs])

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f'{self.rank}{self.suit}'

    def __str__(self):
        suit_char_to_symbol = {
            'S': '\u2660',
            'H': '\u2665',
            'D': '\u2666',
            'C': '\u2663'
        }
        return f'{self.rank}{suit_char_to_symbol[self.suit]}'

    @staticmethod
    def from_spec(spec):
        # 'spec' is a two character string where the rank is the first char and suit the second (S, H, D, or C)
        return Card(spec[0], spec[1])

