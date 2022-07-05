import cards

class Game:
    def __init__(self):
        self.player_one = Player('Player 1')
        self.player_two = Player('Player 2') 

        self.deck = cards.Deck()


class Player:
    def __init__(self, name):
        self.name = name



if __name__ == '__main__':
    g = Game()
    