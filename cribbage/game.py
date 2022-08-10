from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
import cards
from random import Random, shuffle

def print_with_separating_line(str=None):
    if str:
        print(str)
    print('----')


class Game:
    def __init__(self, player_one=None, player_two=None, score_to_win=120):
        self.player_one = player_one if player_one else Player('Player 1')
        self.player_two = player_two if player_two else Player('Player 2')

        self.set_player_crib_status(self.player_one, self.player_two)

        self.deck = cards.Deck()
        self.crib = None
        self.cut_card = None
        self.score_to_win = score_to_win

    def status(self):
        return 'Game status\n{0}\n{1}\nCrib: {2}\nCut card: {3}'.format(self.player_one.status(), self.player_two.status(), self.crib, self.cut_card)
        # above uses .format because f-strings don't support things like \n

    def cut_cards(self):
        # shuffles deck as a side-effect
        shuffle(self.deck)
        self.cut_card = self.deck.draw_hand(1)[0] # indexer to return the Card, not the Hand containing the Card

    def set_player_crib_status(self, crib_player, non_crib_player):
        self.crib_player = crib_player
        self.non_crib_player = non_crib_player
        crib_player.crib = True
        non_crib_player.crib = False

    def swap_crib_player(self):
        self.set_player_crib_status(self.non_crib_player, self.crib_player)

    def update_player_score(self, player, crib=False, print_output=False):
        # score cards, update score, and return True if score is => the winning threshold and False otherwise
        if not crib:
            if print_output:
                print(f'{player.status()}, cut: {self.cut_card}')
            score = player.hand.score(cut_card=self.cut_card)
        else:
            if print_output:
                print(f'Crib: {self.crib}')
            score = self.crib.score(cut_card=self.cut_card, crib=True)

        player.score += score

        if print_output:
            print_with_separating_line(f'Total score: {score}')

        if player.score >= self.score_to_win:
            return True
        else:
            return False


    def play(self):

        # TODO draw for first player

        # one iteration per hand/peg/score 
        while True:
            print_with_separating_line()
            print_with_separating_line(f"Deal. {self.crib_player.name}'s crib.")

            self.deck = cards.Deck()
            shuffle(self.deck)

            self.crib_player.hand = self.deck.draw_hand(6, sort=True)
            self.non_crib_player.hand = self.deck.draw_hand(6, sort=True)

            print_with_separating_line(self.status())

            crib_player_crib_cards = self.crib_player.get_crib_cards()
            non_crib_player_crib_cards = self.non_crib_player.get_crib_cards()
            self.crib = cards.Hand(sorted(crib_player_crib_cards + non_crib_player_crib_cards))

            self.cut_cards()
            print_with_separating_line(self.status())

            # TODO the play, printing played card sequence and remaining cards in hand, scoring

            print_with_separating_line('Score hands and crib')
            # can't break from within the function, so I guess I have to duplicate the check for each call... what's the right/better way to do this?
            # (update_player_score checks to see if the player in question has one and returns True if so)
            if self.update_player_score(self.non_crib_player, print_output=True):
                break
            if self.update_player_score(self.crib_player, print_output=True):
                break
            if self.update_player_score(self.crib_player, crib=True, print_output=True):
                break

            print_with_separating_line(self.status())

            self.swap_crib_player()

        print_with_separating_line(self.status())



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
        crib_status = ' (crib)' if self.crib else ''
        return f'{self.name}: {self.score:3d}, hand: {self.hand}{crib_status}'

    def get_crib_cards(self):
        """
        Called by external code, like Game - does validation and removal from hand, defers choosing which cards 
        to get_candidate_crib_cards. Returns a list of two Card instances.
        """
        crib_cards = self.get_candidate_crib_cards()
        print_with_separating_line(f'Specs for crib cards: {crib_cards}')

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
    # ask someone, like a real person, potentially via UI (whatever's defined in the input_func, which defaults to 'input')
    def get_candidate_crib_cards(self):
        print(self.status())
        crib_card_specs_as_str = self.input_func('Enter crib cards, comma separated:')
        crib_card_specs = [s.strip() for s in crib_card_specs_as_str.split(',')] # split on comma, strip whitespace
        crib_cards = [cards.Card.from_spec(crib_card_specs[0]), cards.Card.from_spec(crib_card_specs[1])]
        return crib_cards

class RandomPlayer(Player):
    # pick cards at random whenever asked
    def get_candidate_crib_cards(self):
        print(self.status())
        hand_copy = self.hand.copy() # copy so we don't change the order of the underlying hand
        shuffle(hand_copy) 
        return hand_copy[:2]


if __name__ == '__main__':
#    g = Game(UIPlayer('Player 1', crib=True), UIPlayer('Player 2'))
#    g = Game(UIPlayer('Player 1', crib=True), RandomPlayer('Random Player'))
    g = Game(RandomPlayer('Random 1'), RandomPlayer('Random 2'))
    g.play()