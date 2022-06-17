import cards

class TestCard:
    def test_has_rank_and_suit(self):
        sut = cards.Card('ace', suit='spades')
