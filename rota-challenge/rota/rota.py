from .api import RotaAPI

from pprint import pprint


class Rota(object):
    api = None

    state = ""

    moves = 0
    player_wins = 0
    computer_wins = 0
    games_won = 0

    is_active = False  # timeout checker
    verbose = False

    hash = ""  # the good stuff

    def __init__(self, email, verbose=False):
        self.api = RotaAPI(email)
        self.refresh_stats()
        self.verbose = verbose

    def refresh_stats(self):
        status = self.api.status()['data']

        self.computer_wins = status['computer_wins']
        self.player_wins = status['player_wins']
        self.moves = status['moves']
        self.games_won = status['games_won']
        self.state = status['board']

        # Handle game-ending cases, such as a loss or a hash
        if(self.computer_wins > 0):
            print("GAME LOST :(")
            self.is_active = False
        try:
            self.hash = status['hash']
            print("WE GOT A HASH!!!!")
            with open("HASHITY.HASH", "w") as f:
                f.write(self.hash)
            print("Hash written to HASHITY.HASH in current directory")
            exit()
        except KeyError as e:
            pass
    
    def dump_stats(self):
        return {"computer_wins":self.computer_wins,
                "player_wins":self.player_wins,
                "moves":self.moves,
                "games_won":self.games_won}

    def display_board_minimal(self):
        """Displays the rota board as a 3x3 grid, with stats at the bottom."""

        s = self.state
        return f'''
        {s[0]}{s[1]}{s[2]}
        {s[3]}{s[4]}{s[5]}
        {s[6]}{s[7]}{s[8]}

Games Won/Lost: {self.games_won}/{self.computer_wins}
Moves:          {self.moves}
Player Wins:    {self.player_wins}  
        '''

    def display_board(self):
        """Displays the rota board in ascii art, with the stats at the bottom."""

        s = self.state
        return f'''
                   *** ### ### ***
               *##        {s[1]}        ##* 
           *##            2            ##*
        *##                               ##*
      *##                                   ##*
    *##  {s[0]}                                 {s[2]}  ##*
   *##   1                                 3   ##*
  *##                                           ##*
 *##                                             ##*
 *##                                             ##*
 *## {s[3]}                    {s[4]}                    {s[5]} ##*
 *## 4                    5                   6  ##*
 *##                                             ##*
  *##                                           ##*
   *##                                         ##*
    *##  {s[6]}                                 {s[8]}  ##*
      *## 7                              9  ##*
        *#                                ##*
           *##            8            ##*
               *##        {s[7]}        ##*
                   *** ### ### ***

Games Won/Lost: {self.games_won}/{self.computer_wins}
Moves:          {self.moves}
Player Wins:    {self.player_wins}   

    '''

    def place(self, loc):
        """Make place requests to the api accessible from the board class"""

        try:
            return self.api.place(loc)
        except Exception as e:
            print(e)

    def move(self, piece, loc):
        """Make move requests to the api accessible from the board class"""

        try:
            return self.api.move(piece, loc)
        except Exception as e:
            print(e)
