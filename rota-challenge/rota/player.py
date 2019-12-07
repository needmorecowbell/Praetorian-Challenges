import datetime

class Player(object):
    """The Player Object mimics the actions of a user who is intentionally trying to stall"""
    
    WON,LOST,IN_PROGRESS = range(3) # Enum for storing game state

    verbose = False
    game = None
    move_history=[]
    game_state= None

    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        self.game_state= self.IN_PROGRESS

    def _handle_placement(self):
        """Get the pieces on the board, correctly set up."""
        pass

    def _stall_game(self):
        """After all pieces are on the board, stall the game for 30 moves"""
        pass

    def _find_available_spaces(self, piece):
        """Finds the available spaces for a piece"""
        pass

    def _place(self,loc):
        """Place piece and record history"""
        results= self.game.place(loc)
        self.move_history.append(results["board"])

    def _move(self,piece,loc):
        """Place piece and record history"""
        results= self.game.move(piece,loc)
        self.move_history.append(results["board"])


    def dump_game_stats(self):
        """Dump the information about the current game and history about the player's session"""
    
        return {"move_history":self.dump_move_history(),
                "stats": self.game.dump_game_stats(),
                "results":self.game_state,
                "timestamp": datetime.datetime.now()}

    def play(self):
        """Emulate the game being played"""

        # Placement Stage
        self._handle_placement()
        # Stalling Stage
        self._stall_game()
