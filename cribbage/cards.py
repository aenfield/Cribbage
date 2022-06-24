from calendar import c
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

    def score(self, cut_card=None):
        cards = self._cards
        cards_with_cut = Hand._add_to_list_if_not_none(self._cards, cut_card)

        points = 0
        
        points += Hand._score_15(cards_with_cut)
        # points += Hand._score_flush(cards, cut_card)

        return points

    @staticmethod
    def _score_15(cards_with_cut):
        total = sum([card.value for card in cards_with_cut])
        return 2 if total == 15 else 0

    # @staticmethod
    # def _score_flush(cards, cut_card=None):
    #     # if cut_card is provided, it must match too (i.e., for pegging)
    #     all_cards = Hand._add_to_list_if_not_none(cards, cut_card)

    #     if not len(cards) == 4:
    #         return 0
    #     else:
    #         return all([ for card in cards])

    @staticmethod
    def _add_to_list_if_not_none(seq, new_item):
        # looks like Python doesn't provide this generally and the shortest would still be something like:
        # return seq if new_item is None else seq + [new_item]
        if new_item:
            return seq + [new_item]
        else:
            return seq



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

    # __add__ should return the same type - i.e., a Card - which doesn't make sense because you can't have cards
    # with ranks of, say, 18 - instead of doing it this way, I'll just manually sum values when I need to 
    # def __add__(self, other):
    #     return self.value + other.value

    @staticmethod
    def from_spec(spec):
        # 'spec' is a two character string where the rank is the first char and suit the second (S, H, D, or C)
        return Card(spec[0], spec[1])

    @property
    def value(self):
        if self.rank == 'A':
            return 1
        elif self.rank in list('TJQK'):
            return 10
        elif int(self.rank) >= 2 and int(self.rank) <= 9:
            return int(self.rank)
        else:
            raise ValueError(f"Invalid rank: '{self.rank}'")
