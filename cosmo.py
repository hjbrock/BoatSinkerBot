#!/usr/bin/python3

import sys
from boatsinker.bot import BoatBot
from boatsinker.logger import Logger

class CosmoBot(BoatBot):

    def __init__(self, host, port):
        super().__init__(host, port, 'cosmo')
        self.logger = Logger()

    def _calculate_shot(self):
        highest_count = -1
        best_move = (0, 0)
        best_player = ''
        best_empty_cells = (self.game.width * self.game.length) + 1

        for player, board in self.game.boards.items():
            if board.count('X') >= self.game.hits_per_board:
                continue
            empty_cells = board.count('.')
            if empty_cells == 0:
                continue
            boats = self._eliminate_boats(board)
            if len(boats) == 0: # we screwed up 
                boats = list(self.game.boats.values())
            board_counts, targetting = self._calculate_counts(player, board, boats)
            count, move = self._max_count(board_counts, targetting, self.game.min_boat_size)
            if (count > highest_count) or (count == highest_count and empty_cells < best_empty_cells):
                highest_count = count
                best_move = move
                best_empty_cells = empty_cells
                best_player = player

        return (best_player, best_move)

    def _max_count(self, board_counts, targetting, min_boat_size):
        max_count = -1
        i = 0
        # parity search - every other square if not targetting
        step = min_boat_size
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
        
        self.logger.debug('Max count:{0} Index:{1}'.format(max_count, i))
        (x, y) = self.index_to_coordinate(i)
        return max_count, (x+1, y+1) # board index starts at 1

    def _calculate_counts(self, player, board, boats):
        board_counts = [0 for x in range(0, len(board))]
        targetting = False #set to true if we have possible boat positions through a hit
        for size in boats:
            # find all spots to put this boat and increment counts for those squares
            for i in range(0, len(board)):
                # loop by rows, alternate parity in each row
                (horizontal, hweight, vertical, vweight) = self._check_boat_location(board, i, size)
                if vweight > 1 or hweight > 1:
                    targetting = True
                if horizontal:
                    for ii in range(i, i + size):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + hweight
                if vertical:
                    for ii in range(i, i + (self.game.width*size), self.game.width):
                        if board[ii] == '.':
                            board_counts[ii] = board_counts[ii] + vweight
       
        str_board = self.print_board(board)
        str_counts = self.print_board(board_counts)
        self.logger.debug('Board:\n{0}\nCount:\n{1}'.format(str_board, str_counts))
        return board_counts, targetting

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

    def _eliminate_boats(self, board):
        boats = list(self.game.boats.values())
        boats.sort()
        # remove boats surrounded by misses from possible boat list
        length = 0
        for x in range(0, self.game.width):
            if length in boats:
                boats.remove(length)
            length = 0
            for y in range(0, self.game.length):
                i = self.coordinate_to_index(x, y) 
                if board[i] != 'X' or not self._adjacent_misses(i, board, 'vertical'):
                    length = 0
                else:
                    length = length + 1

        length = 0
        for y in range(0, self.game.length):
            if length in boats:
                boats.remove(length)
            length = 0
            for x in range(0, self.game.width):
                i = self.coordinate_to_index(x, y)
                if board[i] != 'X' or not self._adjacent_misses(i, board, 'horizontal'):
                    length = 0
                else:
                    length = length + 1

        return boats

    def _hit(self, player, x, y):
        pass

    def get_placements(self, board, size):
        self.logger.debug('In cosmo get_placements')
        locations = []
        firstRow = self.coordinate_to_index(0, 0)
        lastRow = self.coordinate_to_index(0, self.game.length-1)
        lastRowEnd = self.game.width * self.game.length
        lastColumn = self.coordinate_to_index(self.game.width-1, 0)
        
        for i in range(firstRow, lastColumn + 1):
            horizontal, vertical = self.check_boat_placement(board, i, size)
            if horizontal:
                locations.append((i, 'horizontal'))
        for i in range(lastRow, lastRowEnd):
            horizontal, vertical = self.check_boat_placement(board, i, size)
            if horizontal:
                locations.append((i, 'horizontal'))
        for i in range(firstRow, lastRow + 1, self.game.width):
            horizontal, vertical = self.check_boat_placement(board, i, size)
            if vertical:
                locations.append((i, 'vertical'))
        for i in range(lastColumn, lastRowEnd, self.game.width):
            horizontal, vertical = self.check_boat_placement(board, i, size)
            if vertical:
                locations.append((i, 'vertical'))

        if len(locations) == 0:
            for i in range(0, len(board)):
                (horizontal, vertical) = self.check_boat_placement(board, i, size)
                if horizontal:
                    locations.append((i, 'horizontal'))
                if vertical:
                    locations.append((i, 'vertical'))

        return locations
    
    def check_boat_placement(self, board, i, size):
        if board[i] != '.':
            return (False, False)
        # check right and down
        horizontal = int((i + size - 1) / self.game.width) == int(i / self.game.width)
        vertical = int((i + ((size - 1) * self.game.width)) / self.game.width) < self.game.length
        x, y = self.index_to_coordinate(i)
        for pos in range(0, size):
            horiz_idx = self.coordinate_to_index(x+pos, y)
            if horizontal and ((board[horiz_idx] != '.') or self._adjacent_boat(horiz_idx, board)):
                horizontal = False
            vert_idx = self.coordinate_to_index(x, y+pos)
            if vertical and ((board[vert_idx] != '.') or self._adjacent_boat(vert_idx, board)):
                vertical = False
            if not horizontal and not vertical:
                break

        return (horizontal, vertical)

    def _adjacent_idx(self, i, board, exclude_right = False, exclude_below = False):
        above = i - self.game.width
        below = i + self.game.width
        right = i + 1
        left = i - 1
        idx = []
        if above >= 0:
            idx.append(above)
        if (not exclude_below) and below < (self.game.length * self.game.width):
            idx.append(below)
        if (not exclude_right) and int(right/self.game.width) == int(i/self.game.width):
            idx.append(right)
        if int(left/self.game.width) == int(i/self.game.width):
            idx.append(left)
        return idx

    def _adjacent_misses(self, i, board, direction):
        if direction == 'horizontal':
            adj = self._adjacent_idx(i, board, True, False)
        else:
            adj = self._adjacent_idx(i, board, False, True)
        for idx in adj:
            if board[idx] != '0':
                return False

        return True

    def _adjacent_boat(self, i, board):
        idx = self._adjacent_idx(i, board)
        for ii in idx:
            if board[ii] != '.':
                return True
        
        return False

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
