import pytest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from rota import Rota, Player, RotaAPI


@pytest.fixture(scope="module")
def mock_email():
    return "testing@tester.com"

@pytest.fixture(scope="module")
def game(mock_email):
    return Rota(mock_email)


@pytest.fixture(scope="module")
def player(game):
    return Player(game)

@pytest.fixture(scope="module")
def api(mock_email):
    return RotaAPI(mock_email)
    
