def test_is_board_empty(player):
    states= [("c----p--c",False),("---------",True)]
    for state,expectation in states:
        assert expectation == player._is_board_empty(state)

def test_get_num_pieces_on_board(player):
    states= [("c----p--c","c",2),("---------","p",0)]
    for state, team, expectation in states:
        assert expectation == player._get_num_pieces_on_board(state,team)
