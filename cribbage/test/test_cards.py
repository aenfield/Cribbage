import cards

import random # for shuffle

class TestDeck:
    def test_deck_has_52_cards(self):
        sut = cards.Deck()
        assert len(sut) == 52

    def test_deck_gives_cards(self):
        sut = cards.Deck()
        assert sut[0].rank == 'A'
        assert sut[0].suit == 'S'

    def test_deck_can_be_shuffled(self):
        sut = cards.Deck()
        random.shuffle(sut)


class TestHand:
    def test_can_create_hand_directly(self):
        sut = cards.Hand([cards.Card('K', 'S')])
        
    def test_hand_has_length(self):
        sut = cards.Hand([cards.Card('K', 'S')])
        assert len(sut) == 1
    
    def test_hand_can_be_indexed_into(self):
        sut = cards.Hand([cards.Card('K', 'S')])
        assert sut[0].rank == 'K'

    def test_can_create_hand_with_multiple_cards_directly(self):
        sut = cards.Hand([cards.Card('K', 'H'), cards.Card('4', 'S')])
        assert len(sut) == 2
        assert sut[1].rank == '4'

    def test_can_create_multicard_hand_with_specs(self):
        sut = cards.Hand.from_specs(['4H', 'KS'])
        assert len(sut) == 2
        assert sut[0].rank == '4'
        assert sut[0].suit == 'H'
        assert sut[1].rank == 'K'
        assert sut[1].suit == 'S'

    def test_can_draw_hands_of_multiple_sizes_from_same_deck(self):
        sut_deck = cards.Deck()
        sut_h1 = sut_deck.draw_hand(6)
        assert len(sut_h1) == 6
        assert sut_h1[0].rank == 'A'
        assert sut_h1[0].suit == 'S'
        assert sut_h1[5].rank == '6'
        assert sut_h1[5].suit == 'S'
        # draw again and confirm we're getting cards we'd expect from the same deck
        sut_h2 = sut_deck.draw_hand(1)
        assert len(sut_h2) == 1
        assert sut_h2[0].rank == '7'
        assert sut_h2[0].suit == 'S'


    # TODO can score hand - size four, with cut card (perhaps provide handy method to add card, or just manually combine?)
    # TODO for scoring, support 15s, runs, flushes, pairs, nobs


class TestCard:
    def test_card_has_rank_and_suit(self):
        sut = cards.Card(rank='K', suit='S')
        assert sut.rank == 'K'
        assert sut.suit == 'S'

    def test_can_create_card_with_shortform_text(self):
        sut = cards.Card.from_spec('4H')
        assert sut.rank == '4'
        assert sut.suit == 'H'

    def test_card_repr_returns_spec(self):
        sut = cards.Card.from_spec('4H')
        assert repr(sut) == '4H'

    def test_card_str_includes_suit_symbols(self):
        sut_hand = cards.Hand.from_specs(['AS','2H','3D','KC'])
        assert str(sut_hand[0]) == 'A\u2660'
        assert str(sut_hand[1]) == '2\u2665'
        assert str(sut_hand[2]) == '3\u2666'
        assert str(sut_hand[3]) == 'K\u2663'
