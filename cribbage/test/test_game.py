from numpy import cumprod
import game
import cards

class TestGame:
    def test_game_has_players(self):
        sut = game.Game()
        assert sut.player_one.name == "Player 1"
        assert sut.player_two.name == "Player 2"

    def test_game_has_deck(self):
        sut = game.Game()
        assert len(sut.deck) == 52

    def test_game_prints_status(self):
        sut = game.Game()
        status = sut.status()
        assert "Player 1" in status
        assert "Player 2" in status
        assert "hand" in status
        assert "None" in status # haven't drawn a hand so the hand text will say 'None'

    # def test_game_has_play(self):
    #     sut = game.Game()
    #     sut.play()


class TestPlayer:
    def test_player_has_score(self):
        sut = game.Player()
        assert sut.score == 0

    def test_player_has_hand(self):
        sut = game.Player()
        assert sut.hand is None

    def test_player_prints_status(self):
        sut = game.Player()
        sut.hand = cards.Deck().draw_hand(6)
        status = sut.status()
        assert sut.name in status
        assert "0" in status # score
        assert "hand" in status
        assert "2" in status # there's a 2 card
        assert "crib" not in status

    def test_player_has_crib_property_and_status_shows_crib(self):
        sut = game.Player(crib=True)
        status = sut.status()
        assert "crib" in status

    def test_player_get_crib_cards_returns_two_cards(self):
        sut = game.Player()
        sut.hand = cards.Deck().draw_hand(6)
        crib_cards = sut.get_crib_cards()
        assert len(crib_cards) == 2
        assert crib_cards[0] == cards.Card.from_spec('AS')
        assert crib_cards[1] == cards.Card.from_spec('2S')

    def test_can_create_player_UI_instance(self):
        sut = game.UIPlayer()