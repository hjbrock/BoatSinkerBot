# Cosmo boat bot
import sys
import traceback
from communication import listener
from communication import incoming_messages as inc
from communication import outgoing_messages as out

class Cosmo(listener.BoatsinkerListener):
    def __init__(self, host, port):
        super().__init__(host, port)

    def run(self):
        self.connect()

        try:
            msgs = self.receive()
            for msg in msgs:
                if not msg or msg == '':
                    print('Empty message received, shutting down')
                    break
                self._handle(msg)
            print('No more messages, exiting')
        except:
            traceback.print_exc()
            print('Error reading from socket, shutting down')
            self.close()

    def _handle(self, msg):
        print('Received message: ' + msg)
        first = msg[0]
        if first is 'B':
            self._board_change(inc.BoardMessage(msg))
        elif first is 'N':
            self._turn(inc.TurnMessage(msg))
        elif first is 'F':
            self._finish(inc.FinishedMessage(msg))
        elif first is 'R':
            self._score(inc.ScoreMessage(msg))
        elif first is 'G':
            self._game_info(inc.GameInfoMessage(msg))
        else:
            print('Ignoring message: ' + msg)

    def _game_info(self, gameMsg):
        self.game_info = gameMsg
        self.send(out.JoinMessage('cosmo', self._default_board()))

    def _board_change(self, boardMsg):
        #TODO
        pass

    def _turn(self, turnMsg):
        #TODO
        pass

    def _finish(self, finishMsg):
        #TODO
        pass

    def _score(self, scoreMsg):
        #TODO
        pass

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

if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print('Usage: ' + sys.argv[0] + ' server_host server_port')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    cosmo = Cosmo(host, port)
    cosmo.run()
