import sys
from bot import BoatBot
from boards import shot_calculators as shots

class CosmoBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')
        self._move_stack = [] # moves = (player, x, y)

    def calculate_shot(self):
        # use move stack if we have it
#        while len(self._move_stack) is not 0:
#            (player, x, y) = self._move_stack.pop()
#            board = self.game.boards[player]
#            if board[y][x] == '.':
#                return player, (x+1, y+1)

        # calculate probability of all open squares having a boat
        board_counts = [(player, self._calculate_counts(board)) for (player, board) in self.game.boards.items()]
        # hit the square with the highest count
        return self._max_count(board_counts)

    def _max_count(self, counts):
        max_count = -1
        player = list(self.game.boards.keys())[0]
        x = 0
        y = 0
        for (board_player, board_counts) in counts:
            for yy in range(0, len(board_counts)):
                for xx in range(0, len(board_counts[yy])):
                    if board_counts[yy][xx] > max_count:
                        player = board_player
                        x = xx
                        y = yy
                        max_count = board_counts[yy][xx]

        return (player, (x+1, y+1)) # board index starts at 1

    def _calculate_counts(self, board):
        board_counts = [[0 for x in range(0, self.game_info.width)] for y in range(0, self.game_info.length)]
        for boat in self.game_info.boats:
            size = int(boat[1:])
            # find all spots to put this boat and increment counts for those squares
            for y in range(0, len(board)):
                for x in range(0, len(board[y])):
                    (horizontal, vertical) = self._check_boat_location(board, x, y, size)
                    if horizontal:
                        for xx in range(x, x + size):
                            if board[y][xx] == '.':
                                board_counts[y][xx] = board_counts[y][xx] + 1
                    if vertical:
                        for yy in range(y, y + size):
                            if board[yy][x] == '.':
                                board_counts[yy][x] = board_counts[yy][x] + 1
        
        return board_counts

    def _check_boat_location(self, board, x, y, size):
        if board[y][x] == '0':
            return (False, False)
        #check right and down
        horizontal = True
        vertical = True
        for pos in range(0, size):
            if horizontal and (((x + pos) >= len(board[y])) or (board[y][x+pos] == '0')):
                horizontal = False
            if vertical and (((y + pos) >= len(board)) or (board[y+pos][x] == '0')):
                vertical = False
            if not horizontal and not vertical:
                break

        return (horizontal, vertical)

    def _hit(self, hitMsg):
        if hitMsg.player == self.bot_name:
            return
        board = self.game.boards[hitMsg.player]
        to_check = [(hitMsg.x+1, hitMsg.y), (hitMsg.x-1, hitMsg.y), (hitMsg.x, hitMsg.y+1), (hitMsg.x, hitMsg.y-1)]
        for (x,y) in to_check:
            if (y < len(board) and y >= 0) and (x >= 0 and x < len(board[y])):
                self._move_stack.append((hitMsg.player, x, y))

# Cosmo boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    cosmo = CosmoBot(host, port)
    cosmo.run()
