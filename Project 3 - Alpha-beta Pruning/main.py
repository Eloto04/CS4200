import time

board = [[0 for _ in range(8)] for _ in range(8)]
move_sequence = []

def main():
    # Prints an empty board as a starting point
    print_board()

    # This while-loop breaks once user has decided whether they want to go first
    while True:
        go_first = input("Would you like to go first? (Y/N) ").replace(" ", "").upper()
        if go_first == "Y": 
            user_first = True
            print()
            get_move()
            break
        elif go_first == "N": 
            user_first = False
            print()
            break
        else: 
            print("Invalid input.")

    # This while-loop keeps the game running, program exit is handled in check_game_over()
    while True:
        # user_first bool determines how the menu is printed at the end
        # PC moves printed on the left if PC went first, user moves on the left if user went first
        check_game_over(user_first)
        make_move()
        check_game_over(user_first)
        get_move()

def print_board() -> None:
    print("\n  1 2 3 4 5 6 7 8") # Column numbers for reference
    for i in range(8):
        print(chr(i + ord('A')), end=" ") # Row letters for reference
        for j in range(8):
            if board[i][j] == 0:
                print("-", end=" ") # Blank tile
            elif board[i][j] == 1:
                print("X", end=" ") # PC (X)
            elif board[i][j] == 2:
                print("O", end=" ") # User (O)
        print() # Newline after each row
    print()

def get_move() -> None:
    while True:
        move = input("Enter a move: ").replace(" ", "")

        # Formatting check, terminal prompts for move again if format is incorrect
        if (len(move) != 2):
            print("Invalid input format. Must be one row letter followed by one column number.")
            continue
        elif not ('a' <= move[0].lower() <= 'h'):
            print("Row must be a letter between A-H.")
            continue
        elif not ('1' <= move[1] <= '8'):
            print("Column must be a number between 1-8.")
            continue

        r = ord(move[0].lower()) - ord('a')
        c = int(move[1]) - 1
        
        # Populate tile if input format is correct and chosen tile is empty
        if board[r][c] == 0:
            board[r][c] = 2
            move_sequence.append(f"{move[0].upper()}{move[1]}")
            print(f"You play {move[0].upper()}{move[1]}.")
            break
        else:
            print("This space is occupied.\n")
    
    print_board() # Print board again once user makes their move

def evaluate() -> int:
    # This function will check 4 tiles at a time in a given row/column
    # Important features to check for: 
        # Number of open spaces
        # X/O count
    
    # Updated as board configuration is evaluated
    score = 0

    # Check each column
    for c in range(8):
        column = [row[c] for row in board]
        
        for i in range(5):
            window = column[i:i+4]
            x_count = window.count(1)
            o_count = window.count(2)
            empty_count = window.count(0)

            if x_count == 3 and empty_count == 1:
                score += 4000
                if window == [0, 1, 1, 1] or window == [1, 1, 1, 0]:
                    score += 1000
            elif x_count == 2 and empty_count == 2:
                score += 1000
            elif x_count == 1 and empty_count == 3:
                score += 100

            if o_count == 3 and empty_count == 1:
                score -= 15000 # Highest priority to block potential wins from the user
            elif o_count == 2 and empty_count == 2:
                score -= 3000
            elif o_count == 1 and empty_count == 3:
                score -= 200

    # Check each row
    for r in range(8):
        for i in range(5):
            window = board[r][i:i+4]
            x_count = window.count(1)
            o_count = window.count(2)
            empty_count = window.count(0)

            if x_count == 3 and empty_count == 1:
                score += 4000
                if window == [0, 1, 1, 1] or window == [1, 1, 1, 0]:
                    score += 1000
            elif x_count == 2 and empty_count == 2:
                score += 1000
            elif x_count == 1 and empty_count == 3:
                score += 100

            if o_count == 3 and empty_count == 1:
                score -= 15000 # Highest priority to block potential wins from the user
            elif o_count == 2 and empty_count == 2:
                score -= 3000
            elif o_count == 1 and empty_count == 3:
                score -= 200

    return score

def make_move() -> None:
    # Depth limit
    depth = 6

    # Time tracker to make sure search stops after 5 seconds
    start_time = time.time()
    
    print("PC is thinking...")

    best = float('-inf')
    best_r, best_c = None, None

    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:
                board[r][c] = 1
                score = min_value(depth - 1, float('-inf'), float('inf'), start_time)
                board[r][c] = 0

                if score > best:
                    # Function tracks move with the highest score
                    best = score
                    best_r, best_c = r, c

    if best_r is not None and best_c is not None:
        board[best_r][best_c] = 1

    print(f"PC plays {chr(best_r + ord('A'))}{best_c+1}.")
    move_sequence.append(f"{chr(best_r + ord('A'))}{best_c+1}")
    print_board()


def min_value(depth: int, alpha: int, beta: int, start_time):
    # Terminal test
    # Slightly modified from the "tictactoe.doc" code so check_for_win() is not ran twice
    win_check = check_for_win()
    if win_check != 0: return win_check
    
    # Cutoff test: if 5 seconds have passed or depth limit is reached, no more searching.
    if depth == 0 or time.time() - start_time >= 5:
        return evaluate()
    
    # Best score stored for minimizing player (user if they play optimally)
    v = float('inf')

    # Evaluate possible moves, updating alpha and beta
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:
                board[r][c] = 2
                v = min(v, max_value(depth-1, alpha, beta, start_time))
                board[r][c] = 0
                if v <= alpha:
                    return v
                beta = min(beta, v)
                
    return v

def max_value(depth: int, alpha: int, beta: int, start_time) -> int:
    # Terminal test
    # Slightly modified from the "tictactoe.doc" code so check_for_win() is not ran twice
    win_check = check_for_win()
    if win_check != 0: return win_check
    
    # Cutoff test: if 5 seconds have passed or depth limit is reached, no more searching.
    if depth == 0 or time.time() - start_time >= 5:
        return evaluate()
    
    # Best score stored for maximizing player (PC)
    v = float('-inf')

    # Evaluate possible moves, updating alpha and beta
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:
                board[r][c] = 1
                v = max(v, min_value(depth-1, alpha, beta, start_time))
                board[r][c] = 0
                if v >= beta:
                    return v
                alpha = max(alpha, v)
                
    return v

def check_for_win() -> int:
    # Bool to check if there is a move that can be played if no win is found
    empty_square = False
    
    # Check each row for a win
    for r in board:
        for i in range(5):
            val = r[i]
            if not (val == 1 or val == 2): empty_square = True; continue
            if r[i+1] == val and r[i+2] == val and r[i+3] == val:
                return 100000 if val == 1 else -100000

    # Check each column for a win
    for r in range(5):
        for c in range(8):
            val = board[r][c]
            if not (val == 1 or val == 2): empty_square = True; continue
            if board[r+1][c] == val and board[r+2][c] == val and board[r+3][c] == val:
                return 100000 if val == 1 else -100000
    
    # If there is no empty square left, we've reached a draw (1)
    # Otherwise, keep playing (0)
    return 0 if empty_square else 1

def check_game_over(user_first: bool) -> None:
    # Slightly modified from "tictactoe.doc" so check_for_win() is only ran once here
    result = check_for_win()
    if result == 100000:
        print_game_sequence(move_sequence, user_first)
        print("\nPC wins.")
        exit()
    elif result == -100000:
        print_game_sequence(move_sequence, user_first)
        print("\nYou win.")
        exit()
    elif result == 1:
        print_game_sequence(move_sequence, user_first)
        print("\nDraw.")
        exit()

def print_game_sequence(moves: list[str], user_first: bool) -> None:
    print("You (1st) vs. PC (2nd)") if user_first else print("PC (1st) vs. You (2nd)")
    
    for i in range(0, len(moves), 2): 
        if i//2+1 < 10: 
            print(f"      {i//2+1}. {moves[i]} {moves[i+1] if i+1 < len(moves) else ''}")
        else:
            print(f"     {i//2+1}. {moves[i]} {moves[i+1] if i+1 < len(moves) else ''}")

main()