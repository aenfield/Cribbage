import collections

# I based some of the cards impl off of ideas and code in the O'Reilly "Fluent Python" book.

# namedtuple gives us a class w/ the named fields - I'll start w/ it and move from it
# if/when needed (for ex, to impl a way to encapsulate that the count/score for a face card
# is 10, which is different from the rank of 11-13)
Card = collections.namedtuple('Card', ['rank', 'suit'])


class Deck:
    ranks = list('A') + [str(n) for n in range(2, 11)] + list('JQK')
    suits = ['spades', 'diamonds', 'clubs', 'hearts']

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]



# if __name__ == '__main__':
#     foo = Card('7', 'spades')
#     print(foo)