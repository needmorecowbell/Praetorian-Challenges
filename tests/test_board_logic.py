def test_is_board_empty(player):
    states= [("c----p--c",False),("---------",True)]
    for state,expectation in states:
        assert expectation == player._is_board_empty(state)

def test_get_num_pieces_on_board(player):
    states= [("c----p--c","c",2),("c----p--c","p",1), ("---------","p",0),
             ("---------","c",0) ,("-pccc--pp","p",3),("-pccc--pp","c",3)]
    for state, team, expectation in states:
        assert expectation == player._get_num_pieces_on_board(state,team)

def test_get_next_position_clockwise(player):
    clockwise_list = [(2,3), (3,6), (6,9), (9,8), (8,7), (7,4), (4,1), (1,2),(5,None)]
    for position, expected in clockwise_list:
        assert expected == player._get_next_position_clockwise(position)

def test_get_player_locations(player):
    states= [("c----p--c",[6]),("c----pp-c",[6,7]),("---------",[]),('--c-p-c--',[5])]
    for state, expectation in states:
        assert expectation == player._get_player_locations(state)

def test_get_computer_locations(player):
    states= [("c----p--c",[1,9]),("c---ccp-p",[1,5,6]), ("---------",[]),('--c-p-c--',[3,7])]
    for state, expectation in states:
        assert expectation == player._get_computer_locations(state)

def test_mock_move(player):
    states= [("c-cp-pp-c",6,5,"c-cpp-p-c"),
             ("c-cp-pp-c",7,8,"c-cp-p-pc") ]
    for state, piece, loc, expectation in states:
        assert expectation == player._mock_move(state,piece,loc)

def test_is_in_y_position(player):
    states= [("-pcc-pp-c","p",True),("-pcc-pp-c","c",True),("-pc-c-pcp","p",True),("-pc-c-pcp","c",False)]
    for state, team, expectation in states:
        assert expectation == player._is_in_y_position(state,team)

def test_find_available_spaces(player):
    states = [("cpp-c-pc-",2,[]), ("cpp-c-pc-",3,[6]), ("cpp-c-pc-",7,[4])]

    for state, piece, expected in states:
        assert expected == player._find_available_spaces(state,piece)