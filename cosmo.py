import sys
from boatsinker.bot import BoatBot

class CosmoBot(BoatBot):
    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')
        self._move_stack = [] # moves = (player, x, y)

    def _calculate_shot(self):
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
        i = 0
        for (board_player, board_counts) in counts:
            for ii in range(0, len(board_counts)):
                if board_counts[i] > max_count:
                    player = board_player
                    i = ii
                    max_count = board_counts[yy][xx]

        x, y = self.index_to_coordinate(i)
        return (player, (x+1, y+1)) # board index starts at 1

    def _calculate_counts(self, board):
        board_counts = [0 for x in range(0, self.game.width*self.game.length)]
        for boat in self.game.boats:
            size = int(boat[1:])
            # find all spots to put this boat and increment counts for those squares
            for i in range(0, len(board_counts)):
                x, y = self.index_to_coordinate(i) 
                (horizontal, vertical) = self._check_boat_location(board, x, y, size)
                if horizontal:
                    for ii in range(i, i + size):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
                if vertical:
                    for ii in range(ii, ii + (self.game.width*size), self.game.width):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
        
        return board_counts

    def _check_boat_location(self, board, x, y, size):
        if board[self.coordinate_to_index(x,y)] == '0':
            return (False, False)
        #check right and down
        horizontal = True
        vertical = True
        for pos in range(0, size):
            if horizontal and (((x + pos) >= self.game.width) or (board[self.coordinate_to_index(x+pos, y)] == '0')):
                horizontal = False
            if vertical and (((y + pos) >= self.game.length) or (board[self.coordinate_to_index(x, y+pos)] == '0')):
                vertical = False
            if not horizontal and not vertical:
                break

        return (horizontal, vertical)

    def _hit(self, player, x, y):
        if player == self.bot_name:
            return
        to_check = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for (x,y) in to_check:
            if (y < self.game.length and y >= 0) and (x >= 0 and x < self.game.width):
                self._move_stack.append((player, x, y))

    def _generate_board(self):
        # create board with all boats on the outside
        board = ['.' for x in range(0, self.game.width*self.game.length)]
        for boat in self.game.boats:
            (lastx, lasty) = (-1, 0)
            letter = boat[0:1]
            size = int(boat[1:])
            placed = False
            while not placed:
                (x, y) = (lastx + 1, lasty)
                if y >= self.game.length:
                    break
                if (x + size) < self.game.length:
                    placed = True
                    for xx in range(x, x + size):
                        board[self.coordinate_to_index(xx, y)] = letter
                    (lastx, lasty) = (x + size, lasty)
                else:
                    # go to bottom row
                    (lastx, lasty) = (-1, lasty + self.game.length - 1)

            (lastx, lasty) = (0, 1)
            while not placed:
                (x, y) = (lastx, lasty + 1)
                if x >= self.game.width:
                    break
                if (y + size) < self.game.length - 1:
                    placed = True
                    for yy in range(y, y + size):
                        board[self.coordinate_to_index(x, yy)] = letter
                    (lastx, lasty) = (lastx, y + size)
                else:
                    # go to right column
                    (lastx, lasty) = (lastx + self.game.width - 1, 1)

        return board

# Cosmo boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    cosmo = CosmoBot(host, port)
    cosmo.run()
