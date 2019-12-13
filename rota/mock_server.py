from rota import Player as game
class MockServer():
    game=None

    def __init__(self, game):
        self.game=game
