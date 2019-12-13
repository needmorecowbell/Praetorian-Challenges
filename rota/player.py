import datetime
import time
import pdb

class Player(object):
    """The Player Object mimics the actions of a user who is intentionally trying to stall"""

    WON, LOST, IN_PROGRESS = range(3)  # Enum for storing game state
    enum_game_resolution = ["WON", "LOST", "IN_PROGRESS"]

    verbose = False
    game = None
    move_history = []
    game_resolution = None



    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        self.game_resolution = self.IN_PROGRESS

    def _handle_placement(self):
        """Get the pieces on the board, correctly set up. This isn't very pretty."""
        if(self.verbose):
            print(self.game.display_board_minimal())
        
        self._opening_move()  # put your first piece on the board
        root = self.game.get_player_locations()[0] # only player on board
        
        made_first_move = self.game.get_num_pieces_on_board('c') == 1

        expected_cwise = self.game.get_next_position_clockwise(self.game.get_opposite_position(root))
        expected_ccwise = self.game.get_next_position_clockwise(self.game.get_opposite_position(root),clockwise=False)

        #Fill in one of the forks where there is a threat if there is one (assuming player always moves right or left of first piece)
        if(made_first_move):
            loc= self.game.get_computer_locations()[0] # only one opponent on board
            self._place(self.game.get_opposite_position(loc)) # move player to the opposite position
            if(self.verbose):
                print("Made first move, second piece moving opposite of opponent")
                print(self.game.display_board_minimal())
                         

            if(self.game.state[expected_ccwise-1] =='-'):
                print("Filling in the y ccwise...")
                threats=self.game.find_threats_on_border()
                
                if(len(threats)>0):
                    print("attempting alternate y formation")
                    self._place(threats[0])
                else:
                    self._place(expected_ccwise)
                if(self.verbose):
                    print(self.game.display_board_minimal())    
            else:
                print("Filling in the y cwise...")
                threats=self.game.find_threats_on_border()
                
                if(len(threats)>0):
                    print("attempting alternate y formation")
                    self._place(threats[0])
                else:
                    self._place(expected_cwise)
                if(self.verbose):
                    print(self.game.display_board_minimal())      


        else:
            threats= self.game.find_game_ending_threats()

            if(len(threats)>0):
                print("Fixing immediate threat upon placement")
                self._place(threats[0])
                if(self.verbose):
                    print(self.game.display_board_minimal())      

                threats = self.game.find_game_ending_threats()
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
                        threats = self.game.find_game_ending_threats()
                        if(len(threats) > 0):
                            self._place(threats[0])
                            if(self.verbose):
                                print(self.game.display_board_minimal()) 
                        else: 
                            a_locs= self.game.get_all_open_spaces()
                            for loc in a_locs:
                                future_state= self.game.mock_place(loc)
                                if(self.game.is_in_y_position("p", state=future_state)):
                                    print(f"Placing at {loc} to fill out the Y shape.")
                                    self._place(loc)
                                    if(self.verbose):
                                        print(self.game.display_board_minimal()) 

            else: # no threats found
                
                if(self.game.state[expected_ccwise-1] == "-"):
                    print("No threat, moving ccwise")
                    self._place(expected_ccwise)
                    if(self.verbose):
                        print(self.game.display_board_minimal())      

                elif(self.game.state[expected_cwise-1]== "-"):
                    print("No threat, moving cwise")
                    self._place(expected_cwise)
                    if(self.verbose):
                        print(self.game.display_board_minimal())     

                # Work on third piece

                threats = self.game.find_game_ending_threats()
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
                        a_locs= self.game.get_all_open_spaces()
                        for loc in a_locs:
                            future_state= self.game.mock_place(loc)
                            if(self.game.is_in_y_position("p", state=future_state)):
                                print(f"Placing at {loc} to fill out the Y shape.")
                                self._place(loc)
                                if(self.verbose):
                                    print(self.game.display_board_minimal()) 


            
        if(self.game.state[4]=='p'):
            print("Not in Y formation, all pieces are placed")
            a_locs= self.game.find_available_spaces(5)
            for loc in a_locs:
                future_state = self.game.mock_move(5,loc, state=future_state)
                if(self.game.is_in_y_position( "p")):
                    print("Moving center to fill out the Y shape.")
                    self._move(5,loc)
                    if(self.verbose):
                        print(self.game.display_board_minimal()) 

        if(self.game.is_in_y_position("p")):
            print("Success, pieces are in formation for stalling")
        else:
            print("[ERROR] Something went wrong")   
            exit()

    def _opening_move(self):
        """Place the player's first piece on the board"""

        if(self.game.is_board_empty()):  # We make the first move
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
            cpu_loc = self.game.get_computer_locations()[0]

            if(cpu_loc == 5):
                print("Computer picked the center as first move...")
                results = self._place(2)  # place the piece at the top
            else:
                print("Placing piece clockwise to opponent's...")
                results = self._place(
                    self.game.get_next_position_clockwise(cpu_loc))

            if(self.verbose):
                print(self.game.display_board_minimal())

   
    def _stall_game(self):
        """After all pieces are on the board, stall the game for 30 moves"""

        # Remove our piece from the middle if it's there

        print("[Player] Pieces are placed and in formation, time to stall...")
        while(self.game.is_active):
            if(self.game.is_threat_in_center()):
                while(self.game.is_active and self.game.is_threat_in_center()):
                    print("Threat is in center, stalling by moving back and forth")

                    for piece in self.game.get_player_locations():
                        a_locs = self.game.find_available_spaces(piece)
                        if(len(a_locs) == 3): # Find the piece with 3 available spaces
                            #and move it back and forth from the center
                            self._move(piece, 5) 
                            if(self.verbose):
                                print("Moved open piece to center")
                                print(self.game.display_board_minimal())
                            

                            self._move(5,piece)
                            if(self.verbose):
                                print("Moved piece back from center")
                                print(self.game.display_board_minimal())
                            
                            break # We made our double shift, break out to check for threat again
            
            elif(self.game.state[4]=="c"): # if piece is in center
                while(self.game.is_active and self.game.state[4]=='c'):
                    
                    for piece in self.game.get_player_locations():
                        cwise_loc= self.game.get_next_position_clockwise(piece)
                        ccwise_loc= self.game.get_next_position_clockwise(piece, clockwise=False)
                        a_locs = self.game.find_available_spaces(piece)

                        if(cwise_loc in a_locs): # if the clockwise space is open, see if we can move there
                            future_state= self.game.mock_move(piece, cwise_loc)
                            
                            future_threats= self.game.find_game_ending_threats(state=future_state)

                            if(len(future_threats) == 0):
                                self._move(piece,cwise_loc)
                                if(self.verbose):
                                    print("Moved piece clockwise from border")
                                    print(self.game.display_board_minimal())

                                    if(self.game.state[piece-1]=='-'):
                                        future_state= self.game.mock_move(cwise_loc, piece)
                                        future_threats = self.game.find_game_ending_threats(state=future_state)
                                        
                                        if(len(future_threats) == 0):
                                            self._move(cwise_loc, piece)
                                            if(self.verbose):
                                                print("Moved piece back to old position")
                                                print(self.game.display_board_minimal())  
                                        break

                        elif(ccwise_loc in a_locs):
                            future_state= self.game.mock_move(self.game.state, piece, ccwise_loc)
                            future_threats = self.game.find_game_ending_threats(state=future_state)

                            if(len(future_threats) == 0):
                                self._move(piece,ccwise_loc)
                                if(self.verbose):
                                    print("Moved piece counterclockwise from border")
                                    print(self.game.display_board_minimal())                            
                                
                                if(self.game.state[piece-1]=='-'):
                                    future_state= self.game.mock_move(cwise_loc, piece)
                                    future_threats= self.game.find_game_ending_threats(future_state)
                                    
                                    if(len(future_threats)==0):
                                        self._move(ccwise_loc, piece)
                                        if(self.verbose):
                                            print("Moved piece back to old position")
                                            print(self.game.display_board_minimal())  
                                    break
                                                                  

            elif(self.game.state[4]=='-'):
                for piece in self.game.get_player_locations():
                    a_locs= self.game.find_available_spaces( piece)
                    if(len(a_locs)>1):
                        cwise_loc= self.game.get_next_position_clockwise(piece)
                        ccwise_loc= self.game.get_next_position_clockwise(piece, clockwise=False)

                        if(cwise_loc in a_locs): # if the clockwise space is open, see if we can move there
                            future_state= self.game.mock_move( piece, cwise_loc)
                            future_threats= self.game.find_game_ending_threats(state=future_state)
                            if(len(future_threats)==0):
                                self._move(piece,cwise_loc)
                                if(self.verbose):
                                    print("Moved piece clockwise from border")
                                    print(self.game.display_board_minimal())

                                if(self.game.state[piece-1]=='-'):
                                    future_state= self.game.mock_move(cwise_loc, piece)
                                    future_threats= self.game.find_game_ending_threats(state=future_state)
                                    
                                    if(len(future_threats)==0):
                                        self._move(cwise_loc, piece)
                                        if(self.verbose):
                                            print("Moved piece back to old position")
                                            print(self.game.display_board_minimal())  
                                    break

                        elif(ccwise_loc in a_locs):
                            future_state= self.game.mock_move(piece, ccwise_loc)
                            future_threats= self.game.find_game_ending_threats(state=future_state)
                            if(len(future_threats)==0):
                                self._move(piece,ccwise_loc)
                                if(self.verbose):
                                    print("Moved piece counterclockwise from borderrrr")
                                    print(self.game.display_board_minimal())                            
                                
                                if(self.game.state[piece-1]=='-'):
                                    future_state= self.game.mock_move(cwise_loc, piece)
                                    future_threats= self.game.find_game_ending_threats(state=future_state)
                                    
                                    if(len(future_threats)==0):
                                        self._move(ccwise_loc, piece)
                                        if(self.verbose):
                                            print("Moved piece back to old position")
                                            print(self.game.display_board_minimal())  
                                    break
            else:
                print("Not yet supported")
                exit()
            
            time.sleep(.5)
  

    def _place(self, loc):
        """Place piece and record history"""
        results = self.game.place(loc)
        self.game.refresh_stats()
        self.move_history.append(results["data"]["board"])
        if(self.game.is_game_lost):
            self.game_resolution= self.LOST

    def _move(self, piece, loc):
        """Place piece and record history"""
        results = self.game.move(piece, loc)
        self.game.refresh_stats()
        print(results["data"])
        self.move_history.append(results["data"]["board"])
        if(self.game.is_game_lost):
            self.game_resolution= self.LOST

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
        self._stall_game()
