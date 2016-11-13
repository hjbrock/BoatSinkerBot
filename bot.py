import traceback
from communication.listener import BoatsinkerListener
from communication import incoming_messages as inc
from communication import outgoing_messages as out
from boards.game import Game
from boards import shot_calculators as shots

# Bot base class
class BoatBot(BoatsinkerListener):
    def __init__(self, host, port, shot_calculator, bot_name):
        super().__init__(host, port)
        self.shot_calculator = shot_calculator
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

    def _handle(self, msg):
        #print('Received message: ' + msg)
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

    def _game_info(self, gameMsg):
        if self.game is None:
            print('Server version: {0}, Board width: {1}, Board length: {2}'.format(gameMsg.version, str(gameMsg.width), str(gameMsg.length)))
            self.game_info = gameMsg
            self.send(out.JoinMessage(self.bot_name, self._default_board()))
            self.game = Game(self.bot_name)
            print('Joined game')

    def _board_change(self, boardMsg):
        if self.game is not None:
            self.game.update_board(boardMsg.player, boardMsg.board)

    def _turn(self, turnMsg):
        if turnMsg.player == self.bot_name and self.game is not None:
            (player, (x, y)) = self.shot_calculator.next_hit(self.game)
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

    def _default_board(self):
        board = [['.' for x in range(self.game_info.width)] for y in range(self.game_info.length)]
        for x in range(5):
            board[0][x] = 'A'
        
        for y in range(4):
            board[y+2][0] = 'B'

        for x in range(2):
            board[0][x+8] = 'E'

        for x in range(3):
            board[9][x+1] = 'C'

        for y in range(3):
            board[y+4][9] = 'D'
        
        return board


