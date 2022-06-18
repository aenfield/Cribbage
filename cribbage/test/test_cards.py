import cards

import random # for shuffle

class TestDeck:
    def test_deck_has_52_cards(self):
        sut = cards.Deck()
        assert len(sut) == 52

    def test_deck_gives_cards(self):
        sut = cards.Deck()
        assert sut[0].rank == 'A'
        assert sut[0].suit == 'spades'

    def test_deck_can_be_shuffled(self):
        sut = cards.Deck()
        random.shuffle(sut)


class TestCard:
    def test_card_has_rank_and_suit(self):
        sut = cards.Card(rank='K', suit='spades')
        assert sut.rank == 'K'
        assert sut.suit == 'spades'