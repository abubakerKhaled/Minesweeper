# Minesweeper Game

Minesweeper is a classic puzzle game where players dig through a grid of cells, avoiding hidden bombs. This README file provides an overview of the game mechanics, how to play, and the implementation of the code.

## How to Play

1. The game generates a board with a specified size (`dim_size`) and a certain number of bombs (`num_bombs`).
2. Players take turns guessing the location of safe cells by specifying row and column coordinates.
3. If a player digs a bomb, the game is over.
4. If a player successfully digs all non-bomb cells, they win the game.
5. The game provides feedback for each dig, showing the current state of the board and indicating if a guessed cell is safe or not.

## Code Implementation

### Importing Necessary Modules

```python
import re
from board import Board
```

### Main Game Logic

The `play` function contains the main logic for the game. It initializes the board, processes user input, and handles game outcomes.

```python
def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input(f'Where would you like to dig? Input as row, col maximum({board.dim_size-1}, {board.dim_size-1}): '))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print('INVALID location, try again')
            continue
        
        # If it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break
    
    if safe:
        print('CONGRATULATIONS! You are VICTORIOUS!')
    else:
        print('SORRY, GAME OVER :(')
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()
```

### Board Class

The `Board` class handles the creation of the game board, placement of bombs, and the logic for digging cells.

```python
import random

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] != "*":
                board[row][col] = "*"
                bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if self.board[row][col] == "*":
                    continue
                self.board[row][col] = self.get_num_neighboring_bombs(row, col)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue  # don't check the original location
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        string_rep = ""

        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        indices = [i for i in range(self.dim_size)]
        indices_row = " "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += " ".join(cells)
        indices_row += " \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += "  |".join(cells)
            string_rep += "  |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-" * str_len + "\n" + string_rep + "-" * str_len

        return string_rep
```

### Running the Game

To start the game, simply run the `play` function with the desired board size and number of bombs:

```python
if __name__ == "__main__":
    play()
```

## How It Works

- **Creating the Board**: The `Board` class creates a new game board with the specified dimensions and randomly places bombs.
- **Assigning Values**: Each cell in the board is assigned a value based on the number of neighboring bombs.
- **Digging Cells**: The `dig` function reveals the value of the selected cell and recursively digs neighboring cells if the selected cell has no neighboring bombs.
- **Game Loop**: The main game loop in the `play` function repeatedly prompts the user for input, updates the game state, and checks for win/loss conditions.

**Enjoy playing Minesweeper!**
