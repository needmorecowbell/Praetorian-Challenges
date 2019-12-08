import datetime


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

        for i in range(2):  # reactively handle the next two placements

            # Find game ending threat locations
            threat_locations = self._find_game_ending_threats()
            # There will only ever been one possible threat location this early
            # in the game because of our opening strategy

            if(len(threat_locations)> 1):
                print("[FATAL] We're at the end of the line, jim. I guess this is it.")
            if(len(threat_locations) > 0):
                print("[Player] Game ending threat found, mitigating...")
                self._place(threat_locations[0])

                if(self.verbose):
                    print(self.game.display_board_minimal())
                
                if(self.game.is_game_lost):
                    self.game_resolution= self.LOST
                    
            else:
                print("No immediate threats found")

                # No immediate threat found, find player's position and move to the opposite side of their piece
                #print("CPU: ", self._get_computer_locations())
                #print("player: ", self._get_player_locations())

    def _opening_move(self):
        """Place the player's first piece on the board"""

        if(self._is_board_empty()):  # We make the first move
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
            cpu_loc = self._get_computer_locations()[0]

            if(cpu_loc == 5):
                print("Computer picked the center as first move...")
                results = self._place(2)  # place the piece at the top
            else:
                print("Placing piece clockwise to opponent's...")
                results = self._place(
                    self._get_next_position_clockwise(cpu_loc))

            if(self.verbose):
                print(self.game.display_board_minimal())

    def _find_game_ending_threats(self):
        print("[Player] Finding threats...")

        threats = []

        # The middle is open, check if there is risk of losing if it is taken
        if(self.game.state[4] == '-'):
            if(self._is_threat_in_center()):
                # IE:
                #       - - p
                #       c - c
                #       - - -
                print("There is a threat in the center of the board...")
                threats.append(5)  # threat in center

            # if the center is open, there is a chance the border is at risk
            threats_on_border = self._find_threats_on_border()
            # IE:
            #       - - p
            #       - - c
            #       - - c
            if(len(threats_on_border) > 0):
                # There is a chance for 2 threats to come out of this function
                threats.extend(threats_on_border)
                print("There is a threat on the edge of the board")

        elif(self.game.state[4] == 'c'):
            threat_using_center = self._find_threat_using_center()
            if(threat_using_center):
                threats.append(threat_using_center)
                # IE:
                #       - - p
                #       - c c
                #       - - -
                print("There is a threat on the edge of the board, using the center")

        return threats

    def _is_threat_in_center(self):
        """Checks for threat occurring in the center of the board"""
        for loc1, loc2 in self.opposites:
            if(self.game.state[loc1-1] == 'c' and self.game.state[loc2-1] == 'c'):
                return True
        return False

    def _is_teammate_near(self, loc):
        """Returns True if a specific piece around the border has a similar piece next to it"""

        locPost = self._get_next_position_clockwise(loc)
        locPrior = self._get_next_position_clockwise(loc, clockwise=False)

        piece = self.game.state[loc-1]

        if(piece == '-'):
            print("[!] something is wrong, you're looking at an empty space")
            return False
        if(piece == self.game.state[locPost-1] or piece == self.game.state[locPrior-1]):
            return True

        return False

    def _is_empty(self, loc):
        """Returns True if spot on board is empty"""
        return self.game.state[loc-1] == '-'

    def _find_threat_using_center(self):
        """Checks for threat that uses the center piece"""

        # We already know that there is a piece in the center.
        # We need to check if there is another opponent piece on the edge, and
        # if that edge's opposite is empty if it is, the opposite spot is a threat
        for loc1, loc2 in self.opposites:
            if(self.game.state[loc1-1] == 'c' and self.game.state[loc2-1] == '-'):
                print("\t[!] Threat using center found at: ", loc2)
                return loc2
            if(self.game.state[loc1-1] == '-' and self.game.state[loc2-1] == 'c'):
                print("\t[!] Threat using center found at: ", loc1)
                return loc1

        return None

    def _find_threats_on_border(self):
        """Checks for threats that do not use the center, only on the border"""

        # We already know that there is not an opponent piece in the center
        # We need to check along the border for pairs of opponents.
        # if there is an empty space to the left and/or the right, record it
        threats = []
        for item in self.clockwise_list:
            loc1 = item
            loc2 = self._get_next_position_clockwise(loc1)
            loc3 = self._get_next_position_clockwise(loc2)

            loc1_piece = self.game.state[loc1-1]
            loc2_piece = self.game.state[loc2-1]
            loc3_piece = self.game.state[loc3-1]

            group = loc1_piece + loc2_piece + loc3_piece
            # print(group)

            # can't win when if there's a player piece in the set.
            if('p' not in group and group.count('c') == 2):
                print("\t[!] Threat on border")
                loc = group.find('-')

                if(loc == 0):
                    threats.append(loc1)
                elif(loc == 1):
                    threats.append(loc2)
                elif(loc == 2):
                    threats.append(loc3)

        return threats

    def _get_player_locations(self):
        """Returns locations of all pieces owned by the player"""
        return [i+1 for i, letter in enumerate(self.game.state) if letter == "p"]

    def _get_computer_locations(self):
        """Returns locations of all pieces owned by the computer"""
        return [i+1 for i, letter in enumerate(self.game.state) if letter == "c"]

    def _get_next_position_clockwise(self, loc, clockwise=True):
        """Get's the position clockwise to a point of the outer ring"""

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

    def _is_board_empty(self):
        """Determines if board is empty"""
        return self.game.state == "---------"

    def _stall_game(self):
        """After all pieces are on the board, stall the game for 30 moves"""
        pass

    def _find_available_spaces(self, piece):
        """Finds the available spaces for a piece"""
        available = []

        cclock_spot = self._get_next_position_clockwise(piece, clockwise=False)
        clock_spot = self._get_next_position_clockwise(piece)
        middle = self.game.state[4]

        if(self.game.state[cclock_spot-1] == '-'):
            available.append(cclock_spot)

        if(self.game.state[clock_spot-1] == '-'):
            available.append(clock_spot)
        if(middle == '-'):
            available.append(4)

        return available

    def _place(self, loc):
        """Place piece and record history"""
        results = self.game.place(loc)
        self.game.refresh_stats()
        self.move_history.append(results["data"]["board"])

    def _move(self, piece, loc):
        """Place piece and record history"""
        results = self.game.move(piece, loc)
        self.game.refresh_stats()
        self.move_history.append(results["data"]["board"])

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
