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
        board = ['.' for x in range(0, self.game.width*self.game.length)]
        for boat in self.game.boats:
            letter = boat[0:1]
            size = int(boat[1:])
            # find all spots to put this boat, then pick a random spot
            # format: x|y|direction
            locations = []
            for i in range(0, len(board)):
                (horizontal, vertical) = self._check_location(board, i, size)
                if horizontal:
                    locations.append((i, 'horizontal'))
                if vertical:
                    locations.append((i, 'vertical'))

            (i, direction) = locations[randrange(0, len(locations))]
            if direction == 'horizontal':
                for xx in range(i, i + size):
                    board[xx] = letter
            elif direction == 'vertical':
                for yy in range(i, i + (self.game.width*size), self.game.width):
                    board[yy] = letter

        return ''.join(board)
    
    def _check_location(self, board, i, size):
        if board[i] != '.':
            return (False, False)
        #check right and down
        horizontal = True
        vertical = True
        x, y = self.index_to_coordinate(i)
        for pos in range(0, size):
            if horizontal and (((x + pos) >= self.game.width) or (board[self.coordinate_to_index(x+pos, y)] != '.')):
                horizontal = False
            if vertical and (((y + pos) >= self.game.length) or (board[self.coordinate_to_index(x, y+pos)] != '.')):
                vertical = False
            if not horizontal and not vertical:
                break

        return (horizontal, vertical)

# RandomRick boat bot main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    rick = RandomRickBot(host, port)
    rick.run()
