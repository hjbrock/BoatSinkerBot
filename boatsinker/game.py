class Game(object):
    def __init__(self, player_name, width, length, boats):
        self.boards = {}
        self.current_player = player_name
        self.scores = {}
        self.width = width
        self.length = length
        self.boats = {}
        self.hits_per_board = 0
        self.min_boat_size = 1
        for boat in boats:
            letter = boat[:1]
            size = int(boat[1:])
            self.hits_per_board = self.hits_per_board + size
            self.boats[letter] = size
            if size < self.min_boat_size:
                self.min_boat_size = size

    def update_board(self, player_name, board):
        if player_name != self.current_player:
            self.boards[player_name] = board

    def update_score(self, player_name, score):
        self.scores[player_name] = score

    def winner(self):
        max_score = 0
        winner = []
        for player in self.scores:
            if self.scores[player] > max_score:
                winner = []
                max_score = self.scores[player]
                winner.append(player)
            elif self.scores[player] is max_score:
                winner.append(player)
        
        return winner

