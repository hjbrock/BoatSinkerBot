class Game(object):
    def __init__(self, player_name):
        self.boards = {}
        self.current_player = player_name
        self.scores = {}

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

