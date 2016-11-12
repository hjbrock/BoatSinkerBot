# Outgoing message definitions

class OutgoingMessage(object):
    def __init__(self):
        pass

    def to_string(self):
        raise Exception('unimplemented')

class ShootMessage(OutgoingMessage):
    def __init__(self, player, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player

    def to_string(self):
        return 'S|{0}|{1}|{2}'.format(self.player, self.x, self.y)

class JoinMessage(OutgoingMessage):
    def __init__(self, name, board):
        super().__init__()
        self.name = name
        self.board = board

    def to_string(self):
        board_str = ''
        for y in self.board:
            for x in y:
                board_str = board_str + x

        return 'J|{0}|{1}'.format(self.name, board_str)
