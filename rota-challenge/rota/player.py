class Player(object):
    """The Player Object mimics the actions of a user who is intentionally trying to stall"""

    verbose = False
    game = None

    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose

    def _handle_placement(self):
        """Get the pieces on the board, correctly set up."""
        pass

    def _stall_game(self):
        """After all pieces are on the board, stall the game for 30 moves"""
        pass

    def _find_available_spaces(self, piece):
        """Finds the available spaces for a piece"""
        pass

    def play(self):
        """Emulate the game being played"""

        # Placement Stage
        self._handle_placement()
        # Stalling Stage
        self._stall_game()
