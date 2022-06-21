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


class Hand:
    def __init__(self, cards):
        self._cards = cards

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    @staticmethod
    def from_specs(specs):
        # cards = []
        # for spec in specs:
        #     cards.append(Card.from_spec(spec))

        return Hand([Card.from_spec(spec) for spec in specs])

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @staticmethod
    def from_spec(spec):
        # 'spec' is a two character string where the rank is the first char and suit the second (S, H, D, or C)
        return Card(spec[0], spec[1])

