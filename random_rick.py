import sys
from bot import BoatBot
from random import randrange

# Random bot - just picks random untouched cell
class RandomRickBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, 'rick')

    def calculate_shot(self):
        # just hit a random coordinate on a random board that hasn't been touched yet
        board_idx = randrange(0, len(self.game.boards))
        player = list(self.game.boards.keys())[board_idx]
        board = self.game.boards[player]
        # find all square without hit or miss
        coordinates = []
        for y in range(0, len(board)):
            for x in range(0, len(board[y])):
                if board[y][x] == '.':
                    coordinates.append((x+1,y+1))

        return player, coordinates[randrange(0, len(coordinates))]  

    def _hit(self, hitMsg):
        pass

# RandomRick boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    rick = RandomRickBot(host, port)
    rick.run()
