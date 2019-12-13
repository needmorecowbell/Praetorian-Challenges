
def test_find_gaming_ending_threats_threat_in_center(game):
    states= ["c----p--c"]
    for state in states:
        results = game.find_game_ending_threats(state=state)
        assert 5 in results
        assert len(results) == 1

def test_is_threat_in_center(game):
    states= ["c----p--c", "c-cp-pc-p","c-c--pp-c"]
    for state in states:
        results = game.is_threat_in_center(state=state)
        assert results == True

def test_find_threats_using_center(game):
    states= [("c--pcppc-",[2,9]),("c-ppc--cp",[2]),("p-c-c-pcp",[2])]
    for state, expectation in states:
        results = game.find_threats_using_center(state=state)
        assert expectation == results

def test_is_threat_on_border_placement_mode(game):
    """Tests for border threats where not all the pieces are on the board"""
    states= [("cc-p-cp--",[3]),("cc-p-----",[3])]
    for state, expectation in states:
        results = game.find_threats_on_border(state=state)
        assert expectation == results
    
def test_is_threat_on_border(game):
    """Tests for border threats where all the pieces are on the board"""
    states= [("cc--pcp-p",[3]),("cc-p--pcp",[]),("cp-------",[])]
# cc-
# -pc
# p-p
    for state, expectation in states:
        results = game.find_threats_on_border(state=state)
        assert expectation == results

