import time
from player import HumanPlayer, RandomComputerPlayer,GeniusComputerPlayer

# The Player classes (HumanPlayer and RandomComputerPlayer) are assumed to be in a separate file named player.py
# For completeness, here is a basic implementation of those classes:
# ------------------ Start player.py content (for testing locally) ------------------
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

# ------------------ End player.py content ------------------


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # we'll use a single list to represent 3x3 board
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            # Fix 1: Changed assignment operator from '==' to '='
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        col_ind = square % 3
        # Fix 2: Corrected column slice indexing
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left to right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        # If none of the above returned True, then there is no winner yet
        return False

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    # Fix 3: Added variable for alternating letters.
    letter = 'X'  # starting letter

    # Iterate while the game has empty squares
    while game.empty_squares():
        # Get move from appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # Lets define a function to make a move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' Wins!')
                return letter  # end the game and return the winner

            # After we make the move we need to alternate letters
            # Fix 4: Corrected the letter alternation logic
            letter = 'O' if letter == 'X' else 'X'

        # tiny pause
        time.sleep(0.8)

    # This part of the code is only reached if the while loop finishes without a winner (a tie)
    if print_game:
        print('It\'s a tie!')

if __name__ == '__main__':
    # Fix 5: Ensure the computer player is instantiated with 'O' not '0'
    x_player = HumanPlayer('X')
    o_player = GeniusComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)