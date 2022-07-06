import cards

class Game:
    def __init__(self):
        self.player_one = Player('Player 1')
        self.player_two = Player('Player 2') 

        self.deck = cards.Deck()

    def play(self):

        # TODO draw for first player
        self.crib_player = self.player_one

        while True:
            # TODO shuffle, deal six-card hands to both players
            # TODO print game status (score)
            # TODO print player hand, get crib choices
            # TODO the play, printing played card sequence and remaining cards in hand, scoring
            # TODO score both hands and crib
            pass  



class Player:
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = 'A player'

        self.score = 0
        self.hand = None

    def status(self):
        return None


if __name__ == '__main__':
    g = Game()
    g.play()