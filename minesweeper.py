import re

from board import Board

def play(dim_siz = 10, num_bombs = 10):

    board = Board(dim_siz, num_bombs)


    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input(f'Where would you like to dig? Input as row, col maximum({board.dim_size-1}, {board.dim_size-1}): '))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print('INVALID location, try again')
            continue
        
        # it it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhh
            break
    
    if safe:
        print('CONGRATULATIONS1!! you are VICTORIOUS!')
    else:
        print('SORRY GAME OVER :(')
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)



if __name__ == "__main__":
    play()

