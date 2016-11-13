# Message definitions for boat clients

class IncomingMessage(object):
    def __init__(self, message):
        self.orig_message = message

class BoardMessage(IncomingMessage):
    def __init__(self, message, width, length):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 6 or parts[0] is not 'B':
            raise Exception('Not a board message')
        self.player = parts[1]
        self.status = parts[2]
        self.score = int(parts[4])
        self.skips = int(parts[5])
        self.width = width
        self.length = length
        self.board = self._read_board(parts[3])

    def _read_board(self, board_str):
        if len(board_str) is not self.width*self.length:
            raise Exception('Invalid board')
        count = 0
        board = [['.' for x in range(self.width)] for y in range(self.length)]
        for y in range(0, self.length):
            for x in range(0, self.width):
                board[y][x] = board_str[0]
                board_str = board_str[1:]
        return board

    def print_board(self):
        str_board = ''
        for y in range(0, self.length):
            for x in range(0, self.width):
                str_board = str_board + self.board[y][x] + ' '
            str_board = str_board + '\n'

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
        if len(parts) is not 4 or parts[0] is not 'F':
            raise Exception('Invalid finished message')
        self.state = parts[1]
        self.turns = int(parts[2])
        self.players = int(parts[3])

class ScoreMessage(IncomingMessage):
    def __init__(self, message):
        super().__init__(message)
        parts = message.split("|")
        if len(parts) is not 6 or parts[0] is not 'R':
            raise Exception('Invalid score message')
        self.player = parts[1]
        self.score = int(parts[2])
        self.skips = int(parts[3])
        self.turns = int(parts[4])
        self.status = parts[5]

