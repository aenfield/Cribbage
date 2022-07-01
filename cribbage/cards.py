from calendar import c
import itertools

# I based some of the cards impl off of ideas and code in the O'Reilly "Fluent Python" book.
RANKS = list('A23456789TJQK')
SUITS = list('SHDC')


class Deck:

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in SUITS
                                        for rank in RANKS]

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

    def score(self, cut_card=None, crib=False):
        #cards_hand_only = self._cards
        #cards_with_cut = Hand._add_to_list_if_not_none(self._cards, cut_card)

        points = 0
        
        # points += Hand._score_15(self.combinations(cut_card))
        # points += Hand._score_pair(self.combinations(cut_card))
        points += Hand._score_with_combinations(Hand._score_15, self.combinations(cut_card))
        points += Hand._score_with_combinations(Hand._score_pair, self.combinations(cut_card))

        points += Hand._score_with_combinations(lambda c: Hand._score_flush(c, cut_card, crib), self.combinations())

        points += Hand._score_straight(self._cards, cut_card)

        return points

    def combinations(self, cut_card=None):
        """Return a list of tuples, one for each combination of the four (or five, with cut) cards."""
        cards = Hand._add_to_list_if_not_none(self._cards, cut_card)
        combinations_not_flattened = []
        for i in range(1, len(cards) + 1): # we want combinations with 1 to n cards
            combinations_not_flattened.append(itertools.combinations(cards, i))

        return list(itertools.chain(*combinations_not_flattened)) # go ahead and convert to list now, so at least len works w/o further code

    @staticmethod
    def _score_with_combinations(score_func, combinations):
        points_for_all_combinations = [score_func(cards) for cards in combinations]
        return sum(points_for_all_combinations)

    @staticmethod
    def _score_15(cards_with_cut):
        total = sum([card.value for card in cards_with_cut])
        return 2 if total == 15 else 0

    @staticmethod
    def _score_pair(cards_with_cut):
        if len(cards_with_cut) == 2 and cards_with_cut[0].rank == cards_with_cut[1].rank:
                return 2
        else:
            return 0

    @staticmethod
    def _score_flush(cards_hand_only, cut_card=None, crib=False):
        # rule: for hands, 4 or 5 of the same suit score, for crib all five have to have the same suit (right?)

        if len(cards_hand_only) < 4:
            return 0

        is_hand_a_flush = all([cards_hand_only[0].suit == card.suit for card in cards_hand_only[1:]])
        cut_card_matches_suit = cut_card and cards_hand_only[0].suit == cut_card.suit # match against first hand card (before the and to ret false when cut card isn't provided)
        if is_hand_a_flush:
            if not crib: # four hand cards w/ same suit score 4, if the cut card is also the same suit score 5
                if cut_card_matches_suit:
                    return 5
                else:
                    return 4
            else: # crib, so all five cards must have the same suit, which scores 5
                if cut_card_matches_suit:
                    return 5
                else:
                    return 0
        else:
            return 0

    @staticmethod
    def _score_straight(cards, cut_card):
        # can't use each indiv combination by itself because we only score the largest straight - i.e., a straight of three
        # scores 3, but ONLY if there's no straight of four or five; at the same time we DO want to use the combinations so
        # we can handle multiple straights from  duplicate cards - like AS, 2S, 3S and AS, 2H, 3S
        # so we'll figure out the longest straight using _all_ the cards and score only straights of that length
        all_cards = Hand._add_to_list_if_not_none(cards, cut_card)

        length_of_longest_straight = Hand._get_length_of_longest_straight(all_cards)

        # TODO if/as I move scoring routines to instance methods I won't need to recreate a Hand instance here
        for combination in .combinations(cut_card):


        return 0

    @staticmethod
    def _get_length_of_longest_straight(cards):
        # to help score straights, what's the length of the longest straight? (including one or two)
        # assumes cards ordered by rank (which is default ordering defined by the Card class)
        length_of_longest_straight = 1
        curr_rank_index = cards[0].rank_index # first card
        for curr_card in cards[1:]: # check against all subsequent cards
            prev_rank_index = curr_rank_index
            curr_rank_index = curr_card.rank_index
            if prev_rank_index == curr_rank_index:
                # doesn't stop run, doesn't continue it
                pass 
            elif curr_rank_index == (prev_rank_index + 1):
                # one more than prev rank: continues straight
                length_of_longest_straight += 1
            else:
                # not same or one more, so breaks straight
                length_of_longest_straight = 1

        return length_of_longest_straight

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

    def __eq__(self, other):
        return (self.rank, self.suit) == (other.rank, other.suit)

    def __lt__(self, other):
        return (self.rank_index, self.suit_index) < (other.rank_index, other.suit_index)  

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

    @property
    def rank_index(self):
        return RANKS.index(self.rank)

    @property
    def suit_index(self):
        return SUITS.index(self.suit)
