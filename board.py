import random


class Board:
    def __init__(self, dim_size, nums_bomb):
        self.dim_size = dim_size
        self.nums_bomb = nums_bomb

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0

        while bombs_planted < self.nums_bomb:
            loc = random.randint(0, self.dim_size**2 - 1)
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
        # top left = (row-1, col - 1)
        # top middle = (row-1, col)
        # top right = (row-1, col+1)
        # left = (row, col-1)
        # right = (row, col+1)
        # bottom left = (row+1, col-1)
        # bottom middle = (row+1, col)
        # bottom right = (row+1, col+1)

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

    def __str__(self) -> str:
        visible_board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]
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
