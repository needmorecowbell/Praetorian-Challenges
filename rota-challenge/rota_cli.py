from rota import Rota, Player
import argparse
from pprint import pprint


def forced(email, verbose=False):
    game = Rota(email, verbose)
    player = Player(game, verbose)  # give the player a game to play
    player.play()


def interactive(email, verbose=False):
    game = Rota(email)  # initialize a game connection attached to email
    game_in_progress = True

    while (game_in_progress):

        if(verbose):
            print(game.display_board())
        else:
            print(game.display_board_minimal())

        decision = input("\n(e)xit game, (p)lace piece, (m)ove piece: ")
        if(decision is 'e'):  # exit
            game_in_progress = False  # end game

        elif(decision is 'p'):  # place
            print("Possible locations to place a piece: ")
            location = input("place the piece where: ")
            result = game.place(location)

        elif(decision is 'm'):
            print("Possible Moves: ")
            piece = input("Which piece to move: ")
            location = input("Where to move piece: ")
            result = game.move(piece, location)

        try:
            if("must be empty" in result['data']["location"]):
                print("Error: Space must be empty")
        except KeyError as e:
            pass

        try:
            # There are multiple reason a query may fail..handle them here
            if(result["status"] == "fail"):
                print("Query Failed")
                pprint(result)
                # timeout check
                if("Active game not available" in result["data"]["request"] and game.is_active):
                    choice = input(
                        "Game is inactive, new game? press y to continue: ")
                    if(choice is 'y'):
                        game = Rota(args.email)  # make a new board
                    else:
                        game_in_progress = False
        except KeyError as e:
            pass

        game.refresh_stats()  # Get the latest stats from the api


if __name__ == "__main__":
    art = '''
                   *** ### ### ***
               *##        O        ##* 
           *##            |            ##*
        *##               |               ##*
      *##                 |                 ##*
    *##  O                |                O  ##*
   *##      \             |             /      ##*
  *##           \         |         /           ##*
 *##               \      |      /               ##*
 *##                  \   |   /                  ##*
 *## O--------------------O--------------------O ##*
 *##                  /   |   \                  ##*
 *##               /      |      \              ##*
  *##           /         |         \           ##*
   *##      /             |             \      ##*
    *##  O                |                O  ##*
      *##                 |                 ##*
        *#                |               ##*
           *##            |            ##*
               *##        O        ##*
                   *** ### ### ***
    '''
    print(art+"\n\t\t  Welcome to Rota\n")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
   
    parser.add_argument('-f', "--force",
                        help="stall game to win every time",  action="store_true")
    
    parser.add_argument("email", help="email to attach to game")

    args = parser.parse_args()

    if(args.force):
        if(args.verbose):
            print("Attempting win by stalling a Rota opponent to submission 50 times in a row...")
        forced(args.email, args.verbose)

    else:
        if(args.verbose):
            print("Starting game in interactive mode...")
        interactive(args.email, args.verbose)
