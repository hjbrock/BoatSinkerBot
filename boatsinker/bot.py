import traceback
from random import randrange
from boatsinker.listener import BoatsinkerListener
from boatsinker.game import Game

# Bot base class
class BoatBot(BoatsinkerListener):
    def __init__(self, host, port, bot_name):
        super().__init__(host, port)
        self.bot_name = bot_name
        self.game = None
        self.num_scores = 0

    def run(self):
        try:
            self.connect()
            self.send('G') # make sure we get the game info
            msgs = self.receive()
            for msg in msgs:
                if not msg or msg == '':
                    print('Empty message received, leaving game')
                    break
                self._handle(msg)
        except:
            traceback.print_exc()
            print('Error reading from socket, shutting down')
        finally:
            self.close()

    def _calculate_shot(self):
        raise NotImplementedError('BoatBot is abstract')

    def _generate_board(self):
        raise NotImplementedError('BoatBot is abstract')

    def _hit(self, player, x, y):
        raise NotImplementedError('BoatBot is abstract')

    def _handle(self, msg):
        parts = msg.split('|')
        first = parts[0]
        if first is 'B':
            self._board_change(parts)
        elif first is 'N':
            self._turn(parts)
        elif first is 'F':
            self._finish(parts)
        elif first is 'R':
            self._score(parts)
        elif first is 'G':
            self._game_info(parts)
        elif first is 'H':
            player = parts[1]
            x = ord(parts[3][0]) - ord('a')
            y = int(parts[3][1:])
            self._hit(player, x, y)

    def _game_info(self, parts):
        if self.game is None:
            width = int(parts[8])
            length = int(parts[9])
            num_boats = int(parts[10])
            if len(parts) < (11 + num_boats):
                raise Exception('Not enough boat descriptors')
            boats = []
            for boat in range(num_boats):
                boats.append(parts[11 + boat])
            self.game = Game(self.bot_name, width, length, boats)
            board = self._generate_board()
            self.send('J|{0}|{1}'.format(self.bot_name, board))
            print('Joined game with board:')
            self.print_board(board)

    def _board_change(self, parts):
        if self.game is not None:
            player = parts[1]
            board = parts[3]
            self.game.update_board(player, board)

    def _turn(self, parts):
        if parts[1] == self.bot_name and self.game is not None:
            (player, (x, y)) = self._calculate_shot()
            self.send('S|{0}|{1}|{2}'.format(player, x, y))

    def _finish(self, parts):
        self.num_scores = int(parts[3])

    def _score(self, parts):
        player = parts[1]
        score = int(parts[2])
        self.game.update_score(player, score)
        self.num_scores = self.num_scores - 1
        if self.num_scores is 0:
            print('Winner(s): {0}'.format(str(self.game.winner())))
            self.game = None

    def index_to_coordinate(self, index):
        x = int(index % self.game.width)
        y = int(index / self.game.width)
        return x, y

    def coordinate_to_index(self, x, y):
        return int((y * self.game.width) + x)

    def print_board(self, board):
        for y in range(0, self.game.length):
            row = board[y*self.game.width:(y+1)*self.game.width]
            print(' '.join(row))
        
