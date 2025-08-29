from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class GameController(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.board = [0] * 9
        self.current_player = 1

    def possible_moves(self):
        return [i+1 for i,v in enumerate(self.board) if v==0]

    def make_move(self, move):
        self.board[int(move)-1] = self.current_player  # Player 1 đánh O (1), Player 2 đánh X (2)

    def unmake_move(self, move):
        self.board[int(move)-1] = 0

    def loss_condition(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(self.board[i]==1 for i in combo) or all(self.board[i]==2 for i in combo) for combo in combos)

    def is_over(self):
        return len(self.possible_moves())==0 or self.loss_condition()

    def show(self):
        symbols = ['.', 'O', 'X']
        print('\n'+'\n'.join(
            [' '.join([symbols[self.board[3*j+i]] for i in range(3)]) for j in range(3)]
        ))

    def scoring(self):
        if self.loss_condition():
            return -100
        else:
            return 0

if __name__=="__main__":
    algorithm = Negamax(7)
    GameController([Human_Player(), AI_Player(algorithm)]).play()
