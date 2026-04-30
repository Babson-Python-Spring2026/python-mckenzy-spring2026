import os
import platform

def clear_screen():
    # Windows
    if platform.system() == "Windows":
        os.system("cls")
    else:
        # Mac/Linux
        os.system("clear")

def get_valid_integer(prompt, min_val, max_val):
    while True:
        user_input = input(prompt)
        
        # Check type
        if not user_input.isdigit():
            print("You must enter an integer (2 - 10)")
            continue
        
        value = int(user_input)
        
        # Check bounds
        if value < min_val or value > max_val:
            print(f"Please enter {prompt.strip()} ({min_val} - {max_val}) : ")
            continue
        
        return value
    

def get_valid_mines(height, width):
    max_mines = height * width
    
    while True:
        mines = input(f"How many mines (less then {max_mines}) : ")
        
        if not mines.isdigit():
            print("You must enter an integer")
            continue
        
        mines = int(mines)
        
        if mines <= 0 or mines >= max_mines:
            print("Invalid number of mines, please re-enter : ")
            continue
        
        return mines

def create_board(height, width):
    board = []
    
    for r in range(height):
        row = []
        for c in range(width):
            row.append([False, 0, False])  # [is_bomb, count, revealed]
        board.append(row)
    
    return board

import random

def place_mines(board, height, width, mines):
    positions = set()
    
    while len(positions) < mines:
        r = random.randint(0, height - 1)
        c = random.randint(0, width - 1)
        positions.add((r, c))
    
    for (r, c) in positions:
        board[r][c][0] = True  # is_bomb = True

def calculate_counts(board, height, width):
    directions = [-1, 0, 1]
    
    for r in range(height):
        for c in range(width):
            
            if board[r][c][0]:  # skip bombs
                continue
            
            count = 0
            
            for dr in directions:
                for dc in directions:
                    nr = r + dr
                    nc = c + dc
                    
                    if 0 <= nr < height and 0 <= nc < width:
                        if board[nr][nc][0]:
                            count += 1
            
            board[r][c][1] = count


def build_divider(width):
    return "    " + ("----+" * width)

def format_cell(val):
    val = str(val)

    # Emoji fix (treat as width 2)
    if val == "💣":
        return f"{val:^2} "   # I figured out this part on my own, The bombs take about 2 spaces when generated
                            # so I make 2 cells generated when a bomb is in a cell to reach my 4
                            # space constant per cell regardless of what item is inside the cell
    
    return f"{val:^4}"


def print_board(board, height, width, reveal_all=False):

    

    # =========================
    # HEADER
    # =========================
    print("      ", end="")
    for c in range(width):
        print(f"{c}    ", end="")
    print()

    # =========================
# DIVIDER (FIXED ALIGNMENT)
# =========================
    divider = build_divider(width)
    print(divider)

    # =========================
    # BOARD
    # =========================
    for r in range(height):
        print(f"  {r} |", end="")

        for c in range(width):
            is_bomb, count, revealed = board[r][c]

            # =========================
            # VALUE LOGIC
            # =========================
            if reveal_all:
                if is_bomb:
                    val = "💣"
                elif count == 0:
                    val = " "
                else:
                    val = str(count)
            else:
                if not revealed:
                    val = "♦"
                else:
                    if is_bomb:
                        val = "💣"
                    elif count == 0:
                        val = " "
                    else:
                        val = str(count)

            # =========================
            # PRINT CELL
            # =========================
            print(format_cell(val) + "|", end="")

        print()

        # repeat divider after each row
        print(divider)

def flood_fill(board, height, width, r, c):
    stack = [(r, c)]
    
    while stack:
        cr, cc = stack.pop()
        
        if not (0 <= cr < height and 0 <= cc < width):
            continue
        
        if board[cr][cc][2]:  # already revealed
            continue
        
        board[cr][cc][2] = True
        
        is_bomb, count, _ = board[cr][cc]
        
        if count == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 or dc != 0:
                        stack.append((cr + dr, cc + dc))

def check_win(board, height, width):
    for r in range(height):
        for c in range(width):
            is_bomb, _, revealed = board[r][c]
            
            if not is_bomb and not revealed:
                return False
    
    return True

def get_valid_coordinate(prompt, max_val):
    while True:
        val = input(prompt)
        
        if not val.isdigit():
            print("You must enter an integer")
            continue
        
        val = int(val)
        
        if val < 0 or val > max_val:
            print(f"please enter an integer between 0 and {max_val} : ")
            continue
        
        return val
    
def play_game():
    
    # Setup
    height = get_valid_integer("Board height (2 - 10) : ", 2, 10)
    width = get_valid_integer("Board width (2 - 10) : ", 2, 10)
    mines = get_valid_mines(height, width)
    
    board = create_board(height, width)
    place_mines(board, height, width, mines)
    calculate_counts(board, height, width)
    clear_screen()
    
    # Game loop
    while True:
        clear_screen()
        print_board(board, height, width)
        
        while True:
            col = get_valid_coordinate("How many over would you like to dig? : ", width - 1)
            row = get_valid_coordinate("How many down would you like to dig? : ", height - 1)

            if board[row][col][2]:
                clear_screen()
                print_board(board, height, width)
                print("That cell is already revealed. Choose a different one.\n")
            else:
                break

        clear_screen()
        
        is_bomb, count, _ = board[row][col]
        
        # Lose condition
        if is_bomb:
            clear_screen()
            print_board(board, height, width, reveal_all=True)
            print("Game Over!")
            break
        
        # Reveal
        if count == 0:
            flood_fill(board, height, width, row, col)
        else:
            board[row][col][2] = True
        
        # Win check
        if check_win(board, height, width):
            print_board(board, height, width, reveal_all=True)
            print("Congratulations! You won.")
            break

play_game()

    
