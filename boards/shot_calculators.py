from random import randrange

class ShotCalculator(object):
    def __init__(self, name):
        self.name = name

    # Calculator the next hit for a game
    def next_hit(self, game):
        raise NotImplementedError('ShotCalculator is abstract')

class RandomShotCalculator(ShotCalculator):
    def __init__(self):
        super().__init__('random')

    def next_hit(self, game):
        # just hit a random coordinate on a random board that hasn't been touched yet
        board_idx = randrange(0, len(game.boards))
        player = list(game.boards.keys())[board_idx]
        board = game.boards[player]
        # find all square without hit or miss
        coordinates = []
        for y in range(0, len(board)):
            for x in range(0, len(board[y])):
                if board[y][x] == '.':
                    coordinates.append((x+1,y+1))
        return player, coordinates[randrange(0, len(coordinates))]

class CosmoShotCalculator(ShotCalculator):
    def __init__(self):
        super().__init__('cosmo')

    def next_hit(self, game):
        pass
