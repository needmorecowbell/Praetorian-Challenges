import datetime
import time

class Player(object):
    """The Player Object mimics the actions of a user who is intentionally trying to stall"""

    WON, LOST, IN_PROGRESS = range(3)  # Enum for storing game state
    enum_game_resolution = ["WON", "LOST", "IN_PROGRESS"]

    verbose = False
    game = None
    move_history = []
    game_resolution = None

    clockwise_list = [2, 3, 6, 9, 8, 7, 4, 1]
   
    # spots opposite to each other
    opposites = [(2, 8), (3, 7), (6, 4), (9, 1)]

    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        self.game_resolution = self.IN_PROGRESS

    def _handle_placement(self):
        """Get the pieces on the board, correctly set up."""
        if(self.verbose):
            print(self.game.display_board_minimal())
        
        self._opening_move()  # put your first piece on the board
        root = self._get_player_locations(self.game.state)[0] # only player on board
        
        made_first_move = self._get_num_pieces_on_board(self.game.state, 'c') == 1

        expected_cwise = self._get_next_position_clockwise(self._get_opposite_position(root))
        expected_ccwise = self._get_next_position_clockwise(self._get_opposite_position(root),clockwise=False)

        #Fill in one of the forks where there is a threat if there is one (assuming player always moves right or left of first piece)
        if(made_first_move):
            loc= self._get_computer_locations(self.game.state)[0] # only one opponent on board
            self._place(self._get_opposite_position(loc)) # move player to the opposite position
            if(self.verbose):
                print("Made first move, second piece moving opposite of opponent")
                print(self.game.display_board_minimal())
                         

            if(self.game.state[expected_ccwise-1] =='-'):
                print("Filling in the y ccwise...")
                threats=self._find_threats_on_border(self.game.state)
                
                if(len(threats)>0):
                    print("attempting alternate y formation")
                    self._place(threats[0])
                else:
                    self._place(expected_ccwise)
                if(self.verbose):
                    print(self.game.display_board_minimal())    
            else:
                print("Filling in the y cwise...")
                threats=self._find_threats_on_border(self.game.state)
                
                if(len(threats)>0):
                    print("attempting alternate y formation")
                    self._place(threats[0])
                else:
                    self._place(expected_cwise)
                if(self.verbose):
                    print(self.game.display_board_minimal())      


        else:
            threats= self._find_game_ending_threats(self.game.state)

            if(len(threats)>0):
                print("Fixing immediate threat upon placement")
                self._place(threats[0])
                if(self.verbose):
                    print(self.game.display_board_minimal())      

                threats = self._find_game_ending_threats(self.game.state)
                if(len(threats) > 0):
                    self._place(threats[0])
                    if(self.verbose):
                        print(self.game.display_board_minimal())    
                else: # otherwise, let's fill out the y formation
                    if(self.game.state[expected_ccwise-1]=='-'):
                        self._place(expected_ccwise)
                        if(self.verbose):
                            print(self.game.display_board_minimal())      

                    elif(self.game.state[expected_cwise-1]=='-'):
                        self._place(expected_cwise)
                        if(self.verbose):
                            print(self.game.display_board_minimal())      

                    else:
                        threats = self._find_game_ending_threats(self.game.state)
                        if(len(threats) > 0):
                            self._place(threats[0])
                            if(self.verbose):
                                print(self.game.display_board_minimal()) 
                        else: 
                            a_locs= self._get_all_open_spaces(self.game.state)
                            for loc in a_locs:
                                state= self._mock_place(self.game.state, loc)
                                if(self._is_in_y_position(state, "p")):
                                    print(f"Placing at {loc} to fill out the Y shape.")
                                    self._place(loc)
                                    if(self.verbose):
                                        print(self.game.display_board_minimal()) 



            else: # no threats found
                
                if(self.game.state[expected_ccwise-1] =="-"):
                    print("No threat, moving ccwise")
                    self._place(expected_ccwise)
                    if(self.verbose):
                        print(self.game.display_board_minimal())      

                elif(self.game.state[expected_cwise-1]=="-"):
                    print("No threat, moving cwise")
                    self._place(expected_cwise)
                    if(self.verbose):
                        print(self.game.display_board_minimal())     

                else:
                    print("both slots are filled, don't know what to do") 
                    exit()

                # Work on third piece

                threats = self._find_game_ending_threats(self.game.state)
                if(len(threats) > 0):
                    self._place(threats[0])
                    if(self.verbose):
                        print(self.game.display_board_minimal())  
                else:
                    if(self.game.state[expected_ccwise-1]=='-'):
                        self._place(expected_ccwise)
                        if(self.verbose):
                            print(self.game.display_board_minimal())      

                    elif(self.game.state[expected_cwise-1]=='-'):
                        self._place(expected_cwise)
                        if(self.verbose):
                            print(self.game.display_board_minimal()) 
                    else:
                        a_locs= self._get_all_open_spaces(self.game.state)
                        for loc in a_locs:
                            state= self._mock_place(self.game.state, loc)
                            if(self._is_in_y_position(state, "p")):
                                print(f"Placing at {loc} to fill out the Y shape.")
                                self._place(loc)
                                if(self.verbose):
                                    print(self.game.display_board_minimal()) 



            
        if(self.game.state[4]=='p'):
            print("Not in Y formation, all pieces are placed")
            a_locs= self._find_available_spaces(self.game.state, 5)
            for loc in a_locs:
                state = self._mock_move(self.game.state, 5,loc)
                if(self._is_in_y_position(state, "p")):
                    print("Moving center to fill out the Y shape.")
                    self._move(5,loc)
                    if(self.verbose):
                        print(self.game.display_board_minimal()) 

        if(self._is_in_y_position(self.game.state,"p")):
            print("Success, pieces are in formation for stalling")
        else:
            print("[ERROR] Something went wrong")   
            exit()

            

        # for i in range(2):  # reactively handle the next two placements
        #     # Find game ending threat locations
        #     threat_locations = self._find_game_ending_threats(self.game.state)
        #     # There will only ever been one possible threat location this early
        #     # in the game because of our opening strategy

        #     if(len(threat_locations)> 1):
        #         print("[FATAL] We're at the end of the line, jim. I guess this is it.")
        #     if(len(threat_locations) > 0):
        #         print("[Player] Game ending threat found, mitigating...")
        #         self._place(threat_locations[0])

        #         if(self.verbose):
        #             print(self.game.display_board_minimal())
                
        #         if(self.game.is_game_lost):
        #             self.game_resolution= self.LOST
                    
        #     else:
        #         print("\t[+] No immediate threats found")
                
        #         #Place at the opposite end of one of the opponents
        #         cp_locs = self._get_computer_locations(self.game.state)
        #         piece_placed = False

        #         for loc in cp_locs:

        #             if(loc!=5):
        #                 opp_loc= self._get_opposite_position(loc)
        #                 if(self._is_empty(self.game.state,opp_loc) and not self._is_piece_near(loc, piece_type='p')): 
        #                     # location is empty and not near a teammate
        #                     print("[Player] Placing piece opposite of opponent in loc: ", loc)
        #                     results= self._place(opp_loc)
        #                     piece_placed=True

        #                     if(self.verbose):
        #                         print(self.game.display_board_minimal())

        #                     break # if we place an item, restart the logic to detect for new threats
                
        #         if(not piece_placed): # if all opposite places are taken or near a teammate...
        #             for loc in self.clockwise_list:
        #                 if(self._is_empty(self.game.state,loc) and not self._is_piece_near(loc,piece_type='p')):
        #                     print("[Player] No opposite corners found, placing in open area away from teammates...")
        #                     results = self._place(loc)

        #                     if(self.verbose):
        #                         print(self.game.display_board_minimal())

        #                     break


    def _opening_move(self):
        """Place the player's first piece on the board"""

        if(self._is_board_empty(self.game.state)):  # We make the first move
            if(self.verbose):
                print("[Player] Placing piece on open board...")
          
            results = self._place(2)  # Place the piece in the top spot

            if(self.verbose):
                print(self.game.display_board_minimal())

        else:  # If first move has been made by the player, move to the right of the player
            self.move_history.append(self.game.state)
            if(self.verbose):
                print("[Player] Placing first piece, reactive...")

            # There's only one to look for
            cpu_loc = self._get_computer_locations(self.game.state)[0]

            if(cpu_loc == 5):
                print("Computer picked the center as first move...")
                results = self._place(2)  # place the piece at the top
            else:
                print("Placing piece clockwise to opponent's...")
                results = self._place(
                    self._get_next_position_clockwise(cpu_loc))

            if(self.verbose):
                print(self.game.display_board_minimal())

    def _is_in_y_position(self,state,team):
        """Determines if player or opponent are in the y position on the board"""

        for loc in self.clockwise_list:
            expected_cwise = self._get_next_position_clockwise(self._get_opposite_position(loc))
            expected_ccwise = self._get_next_position_clockwise(self._get_opposite_position(loc),clockwise=False)
            if(state[expected_ccwise-1] == team and state[loc-1] == team and state[expected_cwise-1] == team):
                #If all are team members, it must be a y formation
                return True
        return False
        
    def _find_game_ending_threats(self,state):
        print("[Player] Finding threats...")

        threats = []

        # The middle is open, check if there is risk of losing if it is taken
        if(state[4] == '-'):
            if(self._is_threat_in_center(state)):
                # IE:
                #       - - p  or  p - p  or  c - p
                #       c - c      c - c      p - c
                #       - - -      - c p      - - c
                print("[Threat] There is a threat in the center of the board...")
                threats.append(5)  # threat in center

            # if the center is open, there is a chance the border is at risk
            threats_on_border = self._find_threats_on_border(state)
            # IE:
            #       - - p
            #       - - c
            #       - - c
            if(len(threats_on_border) > 0):
                # There is a chance for 2 threats to come out of this function
                threats.extend(threats_on_border)
                print("[Threat] There is a threat on the edge of the board")

        elif(state[4] == 'c'):
            threat_using_center = self._find_threats_using_center(state)
            if(threat_using_center):
                threats.extend(threat_using_center)
                # IE:
                #       - - p
                #       - c c
                #       - - -
                print("[Threat] There is a threat on the edge of the board, using the center")

        return threats

    def _is_threat_in_center(self,state):
        """Checks for threat occurring in the center of the board"""
        
        # we already know that the center is empty
        # Because all pieces can move to this spot, there is no need for a placement mode, it's handled
        # the same.

        for loc1, loc2 in self.opposites:
            if(state[loc1-1] == 'c' and state[loc2-1] == 'c'):
                return True
        return False

    def _is_piece_near(self, loc, piece_type):
        """Returns True if a location around the border has a similar piece next to it"""

        locPost = self._get_next_position_clockwise(loc)
        locPrior = self._get_next_position_clockwise(loc, clockwise=False)

        #loc_piece = self.game.state[loc-1]

        if(piece_type == self.game.state[locPost-1] or piece_type == self.game.state[locPrior-1]):
            return True

        return False


    def _find_threats_using_center(self, state):
        """Checks for threat that uses the center piece"""

        # We already know that there is a piece in the center.
        # We need to check if there is another opponent piece on the edge, and
        # if that edge's opposite is empty if it is, the opposite spot is a threat
        
        threats=[]
        for loc1, loc2 in self.opposites:
            if(state[loc1-1] == 'c' and state[loc2-1] == '-'):
                if(self._get_num_pieces_on_board(self.game.state,"c") <3):
                    print("\t[!] Threat using center found at: ", loc2)
                    threats.append(loc2)

                else:
                    # We need to check that the threat actually can be moved to by another piece
                    for cloc in self._get_computer_locations(self.game.state):
                        if(cloc not in [loc1, 5]):
                            if(loc2 in self._find_available_spaces(self.game.state,cloc)):
                                threats.append(loc2) # There is an opponent that can move

            if(state[loc1-1] == '-' and state[loc2-1] == 'c'):
                if(self._get_num_pieces_on_board(self.game.state,"c") <3):
                    print("\t[!] Threat using center found at: ", loc1)
                    threats.append(loc1)
                else:
                    for cloc in self._get_computer_locations(self.game.state):
                        if(cloc not in [loc2,5]):
                            if(loc1 in self._find_available_spaces(self.game.state,cloc)):
                                threats.append(loc1)

        return threats

    def _find_threats_on_border(self, state):
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
            loc2 = self._get_next_position_clockwise(loc1)
            loc3 = self._get_next_position_clockwise(loc2)

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
                    print(self.game.state)
                    if(self._get_num_pieces_on_board(state,"c") <3):
                        print("\t[!] Threat on border")
                        threats.append(threat) #this is definitely a threat if there is only 2 pieces on the board
                    else:
                        for cloc in self._get_computer_locations(state):
                            if(cloc not in [loc1,loc2,loc3]):
                                if(threat in self._find_available_spaces(state,cloc)):
                                    print(f"\t[!] Threat on border [{cloc} moves to {threat}]")
                                    threats.append(threat)


        return list(set(threats))

    def _stall_game(self):
        """After all pieces are on the board, stall the game for 30 moves"""

        # Remove our piece from the middle if it's there

        print("[Player] All pieces are placed, time to stall...")
        while(self.game.is_active):
            threats= self._find_game_ending_threats(self.game.state) 
            
            if(len(threats)>0): # if there is an immediate threat to take care of...
                
                print("[Player] Possible threats: ", threats)
                player_moved=False

                for player_loc in self._get_player_locations(self.game.state):
                    available_spaces= self._find_available_spaces(self.game.state,player_loc)

                    if(threats[0] in available_spaces): # if our player has the option of defending against the threat
                        future_state = self._mock_move(self.game.state, player_loc, threats[0])
                        future_threats= self._find_game_ending_threats(future_state)
                        print("Future threats: ",future_threats)
                        print("Location: ",player_loc)

                        if(len(future_threats)== 0): # this move won't cause us to lose
                            self._move(player_loc, threats[0])
                            player_moved=True
                            print('\t[+] Moved player from center to: ',player_loc)

                            if(self.verbose):
                                print(self.game.display_board_minimal())
                            break # we made our move, break out
                
                if(not player_moved):
                    
                    print("Couldn't fix the threat")
                    time.sleep(2)
                    for player_loc in self._get_player_locations(self.game.state):
                        available_spaces = self._find_available_spaces(self.game.state,player_loc)
                        if(5 in available_spaces and self._is_empty(self.game.state,5)):
                            future_state = self._mock_move(self.game.state, player_loc, 5)
                            future_threats = self._find_game_ending_threats(future_state)
                            print("Future Threat: "+future_threats)
                            print(f"Moving player [{player_loc}] to center")
                            if(len(future_threats) == 0): # this move won't cause us to lose
                                self._move(player_loc, 5)
                                player_moved = True
                                print(f'\t[+] Moved player [{player_loc}] to center')

                                if(self.verbose):
                                    print(self.game.display_board_minimal())

                                break # we made our move, break out
        


            elif(self.game.state[4] == 'p'):
                print("[Player] piece is in center, attempting to move away")
                available_locs = self._find_available_spaces(self.game.state,5) #find all available locations for a piece in the center
                print("Available spaces: ",available_locs)
                center_moved= False
                for loc in available_locs:
                    if(not self._is_piece_near(loc,'p')): #If spot is not near another player piece.
                        future_state = self._mock_move(self.game.state, 5, loc)
                        future_threats= self._find_game_ending_threats(future_state)
                        

                        if(len(future_threats)==0):
                            results= self._move(5, loc)
                            centerMoved= True
                            print('\t[+] Moved player from center to: ',loc)

                            if(self.verbose):
                                print(self.game.display_board_minimal())
                            break # we made our move, break out
                
                if(not center_moved): # If we can't move the center because of threats, move a border piece
                    player_moved=False
                    for player_loc in self._get_player_locations(self.game.state):

                        available_spaces = self._find_available_spaces(self.game.state,player_loc)

                        for aloc in available_spaces:
                            future_state = self._mock_move(self.game.state, player_loc, aloc)
                            future_threats = self._find_game_ending_threats(future_state)

                            if(len(future_threats) == 0): # this move won't cause us to lose
                                self._move(player_loc, aloc)
                                player_moved = True
                                print(f'\t[+] Moved player [{player_loc}] to: {aloc}')

                                if(self.verbose):
                                    print(self.game.display_board_minimal())

                                break # we made our move, break out

                        if(player_moved):
                            break # player has moved, exit          

            else:
                print("[Player] No threats and piece is not in the center")
                # if no threat is found, then let's make sure our move won't cause one
                for player_loc in self._get_player_locations(self.game.state): 
                        available_spaces = self._find_available_spaces(self.game.state,player_loc)
                        for aloc in available_spaces:
                            future_state = self._mock_move(self.game.state, player_loc, aloc)
                            future_threats = self._find_game_ending_threats(future_state)

                            if(len(future_threats) == 0): # this move won't cause us to lose
                                self._move(player_loc, aloc)
                                print(f'\t[+] Moved player [{player_loc}] to: {aloc}')

                                if(self.verbose):
                                    print(self.game.display_board_minimal())
                                break

    def _mock_move(self, state, piece, loc):
        """Returns a game state of a move without sending it to the server"""
        future_state = state[0:piece-1]+'-'+state[piece:] # sub out piece to empty space
        future_state = future_state[0:loc-1]+'p'+future_state[loc:]
        return future_state

    def _mock_place(self, state, loc):
        """ Returns a game state of a placement without sending it to the server"""
        future_state = state[0:loc-1]+'p'+state[loc:]
        return future_state

    def _find_available_spaces(self, state, piece):
        """Finds the available spaces for a piece"""
        available = []

        if(piece !=5):
            cclock_spot = self._get_next_position_clockwise(piece, clockwise=False)
            clock_spot = self._get_next_position_clockwise(piece)
            middle = state[4]

            if(state[cclock_spot-1] == '-'):
                available.append(cclock_spot)

            if(state[clock_spot-1] == '-'):
                available.append(clock_spot)
            if(middle == '-'):
                available.append(5)
        else:
            for loc in self.clockwise_list:
                if(self._is_empty(state,loc)):
                    available.append(loc)

        return available

    def _place(self, loc):
        """Place piece and record history"""
        results = self.game.place(loc)
        self.game.refresh_stats()
        print(results["data"])
        self.move_history.append(results["data"]["board"])
        if(self.game.is_game_lost):
            self.game_resolution= self.LOST

    def _move(self, piece, loc):
        """Place piece and record history"""
        results = self.game.move(piece, loc)
        self.game.refresh_stats()
        self.move_history.append(results["data"]["board"])
        if(self.game.is_game_lost):
            self.game_resolution= self.LOST

    def _get_player_locations(self,state):
        """Returns locations of all pieces owned by the player"""
        return [i+1 for i, letter in enumerate(state) if letter == "p"]

    def _get_computer_locations(self,state):
        """Returns locations of all pieces owned by the computer"""
        return [i+1 for i, letter in enumerate(state) if letter == "c"]

    def _get_all_open_spaces(self,state):
        """Returns locations of all pieces owned by the computer"""
        return [i+1 for i, letter in enumerate(state) if letter == "-"]


    def _get_next_position_clockwise(self, loc, clockwise=True):
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

    def _get_num_pieces_on_board(self, state,team):
        return state.count(team)

    def _is_board_empty(self,state):
        """Determines if board is empty"""
        return state == "---------"
  
    def _is_empty(self,state, loc):
        """Returns True if spot on board is empty"""
        return state[loc-1] == '-'

    def _get_opposite_position(self, loc):
        """Return none for 5, the opposite location for the rest"""
        if(loc==5):
            return None
        for loc1, loc2 in self.opposites:
            if(loc1 == loc):
                return loc2
            elif(loc2==loc):
                return loc1
        

    def dump_game_stats(self):
        """Dump the information about the current game and history about the player's session"""

        return {"move_history": self.move_history,
                "stats": self.game.dump_stats(),
                "results": self.enum_game_resolution[self.game_resolution],
                "timestamp": str(datetime.datetime.now())}

    def play(self):
        """Emulate the game being played"""

        # Placement Stage
        self._handle_placement()
        # Stalling Stage
        #self._stall_game()
