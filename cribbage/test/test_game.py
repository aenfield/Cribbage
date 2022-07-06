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
        assert "Score: 0" in status
        assert "Hand:" in status 