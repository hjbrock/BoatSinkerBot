#!/usr/bin/python3

import sys
from boatsinker.bot import BoatBot
from boatsinker.logger import Logger

class CosmoBot(BoatBot):

    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')
        self.logger = Logger()
        self.hit_stack = []

    def _calculate_shot(self):
        player, targetting = self._pick_board()
        # calculate probability of all open squares having a boat
        board_counts = self._calculate_counts(player, self.game.boards[player])
        # hit the square with the highest count
        move = self._max_count(board_counts, targetting)
        return (player, move)

    def _pick_board(self):
        if len(self.hit_stack) > 0:
            targetting = True
            candidates = self.hit_stack
        else:
            targetting = False
            candidates = self.game.boards.keys()

        bestPlayer = ''
        minEmptyCells = (self.game.width * self.game.length) + 1
        for player in candidates:
            emptyCells = self.game.boards[player].count('.')
            if emptyCells < minEmptyCells:
                minEmptyCells = emptyCells
                bestPlayer = player

        return bestPlayer, targetting

    def _max_count(self, board_counts, targetting):
        max_count = -1
        i = 0
        # parity search - every other square if not targetting
        step = 2
        if targetting:
            step = 1
        for row in range(0, self.game.length):
            start = (row * self.game.width)
            end = start + self.game.width
            if not targetting:
                start = start + (row % 2)
            for ii in range(start, end, step):
                if board_counts[ii] > max_count:
                    i = ii
                    max_count = board_counts[ii]

        (x, y) = self.index_to_coordinate(i)
        return (x+1, y+1) # board index starts at 1

    def _calculate_counts(self, player, board):
        board_counts = [0 for x in range(0, len(board))]
        for boat in self.game.boats:
            size = int(boat[1:])
            # find all spots to put this boat and increment counts for those squares
            for i in range(0, len(board)):
                # loop by rows, alternate parity in each row
                (horizontal, hweight, vertical, vweight) = self._check_boat_location(board, i, size)
                if horizontal:
                    for ii in range(i, i + size):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + hweight
                if vertical:
                    for ii in range(i, i + (self.game.width*size), self.game.width):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + vweight
       
        self.logger.debug('Board:\n{0}\nCount:\n{1}'.format(self.print_board(board), self.print_board(board_counts)))
        return board_counts

    def _check_boat_location(self, board, i, size):
        if board[i] == '0':
            return (False, 1, False, 1)
        #check right and down
        horizontal = int((i + size - 1) / self.game.width) == int(i / self.game.width)
        vertical = int((i + ((size - 1) * self.game.width)) / self.game.width) < self.game.length
        hweight = 1
        vweight = 1
        if horizontal or vertical:
            for x in range(0, size):
                if horizontal:
                    if board[i + x] == '0':
                        horizontal = False
                    elif board[i + x] == 'X':
                        hweight = hweight + 5
                if vertical:
                    if board[i + (x * self.game.width)] == '0':
                        vertical = False
                    elif board[i + (x * self.game.width)] == 'X':
                        vweight = vweight + 5
                if not horizontal and not vertical:
                    break

        return (horizontal, hweight, vertical, vweight)

    def _hit(self, player, x, y):
        if player == self.bot_name:
            return
        self.hit_stack.append(player)

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
