
def test_find_gaming_ending_threats_threat_in_center(player):
    states= ["c----p--c"]
    for state in states:
        results = player._find_game_ending_threats(state)
        assert 5 in results
        assert len(results) == 1

def test_is_threat_in_center(player):
    states= ["c----p--c", "c-cp-pc-p","c-c--pp-c"]
    for state in states:
        results = player._is_threat_in_center(state)
        assert results == True

def test_is_threat_on_border_placement_mode(player):
    """Tests for border threats where not all the pieces are on the board"""
    states= [("cc-p-cp--",[3]),("cc-p-----",[3])]
    for state, expectation in states:
        results = player._find_threats_on_border(state)
        assert expectation == results
    
def test_is_threat_on_border(player):
    """Tests for border threats where all the pieces are on the board"""
    states= [("cc--pcp-p",[3]),("cc-p--pcp",[])]

    for state, expectation in states:
        results = player._find_threats_on_border(state)
        assert expectation == results

