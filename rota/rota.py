from .api import RotaAPI

from pprint import pprint


class Rota(object):
    api = None

    state = ""

    moves = 0
    player_wins = 0
    computer_wins = 0
    games_won = 0

    is_active = True  # timeout checker
    is_game_lost= False
    verbose = False

    hash = ""  # the good stuff

    clockwise_list = [2, 3, 6, 9, 8, 7, 4, 1]
   
    # spots opposite to each other
    opposites = [(2, 8), (3, 7), (6, 4), (9, 1)]

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
            self.is_game_lost = True
            self.is_active= False
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

    def display_board_minimal(self, state=state):
        """Displays the rota board as a 3x3 grid, with stats at the bottom."""

        s = state
        return f'''
        {s[0]}{s[1]}{s[2]}
        {s[3]}{s[4]}{s[5]}
        {s[6]}{s[7]}{s[8]}

Games Won/Lost: {self.games_won}/{self.computer_wins}
Moves:          {self.moves}
Player Wins:    {self.player_wins}  
        '''

    def display_board(self, state=state):
        """Displays the rota board in ascii art, with the stats at the bottom."""

        s = state
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
            results= self.api.place(loc)
            self.refresh_stats()
            return results
        except Exception as e:
            print(e)

    def move(self, piece, loc):
        """Make move requests to the api accessible from the board class"""

        try:
            results= self.api.move(piece, loc)
            self.refresh_stats()
            return results
        except Exception as e:
            print(e)



    def mock_move(self, piece, loc, state=self.state):
        """Returns a game state of a move without sending it to the server"""
        future_state = state[0:piece-1]+'-'+state[piece:] # sub out piece to empty space
        future_state = future_state[0:loc-1]+'p'+future_state[loc:]
        return future_state

    def mock_place(self, loc, state=self.state):
        """ Returns a game state of a placement without sending it to the server"""
        future_state = state[0:loc-1]+'p'+state[loc:]
        return future_state

    def find_available_spaces(self, piece, state=self.state):
        """Finds the available spaces for a piece"""
        available = []

        if(piece !=5):
            cclock_spot = self.get_next_position_clockwise(piece, clockwise=False)
            clock_spot = self.get_next_position_clockwise(piece)
            middle = state[4]

            if(state[cclock_spot-1] == '-'):
                available.append(cclock_spot)

            if(state[clock_spot-1] == '-'):
                available.append(clock_spot)
            if(middle == '-'):
                available.append(5)
        else:
            for loc in self.clockwise_list:
                if(self.is_empty(state,loc)):
                    available.append(loc)

        return available


    def is_in_y_position(self,team, state=self.state):
        """Determines if player or opponent are in the y position on the board"""

        for loc in self.clockwise_list:
            expected_cwise = self.get_next_position_clockwise(self.get_opposite_position(loc))
            expected_ccwise = self.get_next_position_clockwise(self.get_opposite_position(loc),clockwise=False)
            if(state[expected_ccwise-1] == team and state[loc-1] == team and state[expected_cwise-1] == team):
                #If all are team members, it must be a y formation
                return True
        return False
        
    def find_game_ending_threats(self, state=self.state):
        print("[Player] Finding threats...")

        threats = []

        # The middle is open, check if there is risk of losing if it is taken
        if(state[4] == '-'):
            if(self.is_threat_in_center(state)):
                # IE:
                #       - - p  or  p - p  or  c - p
                #       c - c      c - c      p - c
                #       - - -      - c p      - - c
                print("[Threat] There is a threat in the center of the board...")
                threats.append(5)  # threat in center

            # if the center is open, there is a chance the border is at risk
            threats_on_border = self.find_threats_on_border(state)
            # IE:
            #       - - p
            #       - - c
            #       - - c
            if(len(threats_on_border) > 0):
                # There is a chance for 2 threats to come out of this function
                threats.extend(threats_on_border)
                print("[Threat] There is a threat on the edge of the board")

        elif(state[4] == 'c'):
            threat_using_center = self.find_threats_using_center(state)
            if(threat_using_center):
                threats.extend(threat_using_center)
                # IE:
                #       - - p
                #       - c c
                #       - - -

                print("[Threat] There is a threat on the edge of the board, using the center")

        return threats

    def is_threat_in_center(self,state=self.state):
        """Checks for threat occurring in the center of the board"""
        
        # we already know that the center is empty
        # Because all pieces can move to this spot, there is no need for a placement mode, it's handled
        # the same.

        for loc1, loc2 in self.opposites:
            if(state[loc1-1] == 'c' and state[loc2-1] == 'c'):
                return True
        return False

    def is_piece_near(self, loc, piece_type):
        """Returns True if a location around the border has a similar piece next to it"""
        locPost = self.get_next_position_clockwise(loc)
        locPrior = self.get_next_position_clockwise(loc, clockwise=False)
        if(piece_type == self.state[locPost-1] or piece_type == self.state[locPrior-1]):
            return True

        return False

    def find_threats_using_center(self, state=self.state):
        """Checks for threat that uses the center piece"""

        # We already know that there is a piece in the center.
        # We need to check if there is another opponent piece on the edge, and
        # if that edge's opposite is empty if it is, the opposite spot is a threat
        
        threats=[]
        for loc1, loc2 in self.opposites:
            if(state[loc1-1] == 'c' and state[loc2-1] == '-'):
                if(self.get_num_pieces_on_board(state,"c") <3):
                    print("\t[!] Threat using center found at: ", loc2)
                    threats.append(loc2)

                else:
                    # We need to check that the threat actually can be moved to by another piece
                    for cloc in self.get_computer_locations(state):
                        if(cloc not in [loc1, 5]):
                            if(loc2 in self.find_available_spaces(state,cloc)):
                                threats.append(loc2) # There is an opponent that can move

            if(state[loc1-1] == '-' and state[loc2-1] == 'c'):
                if(self.get_num_pieces_on_board(state,"c") <3):
                    print("\t[!] Threat using center found at: ", loc1)
                    threats.append(loc1)
                else:
                    for cloc in self.get_computer_locations(state):
                        if(cloc not in [loc2,5]):
                            if(loc1 in self.find_available_spaces(state,cloc)):
                                threats.append(loc1)

        return threats

    def find_threats_on_border(self, state=self.state):
        """Checks for threats that do not use the center, only on the border"""

        # We already know that there is not an opponent piece in the center
        # We need to check along the border for pairs of opponents.
        # if there is an empty space to the left and/or the right, record it

        # c c - 
        # - p c 
        # p - p
        
        threats = []
        for item in self.clockwise_list:
            loc1 = item
            loc2 = self.get_next_position_clockwise(loc1)
            loc3 = self.get_next_position_clockwise(loc2)

            loc1_piece = state[loc1-1]
            loc2_piece = state[loc2-1]
            loc3_piece = state[loc3-1]

            group = loc1_piece + loc2_piece + loc3_piece

            # can't win when if there's a player piece in the set.
            if('p' not in group and group.count('c') == 2):                    
                loc = group.find('-')

                threat=None

                if(loc == 0):
                    threat=loc1    
                elif(loc == 1):
                    threat=loc2
                elif(loc == 2):
                    threat=loc3

        # cc-
        # -pc
        # p-p
        
                if(threat is not None):
                    print(self.state)
                    if(self.get_num_pieces_on_board(state,"c") <3):
                        print("\t[!] Threat on border")
                        threats.append(threat) #this is definitely a threat if there is only 2 pieces on the board
                    else:
                        for cloc in self.get_computer_locations(state):
                            if(cloc not in [loc1,loc2,loc3]):
                                if(threat in self.find_available_spaces(state,cloc)):
                                    print(f"\t[!] Threat on border [{cloc} moves to {threat}]")
                                    threats.append(threat)


        return list(set(threats))


    def get_player_locations(self,state=self.state):
        """Returns locations of all pieces owned by the player"""
        return [i+1 for i, letter in enumerate(state) if letter == "p"]

    def get_computer_locations(self,state=self.state):
        """Returns locations of all pieces owned by the computer"""
        return [i+1 for i, letter in enumerate(state) if letter == "c"]

    def get_all_open_spaces(self,state=self.state):
        """Returns locations of all pieces owned by the computer"""
        return [i+1 for i, letter in enumerate(state) if letter == "-"]


    def get_next_position_clockwise(self, loc, clockwise=True):
        """Get's the position clockwise to a point of the outer ring"""

        if(loc == 5): # The center can't be clockwise
            return None


        index = self.clockwise_list.index(loc)
        
        if(clockwise):
            if(index == 7):
                return self.clockwise_list[0]
            else:
                return self.clockwise_list[index+1]
        else:
            if(index == 0):
                return self.clockwise_list[7]
            else:
                return self.clockwise_list[index-1]

    def get_num_pieces_on_board(self, team, state=self.state):
        return state.count(team)

    def is_board_empty(self,state=self.state):
        """Determines if board is empty"""
        return state == "---------"
  
    def is_empty(self,loc, state=self.state):
        """Returns True if spot on board is empty"""
        return state[loc-1] == '-'

    def get_opposite_position(self, loc):
        """Return none for 5, the opposite location for the rest"""
        if(loc==5):
            return None
        for loc1, loc2 in self.opposites:
            if(loc1 == loc):
                return loc2
            elif(loc2==loc):
                return loc1
        