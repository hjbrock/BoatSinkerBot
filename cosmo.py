import sys
from boatsinker.bot import BoatBot
from boatsinker.logger import Logger

class CosmoBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')

    def _calculate_shot(self):
        # calculate probability of all open squares having a boat
        board_counts = [(player, self._calculate_counts(board)) for (player, board) in self.game.boards.items()]
        # hit the square with the highest count
        return self._max_count(board_counts)

    def _max_count(self, counts):
        max_count = -1
        player = list(self.game.boards.keys())[0]
        i = 0
        for (board_player, board_counts) in counts:
            for ii in range(0, len(board_counts)):
                if board_counts[ii] > max_count:
                    player = board_player
                    i = ii
                    max_count = board_counts[ii]

        x, y = self.index_to_coordinate(i)
        return (player, (x+1, y+1)) # board index starts at 1

    def _calculate_counts(self, board):
        board_counts = [0 for x in range(0, len(board))]

        for boat in self.game.boats:
            size = int(boat[1:])
            # find all spots to put this boat and increment counts for those squares
            for i in range(0, len(board)):
                (horizontal, vertical) = self._check_boat_location(board, i, size)
                if horizontal:
                    for ii in range(i, i + size):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
                if vertical:
                    for ii in range(i, i + (self.game.width*size), self.game.width):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
       
        return board_counts

    def _check_boat_location(self, board, i, size):
        if board[i] == '0':
            return (False, False)
        #check right and down
        horizontal = int((i + size - 1) / self.game.width) == int(i / self.game.width)
        vertical = int((i + ((size - 1) * self.game.width)) / self.game.width) < self.game.length
        if horizontal or vertical:
            for x in range(0, size):
                if horizontal and board[i + x] == '0':
                    horizontal = False
                if vertical and board[i + (x * self.game.width)] == '0':
                    vertical = False
                if not horizontal and not vertical:
                    break

        return (horizontal, vertical)

    def _hit(self, player, x, y):
        #if player == self.bot_name:
        #    return
        #to_check = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        #for (x,y) in to_check:
        #    if (y < self.game.length and y >= 0) and (x >= 0 and x < self.game.width):
        #        self._move_stack.append((player, x, y))
        pass

    def _generate_board(self):
        # TODO make smarter
        return self.random_board()

# Cosmo boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port [-v|s]')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    debug = len(sys.argv) > 3 and sys.argv[3] == '-v'
    silent = len(sys.argv) > 3 and sys.argv[3] == '-s'

    cosmo = CosmoBot(host, port)
    if debug:
        Logger().loglevel = Logger.DEBUG
    elif silent:
        Logger().loglevel = Logger.SILENT
    else:
        Logger().loglevel = Logger.INFO

    cosmo.run()
