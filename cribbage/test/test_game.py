import game

class TestGame:
    def test_game_has_players(self):
        sut = game.Game()
        assert sut.player_one.name == "Player 1"
        assert sut.player_two.name == "Player 2"

    def test_game_has_deck(self):
        sut = game.Game()
        assert len(sut.deck) == 52

    def test_game_has_play(self):
        sut = game.Game()
        sut.play()


# class TestPlayer:
#     def test_player