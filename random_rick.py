import sys
from boatsinker.bot import BoatBot
from random import randrange

# Random bot - just picks random untouched cell
class RandomRickBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, 'rick')

    def _calculate_shot(self):
        # just hit a random coordinate on a random board that hasn't been touched yet
        board_idx = randrange(0, len(self.game.boards))
        player = list(self.game.boards.keys())[board_idx]
        board = self.game.boards[player]
        # find all square without hit or miss
        idxs = []
        for i in range(0, len(board)):
            if board[i] == '.':
                idxs.append(i)

        x, y = self.index_to_coordinate(idxs[randrange(0, len(idxs))])
        return player, (x+1, y+1)  

    def _hit(self, player, x, y):
        pass

    def _generate_board(self):
        return self.random_board()

# RandomRick boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    rick = RandomRickBot(host, port)
    rick.run()
