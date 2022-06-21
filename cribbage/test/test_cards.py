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


class TestHand:
    # TODO can create hand directly by spceifying cards
    def test_can_create_hand_directly(self):
        sut = cards.Hand([cards.Card('K', 'spades')])
        
    def test_hand_has_length(self):
        sut = cards.Hand([cards.Card('K', 'spades')])
        assert len(sut) == 1
    
    def test_hand_can_be_indexed_into(self):
        sut = cards.Hand([cards.Card('K', 'spades')])
        assert sut[0].rank == 'K'

    # TODO can create hand directly by specifying cards as strings
    # TODO can get hand from deck, siwth size param - check six and one (for cut card)
    # TODO can score hand - size four, with cut card (perhaps provide handy method to add card, or just manually combine?)
    # TODO for scoring, support 15s, runs, flushes, pairs, nobs


class TestCard:
    def test_card_has_rank_and_suit(self):
        sut = cards.Card(rank='K', suit='spades')
        assert sut.rank == 'K'
        assert sut.suit == 'spades'

    # TODO can create via short form, like '4H' for four of hearts
    # TODO get short form representation (as str?) using either SHDC or Unicode symbols