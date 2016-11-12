# Message definitions for boat clients

class IncomingMessage(object):
    def __init__(self, message):
        self.orig_message = message

class BoardMessage(IncomingMessage):
    BOARD_SIZE = 10 # assumes 10x10 board
    
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 6 or parts[0] is not 'B':
            raise Exception('Not a board message')
        self.player = parts[1]
        self.status = parts[2]
        self._board_str = parts[3]
        self.score = parts[4]
        self.skips = parts[5]

    def board(self):
        super().__init__(message)
        if len(self._board_str) is not self.BOARD_SIZE**2:
            raise Exception('Invalid board')
        count = 0
        board = [['.' for x in range(self.BOARD_SIZE)] for y in range(self.BOARD_SIZE)]
        for char in self._board_str:
            y = count / self.BOARD_SIZE
            x = count % self.BOARD_SIZE
            board[y][x] = char
        return board

class GameInfoMessage(IncomingMessage):
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) < 11 or parts[0] is not 'G':
            raise Exception('Invalid game info message')
        self.version = parts[1]
        self.title = parts[2]
        self.started = parts[3] is 'Y' or parts[3] is 'y'
        self.min_players = int(parts[4])
        self.max_players = int(parts[5])
        self.num_players = int(parts[6])
        self.goal = int(parts[7])
        self.width = int(parts[8])
        self.length = int(parts[9])
        self.num_boats = int(parts[10])
        if len(parts) < (11 + self.num_boats):
            raise Exception('Not enough boat descriptors')
        boats = []
        for boat in range(self.num_boats):
            boats.append(parts[11 + boat])

class TurnMessage(IncomingMessage):
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 2 or parts[0] is not 'N':
            raise Exception('Invalid turn message')
        self.player = parts[1]

class FinishedMessage(IncomingMessage):
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 3 or parts[0] is not 'F':
            raise Exception('Invalid finished message')
        self.state = parts[1]
        self.turns = parts[2]
        self.players = parts[3]

class ScoreMessage(IncomingMessage):
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 6 or parts[0] is not 'R':
            raise Exception('Invalid score message')
        self.player = parts[1]
        self.score = parts[2]
        self.skips = parts[3]
        self.turns = parts[4]
        self.status = parts[5]

