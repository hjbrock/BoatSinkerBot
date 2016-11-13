import traceback
from random import randrange
from communication.listener import BoatsinkerListener
from communication import incoming_messages as inc
from communication import outgoing_messages as out
from boards.game import Game
from boards import shot_calculators as shots

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

    def calculate_shot(self):
        raise NotImplementedError('BoatBot is abstract')

    def _hit(self, hitMsg):
        raise NotImplementedError('BoatBot is abstract')

    def _handle(self, msg):
        first = msg[0]
        if first is 'B':
            if self.game_info is not None:
                self._board_change(inc.BoardMessage(msg, self.game_info.width, self.game_info.length))
        elif first is 'N':
            self._turn(inc.TurnMessage(msg))
        elif first is 'F':
            self._finish(inc.FinishedMessage(msg))
        elif first is 'R':
            self._score(inc.ScoreMessage(msg))
        elif first is 'G':
            self._game_info(inc.GameInfoMessage(msg))
        elif first is 'H':
            self._hit(inc.HitMessage(msg))

    def _game_info(self, gameMsg):
        if self.game is None:
            print('Server version: {0}, Board width: {1}, Board length: {2}'.format(gameMsg.version, str(gameMsg.width), str(gameMsg.length)))
            self.game_info = gameMsg
            board = self._generate_board()
            self.send(out.JoinMessage(self.bot_name, self._generate_board()))
            self.game = Game(self.bot_name)
            print('Joined game with board:')
            self._print_board(board)

    def _board_change(self, boardMsg):
        if self.game is not None:
            self.game.update_board(boardMsg.player, boardMsg.board)

    def _turn(self, turnMsg):
        if turnMsg.player == self.bot_name and self.game is not None:
            (player, (x, y)) = self.calculate_shot()
            self.send(out.ShootMessage(player, x, y))

    def _finish(self, finishMsg):
        print('Game finished')
        self.num_scores = finishMsg.players

    def _score(self, scoreMsg):
        print('Player: {0}, Score: {1}'.format(scoreMsg.player, scoreMsg.score))
        self.game.update_score(scoreMsg.player, scoreMsg.score)
        self.num_scores = self.num_scores - 1
        if self.num_scores is 0:
            print('Winner(s): {0}'.format(str(self.game.winner())))
            self.game = None

    def _generate_board(self):
        board = [['.' for x in range(0, self.game_info.width)] for y in range(0, self.game_info.length)]
        for boat in self.game_info.boats:
            letter = boat[0:1]
            size = int(boat[1:])
            # find all spots to put this boat, then pick a random spot
            # format: x|y|direction
            locations = []
            for y in range(0, len(board)):
                for x in range(0, len(board[y])):
                    (horizontal, vertical) = self._check_location(board, x, y, size)
                    if horizontal:
                        locations.append((x, y, 'horizontal'))
                    if vertical:
                        locations.append((x, y, 'vertical'))

            (x, y, direction) = locations[randrange(0, len(locations))]
            if direction == 'horizontal':
                for xx in range(x, x + size):
                    board[y][xx] = letter
            elif direction == 'vertical':
                for yy in range(y, y + size):
                    board[yy][x] = letter

        return board
    
    def _check_location(self, board, x, y, size):
        if board[y][x] != '.':
            return (False, False)
        #check right and down
        horizontal = True
        vertical = True
        for pos in range(0, size):
            if horizontal and (((x + pos) >= len(board[y])) or (board[y][x+pos] != '.')):
                horizontal = False
            if vertical and (((y + pos) >= len(board)) or (board[y+pos][x] != '.')):
                vertical = False
            if not horizontal and not vertical:
                break

        return (horizontal, vertical)
    
    def _print_board(self, board):
        board_str = ''
        for row in board:
            for cell in row:
                board_str = board_str + str(cell) + ' '
            board_str = board_str + '\n'
        
        print(board_str)

