import cards
from random import shuffle

class Game:
    def __init__(self):
        self.player_one = Player('Player 1')
        self.player_two = Player('Player 2') 

        self.deck = cards.Deck()

    def status(self):
        return '{0}\n{1}'.format(self.player_one.status(), self.player_two.status())
        # above uses .format because f-strings don't support things like \n

    def play(self):

        # TODO draw for first player
        self.crib_player = self.player_one

        # one iteration per hand/peg/score 
        #while True:
        shuffle(self.deck)
        self.player_one.hand = self.deck.draw_hand(6)
        self.player_two.hand = self.deck.draw_hand(6)

        print(self.status())


        # TODO print player hand, get crib choices
        # TODO the play, printing played card sequence and remaining cards in hand, scoring
        # TODO score both hands and crib



class Player:
    def __init__(self, name=None, crib=False):
        if name:
            self.name = name
        else:
            self.name = 'A player'

        self.score = 0
        self.hand = None
        self.crib = crib

    def status(self):
        crib_status = '(crib)' if self.crib else ''
        return f'{self.name}: {self.score}; {crib_status}hand: {str(self.hand)}'


if __name__ == '__main__':
    g = Game()
    g.play()