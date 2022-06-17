import cards

class TestDeck:
    def test_deck_has_52_cards(self):
        sut = cards.Deck()
        assert len(sut) == 52

    def test_deck_gives_cards(self):
        sut = cards.Deck()
        assert sut[0].rank == 'A'
        assert sut[0].suit == 'spades'

class TestCard:
    def test_card_has_rank_and_suit(self):
        sut = cards.Card(rank='K', suit='spades')
        assert sut.rank == 'K'
        assert sut.suit == 'spades'