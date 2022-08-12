import cards
import random   

SCORE_TO_WIN = 120

class WinningScoreException(Exception):
    """
    Raised when a player achieves at least the winning score. Defined as an exception so we can check for the condition in a single
    place (currently in the Player.score property set impl) and affect outer/calling code without requiring a series of return 
    values and conditional checks. Also, winning doesn't happen much, so it's 'exceptional' :-). 
    """
    pass

def print_with_separating_line(str=None):
    if str:
        print(str)
    print('----')


class Game:
    def __init__(self, player_one=None, player_two=None, score_to_win=SCORE_TO_WIN):
        self.player_one = player_one if player_one else Player('Player 1', score_to_win=score_to_win)
        self.player_two = player_two if player_two else Player('Player 2', score_to_win=score_to_win)

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
        random.shuffle(self.deck)
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
        try:
            # Note that I test individual parts of this loop, but the loop still has some logic which I don't currently test
            # TODO probably best to extract the logic so I can test it in test_game.py  
            while True:
                print_with_separating_line()
                print_with_separating_line(f"Deal. {self.crib_player.name}'s crib.")

                self.deck = cards.Deck()
                random.shuffle(self.deck)

                self.crib_player.hand = self.deck.draw_hand(6, sort=True)
                self.non_crib_player.hand = self.deck.draw_hand(6, sort=True)

                print_with_separating_line(self.status())

                crib_player_crib_cards = self.crib_player.get_crib_cards()
                non_crib_player_crib_cards = self.non_crib_player.get_crib_cards()
                self.crib = cards.Hand(sorted(crib_player_crib_cards + non_crib_player_crib_cards))

                self.cut_cards()
                print_with_separating_line(self.status())

                # print_with_separating_line('The play')
                # self.do_play_loop()
                
                print_with_separating_line('Score hands and crib')
                # TODO update name to show that we score the hand/crib and then update score - maybe 'score_cards_and_update_player_score'
                self.update_player_score(self.non_crib_player, print_output=True)
                self.update_player_score(self.crib_player, print_output=True)
                self.update_player_score(self.crib_player, crib=True, print_output=True)

                print_with_separating_line(self.status())

                self.swap_crib_player()
        except WinningScoreException as e:
            print_with_separating_line(self.status())

    def do_play_loop(self):
        """Implements 'the play' - pegging, one card at a time, until both players have used all of their cards."""
        curr_play_cards = [] 
        all_play_cards = []

        # TODO should use reset_eligible...
        self.player_one.remaining_cards_for_the_play = self.player_one.hand.copy()
        self.player_two.remaining_cards_for_the_play = self.player_two.hand.copy()

        curr_play_player = self.non_crib_player
        # TODO 
        # while at least one player has at least one card remaining
        #   set curr player to the opposite of the last player that played a card or to the non-crib player (at start)
        #   set both player's said_go to false
        #   move curr_play_cards to used_play_cards (will move empty list to empty list in first iteration)
        #   while True: # inner loop for particular 0-31 iteration, exits via break so while True
        #       get card from player, score card, add card to curr cards, set go if no card (via get_and_score_one_play_card) 
        #       if score == 31 or both players have said go:
        #           if score != 31:
        #               score +1 for curr player (always will have been last player to play?)
        #          else:
        #               score +2 for curr player
        #       else:
        #           # continue inner loop
        #           find and set next player (likely via func, look at other player and if they've haven't said go then swap, otherwise leave curr player unchanged)           
        #           (above needs simple 'get_other_player' func on Game)


        self.get_and_score_one_play_card(curr_play_player, curr_play_cards, all_play_cards)

    def get_and_score_one_play_card(self, player, curr_play_cards, all_play_cards):
        curr_play_card = player.get_play_card(curr_play_cards, all_play_cards)
        if curr_play_card:
            curr_play_cards.append(curr_play_card) # curr_play_cards is passed by ref, so this appends to the master list, as desired
            # TODO score, output scoring result, and add score to curr_play_player.score
        else:
            player.said_go = True



class Player:
    def __init__(self, name=None, crib=False, input_func=input, score_to_win=SCORE_TO_WIN):
        if name:
            self.name = name
        else:
            self.name = 'A player'

        self._score_to_win = score_to_win
        self.score = 0
        self.hand = None
        self.crib = crib
        self.input_func = input_func
        self.remaining_cards_for_the_play = [] # currently set by reset_eligible_play_cards

    @property 
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        if self._score >= self._score_to_win:
            raise WinningScoreException()

    def status(self):
        crib_status = ' (crib)' if self.crib else ''
        return f'{self.name}: {self.score:3d}, hand: {self.hand}{crib_status}'

    def get_crib_cards(self):
        """
        Called by external code, like Game - does validation and removal from hand, defers choosing which cards 
        to get_candidate_crib_cards, which subclasses can override. Returns a list of two Card instances.
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

    def get_play_card(self, curr_play_cards, all_play_cards):
        """
        In a similar way as get_crib_cards, this method is called by external code, like Game; this method does validation
        and removal from cards for the play and defers choosing the exact card to get_candidate_play_card, which subclasses
        can override.
        """        
        if len(self.remaining_cards_for_the_play) == 0:
            candidate_play_card = None
            msg = 'has no cards'
        elif (cards.Hand._get_value_total(curr_play_cards) + min([c.value for c in self.hand])) > 31:
            # smallest card would still make the total > 31, so say go
            candidate_play_card = None
            msg = 'says go'
        else: 
            candidate_play_card = self.get_candidate_play_card(curr_play_cards, all_play_cards)
            msg = f'plays {candidate_play_card}'

            try:
                self.remaining_cards_for_the_play.remove(candidate_play_card)
            except ValueError:
                raise ValueError(f'Specified play card {candidate_play_card} not found in {self.remaining_cards_for_the_play}.')


        print(f'{self.name} {msg}')
        return candidate_play_card

    def get_candidate_play_card(self, curr_play_cards, all_play_cards):
        # base class just returns the first card; subclasses can do things differently (like use UI)
        # don't have to worry about saying go, as get_play_card will check this first automatically and only call this method if it can return a card 
        return self.remaining_cards_for_the_play[0]

    def reset_eligible_play_cards(self):
        # whatever's in the hand we call an eligible play card
        self.remaining_cards_for_the_play = self.hand

class UIPlayer(Player):
    # ask someone, like a real person, potentially via UI (whatever's defined in the input_func, which defaults to 'input')
    def get_candidate_crib_cards(self):
        # TODO move status print to get_crib_cards as it's the same in both subclasses?
        print(self.status())
        crib_card_specs_as_str = self.input_func('Enter crib cards, comma separated:')
        crib_card_specs = [s.strip() for s in crib_card_specs_as_str.split(',')] # split on comma, strip whitespace
        crib_cards = [cards.Card.from_spec(crib_card_specs[0]), cards.Card.from_spec(crib_card_specs[1])]
        return crib_cards

    def get_candidate_play_card(self, curr_play_cards, all_play_cards):
        # TODO add status print for play info - likely curr, all, and eligible?
        # TODO move/implement that the status print in get_play_card so only have to implement it once?
        play_card_spec_as_str = self.input_func('Enter play card:')
        return cards.Card.from_spec(play_card_spec_as_str)

class RandomPlayer(Player):
    # pick cards at random whenever asked
    def get_candidate_crib_cards(self):
        print(self.status())
        return random.sample(list(self.hand), 2) # sample requires a sequence, so use list to get one 

    def get_candidate_play_card(self, curr_play_cards, all_play_cards):
        return random.choice(self.remaining_cards_for_the_play)


if __name__ == '__main__':
#    g = Game(UIPlayer('Player 1', crib=True), UIPlayer('Player 2'))
#    g = Game(UIPlayer('Player 1', crib=True), RandomPlayer('Random Player'))
    g = Game(RandomPlayer('Random 1'), RandomPlayer('Random 2'))
    g.play()