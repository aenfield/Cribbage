import cards

import random # for shuffle
# These are pytest tests - no imports are needed, so noting this here in case I'd otherwise forget :-)


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

    def test_hand_exposes_card_combinations(self):
        sut_hand = cards.Hand.from_specs(['2S', '4C', '6D', '8H'])
        assert len(sut_hand.combinations()) == 15

    def test_hand_exposes_card_combinations_with_cut_card(self):
        sut_hand = cards.Hand.from_specs(['2S', '4C', '6D', '8H'])
        assert len(sut_hand.combinations(cards.Card.from_spec('KH'))) == 31

    def test_hand_combinations_dont_include_empty_and_do_include_both(self):
        sut_hand_combos = cards.Hand.from_specs(['7H','8D']).combinations()
        assert len(sut_hand_combos) == 3
        assert sut_hand_combos[0][0] == cards.Card.from_spec('7H')
        assert sut_hand_combos[1][0] == cards.Card.from_spec('8D')
        assert sut_hand_combos[2] == (cards.Card.from_spec('7H'), cards.Card.from_spec('8D'))

    # TODO should update indiv score routines to just use Hand members to simplify call, and because each indiv detail 
    # routine should worry about whether it wants combinations and if so how (for ex, i think runs will need the full hand
    # and the combinations)
    # TODO when things are working, may want to set combinations when _cards is set, and retrieve the already calculated 
    # sequence from then on out (figuring out combos seems like it's many cycles, but may not matter) 

    # Note that below so far I'm testing the internal score routines, like _score_15, indirectly via score, by defining hands
    # that _only_ give scores from the specified internal score routine - maybe I should just test the score routines directly 

    def test_hand_worth_zero_scores_zero(self):
        sut_nothing = cards.Hand.from_specs(['2S', '4C', '6D', '8H', 'KH'])
        assert sut_nothing.score() == 0

    # 15
    def test_hand_scores_single_15_with_two_cards(self):
        sut_15 = cards.Hand.from_specs(['7H', '8S'])
        assert sut_15.score() == 2

    def test_hand_scores_single_15_with_three_cards(self):
        sut_15 = cards.Hand.from_specs(['2S', '4D', '9C'])
        assert sut_15.score() == 2

    def test_hand_scores_single_15_with_cut_card(self):
        sut_15 = cards.Hand.from_specs(['7H'])
        assert sut_15.score(cards.Card.from_spec('8D')) == 2

    # flush
    def test_hand_scores_flush_without_matching_cut_card(self):
        sut_flush = cards.Hand.from_specs(['AS', '2S', '6S', 'KS'])
        assert sut_flush.score(cards.Card.from_spec('QD')) == 4

    def test_hand_scores_flush_with_matching_cut_card(self):
        sut_flush = cards.Hand.from_specs(['AS', '2S', '6S', 'KS'])
        assert sut_flush.score(cards.Card.from_spec('QS')) == 5

    def test_crib_hand_doesnt_score_flush_without_matching_cut_card(self):
        sut_flush = cards.Hand.from_specs(['AS', '2S', '6S', 'KS'])
        assert sut_flush.score(cards.Card.from_spec('QD'), crib=True) == 0

    def test_crib_hand_scores_flush_with_cut_card_matching(self):
        sut_flush = cards.Hand.from_specs(['AS', '2S', '6S', 'KS'])
        assert sut_flush.score(cards.Card.from_spec('QS'), crib=True) == 5

    # pairs
    def test_hand_scores_pair_using_two_cards(self):
        sut_pair = cards.Hand.from_specs(['5H','5D'])
        assert sut_pair.score() == 2

    def test_hand_scores_pair_using_one_card_and_cut_card(self):
        sut_pair = cards.Hand.from_specs(['5H'])
        assert sut_pair.score(cards.Card.from_spec('5S')) == 2

    def test_hand_scores_pair_with_three_cards(self):
        # rely on score calling with all combinations so it also is called w/ the 
        # two-card combos and we get the pair there
        sut_pair = cards.Hand.from_specs(['5H','5D','3C'])
        assert sut_pair.score() == 2



    # TODO can score hand - size four, with cut card 
    # TODO for scoring, support 15s, runs, flushes, pairs, nobs
    # TODO note that flushes require the four non-cut cards to be the same suit, so scoring does require knowing what it is


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

    def test_card_value_is_rank_for_numeric_cards(self):
        assert cards.Card.from_spec('2D').value == 2
        assert cards.Card.from_spec('4H').value == 4
        assert cards.Card.from_spec('9S').value == 9

    def test_card_value_is_one_or_ten_for_nonnumeric_cards(self):
        assert cards.Card.from_spec('AS').value == 1
        assert cards.Card.from_spec('TD').value == 10
        assert cards.Card.from_spec('JC').value == 10
        assert cards.Card.from_spec('QH').value == 10
        assert cards.Card.from_spec('KS').value == 10

    def test_can_compare_cards(self):
        assert cards.Card.from_spec('7H') == cards.Card.from_spec('7H')

    def test_can_sort_cards_with_numeric_ranks(self):
        sut_sort = sorted(cards.Hand.from_specs(['7S', '2S']))
        assert sut_sort[0] == cards.Card.from_spec('2S')
        assert sut_sort[1] == cards.Card.from_spec('7S')

    def test_can_sort_cards_with_alpha_and_numberic_ranks(self):
        sut_sort = sorted(cards.Hand.from_specs(['KS','AS','JS','7S','0S','2S']))
        assert sut_sort[0] == cards.Card.from_spec('AS')
        assert sut_sort[1] == cards.Card.from_spec('2S')
        assert sut_sort[2] == cards.Card.from_spec('7S')
        assert sut_sort[3] == cards.Card.from_spec('0S')
        assert sut_sort[4] == cards.Card.from_spec('JS')
        assert sut_sort[5] == cards.Card.from_spec('KS')

    def test_can_sort_cards_with_different_suits(self):
        sut_sort = sorted(cards.Hand.from_specs(['7S', '2C', '2S']))
        assert sut_sort[0] == cards.Card.from_spec('2S')
        assert sut_sort[1] == cards.Card.from_spec('2C')
        assert sut_sort[2] == cards.Card.from_spec('7S')
