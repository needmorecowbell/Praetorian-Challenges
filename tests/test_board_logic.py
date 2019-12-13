def test_is_board_empty(game):
    states= [("c----p--c",False),("---------",True)]
    for state,expectation in states:
        assert expectation == game.is_board_empty(state=state)

def test_get_num_pieces_on_board(game):
    states= [("c----p--c","c",2),("c----p--c","p",1), ("---------","p",0),
             ("---------","c",0) ,("-pccc--pp","p",3),("-pccc--pp","c",3)]
    for state, team, expectation in states:
        assert expectation == game.get_num_pieces_on_board(team, state=state)

def test_get_next_position_clockwise(game):
    clockwise_list = [(2,3), (3,6), (6,9), (9,8), (8,7), (7,4), (4,1), (1,2),(5,None)]
    for position, expected in clockwise_list:
        assert expected == game.get_next_position_clockwise(position)

def test_get_player_locations(game):
    states= [("c----p--c",[6]),("c----pp-c",[6,7]),("---------",[]),('--c-p-c--',[5])]
    for state, expectation in states:
        assert expectation == game.get_player_locations(state=state)

def test_get_computer_locations(game):
    states= [("c----p--c",[1,9]),("c---ccp-p",[1,5,6]), ("---------",[]),('--c-p-c--',[3,7])]
    for state, expectation in states:
        assert expectation == game.get_computer_locations(state=state)

def test_mock_move(game):
    states= [("c-cp-pp-c",6,5,"c-cpp-p-c"),
             ("c-cp-pp-c",7,8,"c-cp-p-pc"),
             ("-pc-c-pcp",2,1,"p-c-c-pcp") ]
    for state, piece, loc, expectation in states:
        assert expectation == game.mock_move(piece,loc,state=state)


def test_mock_place(game):
    states= [("---------",2,"-p-------") ,
             ("c----p--p",8,"c----p-pp")]
    for state, loc, expectation in states:
        assert expectation == game.mock_place(loc, state=state)


def test_is_in_y_position(game):
    states= [("-pcc-pp-c","p",True),("-pcc-pp-c","c",True),("-pc-c-pcp","p",True),("-pc-c-pcp","c",False)]
    for state, team, expectation in states:
        assert expectation == game.is_in_y_position(team,state=state)

def test_find_available_spaces(game):
    states = [("cpp-c-pc-",2,[]), ("cpp-c-pc-",3,[6]), ("cpp-c-pc-",7,[4])]

    for state, piece, expected in states:
        assert expected == game.find_available_spaces(piece, state=state)