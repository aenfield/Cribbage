import cards
from random import shuffle

def print_with_separating_line(str):
    print(str)
    print('----')


class Game:
    def __init__(self, player_one=None, player_two=None):
        self.player_one = player_one if player_one else Player('Player 1')
        self.player_two = player_two if player_two else Player('Player 2')

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

        print_with_separating_line(self.status())

        player_one_crib_cards = self.player_one.get_crib_cards()
        player_two_crib_cards = self.player_two.get_crib_cards()

        print_with_separating_line(self.status())

        # TODO print player hand, get crib choices
        # TODO the play, printing played card sequence and remaining cards in hand, scoring
        # TODO score both hands and crib



class Player:
    def __init__(self, name=None, crib=False, input_func=input):
        if name:
            self.name = name
        else:
            self.name = 'A player'

        self.score = 0
        self.hand = None
        self.crib = crib
        self.input_func = input_func

    def status(self):
        crib_status = '(crib)' if self.crib else ''
        return f'{self.name}: {self.score}; {crib_status}hand: {str(self.hand)}'

    def get_crib_cards(self):
        """
        Called by external code, like Game - does validation and removal from hand, defers choosing which cards 
        to get_candidate_crib_cards.
        """
        crib_cards = self.get_candidate_crib_cards()
        print(f'Specs for crib cards: {crib_cards}')

        #if not all([candidate_crib_card in self.hand for candidate_crib_card in crib_cards]):
            # raise ValueError(f'At least one specified card not found in hand: {crib_cards} not in {self.hand}.')

        for crib_card in crib_cards:
            try:
                self.hand.remove(crib_card)
            except ValueError:
                raise ValueError(f'At least one specified card not found in hand: {crib_cards} not in {self.hand}.')

        return crib_cards


    def get_candidate_crib_cards(self):
        # base class just returns the first two cards; subclasses can do things differently (like use UI)
        return self.hand[:2]

class UIPlayer(Player):
    def get_candidate_crib_cards(self):
        print(self.status())
        crib_card_specs_as_str = self.input_func('Enter crib cards, comma separated:')
        crib_card_specs = [s.strip() for s in crib_card_specs_as_str.split(',')] # split on comma, strip whitespace
        crib_cards = [cards.Card.from_spec(crib_card_specs[0]), cards.Card.from_spec(crib_card_specs[1])]
        return crib_cards


if __name__ == '__main__':
    g = Game(UIPlayer('Player 1'), UIPlayer('Player 2'))
    g.play()