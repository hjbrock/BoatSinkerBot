#!/usr/bin/python3

import sys
from boatsinker.bot import BoatBot
from boatsinker.logger import Logger

class CosmoBot(BoatBot):

    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')
        self.logger = Logger()
        self.move_stack = {}

    def _calculate_shot(self):
        player = self._pick_board()
        # calculate probability of all open squares having a boat
        board_counts = self._calculate_counts(player, self.game.boards[player])
        # check if we're targetting
        if player in self.move_stack:
            moves = self.move_stack[player]
            while len(moves) > 0:
                move = moves.pop()
                if board_counts[move] > 0:
                    (x,y) = self.index_to_coordinate(move)
                    self.logger.debug('Using stack move {0}'.format(move))
                    return (player, (x+1,y+1))
                else:
                    self.logger.debug('Move {0} has 0 count'.format(move))
        else:
            self.logger.debug('Player {0} is not in move stack'.format(player))
        # hit the square with the highest count otherwise
        return (player, self._max_count(board_counts))

    def _pick_board(self):
        if len(self.game.boards) == 1:
            return list(self.game.boards.keys())[0]

        bestPlayer = ''
        minEmptyCells = (self.game.width * self.game.length) + 1
        for (player, board) in self.game.boards.items():
            emptyCells = board.count('.')
            if emptyCells < minEmptyCells:
                minEmptyCells = emptyCells
                bestPlayer = player

        return player

    def _max_count(self, board_counts):
        max_count = -1
        i = 0
        # parity search - every other square
        #for ii in range(0, len(board_counts)):
        for row in range(0, self.game.length):
            start = (row * self.game.width) + (row % 2)
            end = start + self.game.width
            self.logger.debug('Start:{0} End:{1}'.format(start, end))
            for ii in range(start, end, 2):
                if board_counts[ii] > max_count:
                    i = ii
                    max_count = board_counts[ii]

        x, y = self.index_to_coordinate(i)
        return (x+1, y+1) # board index starts at 1

    def _calculate_counts(self, player, board):
        board_counts = [0 for x in range(0, len(board))]
        for boat in self.game.boats:
            size = int(boat[1:])
            # find all spots to put this boat and increment counts for those squares
            for i in range(0, len(board)):
                # loop by rows, alternate parity in each row
                (horizontal, vertical) = self._check_boat_location(board, i, size)
                if horizontal:
                    for ii in range(i, i + size):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
                if vertical:
                    for ii in range(i, i + (self.game.width*size), self.game.width):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + 1
       
        self.logger.debug('Board:\n{0}\nCount:\n{1}'.format(self.print_board(board), self.print_board(board_counts)))
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
        self.logger.debug('Hit at ({0},{1})'.format(x, y))
        if player == self.bot_name:
            return
        if player not in self.move_stack:
            self.move_stack[player] = []        
        moves = self.move_stack[player]
        if (x + 1) < self.game.width:
            moves.append(self.coordinate_to_index(x + 1, y))
        if (x - 1) >= 0:
            moves.append(self.coordinate_to_index(x - 1, y))
        if (y + 1) < self.game.length:
            moves.append(self.coordinate_to_index(x, y + 1))
        if (y - 1) >= 0:
            moves.append(self.coordinate_to_index(x, y - 1))
        self.logger.debug('Added moves to stack:{0}'.format(moves))

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
