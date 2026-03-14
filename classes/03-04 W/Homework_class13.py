"""
Due Next Friday
the program counts the number of final boards that are unique
Homework: Reading Code with State / Transitions / Invariants (Tic-Tac-Toe)

This program brute-forces tic-tac-toe WITHOUT recursion.

What it actually counts:
- It explores all possible games where X starts and players alternate.
- The search STOPS as soon as someone wins (a terminal state).
- It also records full boards that end in a tie.
- It tracks UNIQUE *terminal* boards “up to symmetry” (rotations + reflections),
  meaning rotated/flipped versions are treated as the same terminal board.

YOUR TASKS:

RULE:  Do not change any executable code (no reformatting logic, no renaming variables, no moving lines). 
       Only add/replace comments and docstrings.
       
1) Define STATE for this program.
   - What variables change as the program runs?
2) Explain where TRANSITIONS happen.
   - Where does the state change? (where in the code, which functions)
3) Identify 4 INVARIANTS.
   - What properties remain true as the program runs (and what checks enforce them).
   - For instance: has_winner() is a check; the invariant is “we do not continue exploring after a win.”
4) For every function that says ''' TODO ''', replace that docstring with a real explanation
   of what the function does (1-4 sentences).
5) Add inline comments anywhere you see "# TODO" explaining what that code block is doing.
6) DO NOT USE AI. Write 5-8 sentences explaining one non-obvious part (choose one):  
   (a) symmetry logic (what makes a board unique), 
   (b) why we undo moves, 
   (c) why standard_form() produces uniqueness
7) The output from the program is two print statements:
       127872
       138 81792 46080 91 44 3

    explain what each number represents.


Submission:
- Update this file with your answers. Commit and sync

"""

# ----------------------------
# Global running totals (STATE)
# ----------------------------

unique_seen = []             # TODO: Represents the current tic-tac-toe board. A list of 9 positions containing 'X', 'O', or ' '
board = [' '] * 9            # TODO: Stores the standard form of every unique terminal board. it is used to avoid counting rotated or flipped versions of the same board.

full_boards = 0              # TODO: Counts how many games reached 9 moves without stopping earlier
x_wins_on_full_board = 0     # TODO: Counts games where X wins on the 9th move
draws_on_full_board = 0      # TODO: Counts games where the board is full and no player wins

x_wins = 0                   # TODO: Counts the number of unique terminal boards where X wins
o_wins = 0                   # TODO: Counts the number of unique terminal boards where O wins
ties = 0                     # TODO: Counts the number of unique terminal boards that end in a tie


# ----------------------------
# Board representation helpers
# ----------------------------
# This builds the baord into 1 dim
def to_grid(flat_board: list[str]) -> list[list[str]]:
    ''' TODO - This function Converts the flat board list of 9 positions into a 3x3 grid. 
This makes it easier to perform rotations and reflections when computing board symmetry. 
Each row of the grid corresponds to three consecutive positions in the flat board.'''
    grid = []
    for row in range(3):
        row_vals = []
        for col in range(3):
            row_vals.append(flat_board[row * 3 + col])
        grid.append(row_vals)
    return grid


def rotate_clockwise(grid: list[list[str]]) -> list[list[str]]:
    ''' TODO - This function rotates a 3x3 tic-tac-toe grid 90 degrees clockwise. 
This is used when generating different symmetrical versions of a board. 
The function creates a new grid with positions rearranged depending on the rotation. '''
    rotated = [[' '] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            rotated[c][2 - r] = grid[r][c]
    return rotated


def flip_vertical(grid: list[list[str]]) -> list[list[str]]:
    ''' TODO - This function flips a 3x3 grid vertically by reversing the order of the rows. 
This creates a reflected version of the board. 
It is used to generate symmetrical variants when assessing board uniqueness. '''
    return [grid[2], grid[1], grid[0]]


def standard_form(flat_board: list[str]) -> list[list[str]]:
    ''' TODO - Generates all symmetrical versions of a board using rotations and vertical flips. 
It compares these variants and returns the smallest one in alphabetical order. 
This standard representation allows different rotations or reflections of the same board to be treated as identical.'''
    grid = to_grid(flat_board)
    flipped = flip_vertical(grid)

    variants = []
    for _ in range(4):
        variants.append(grid)
        variants.append(flipped)
        grid = rotate_clockwise(grid)
        flipped = rotate_clockwise(flipped)

    return min(variants)


def record_unique_board(flat_board: list[str]) -> None:
    ''' TODO - Records a terminal board state if it has not been seen before under symmetry. 
The board is first converted to its standard form and compared against previously seen boards. 
If the board is unique, it is added to unique_seen and the appropriate win or tie counter is updated.'''
    global x_wins, o_wins, ties

    rep = standard_form(flat_board)

    # TODO: Why do we check "rep not in unique_seen" before appending?
    # This prevents counting the same board multiple times when it appears through rotations or reflections
    if rep not in unique_seen:
        unique_seen.append(rep)

        # TODO: This updates counts for unique *terminal* boards. What are the categories?
        #Terminal boards are categorized as X wins, O wins, or ties based on the result of who_won()
        winner = who_won(flat_board)
        if winner == 'X':
            x_wins += 1
        elif winner == 'O':
            o_wins += 1
        else:
            ties += 1


# ----------------------------
# Game logic
# ----------------------------

def has_winner(flat_board: list[str]) -> bool:
    ''' TODO - This function checks whether the current board contains a winning line. 
It evaluates all possible rows, columns, and diagonals to see if either player has three in a row. 
The function returns True if a winner exists and False otherwise.'''
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10
        if abs(score) == 30:
            return True

    return False


def who_won(flat_board: list[str]) -> str:
    ''' TODO - This function determines which player has won the game on the current board. 
It checks all possible winning lines and calculates a score to identify whether X or O has three in a row. 
The function returns 'X', 'O', or 'TIE' if no winner is found. '''
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10

        if score == 30:
            return 'X'
        elif score == -30:
            return 'O'

    return 'TIE'


def should_continue(flat_board: list[str], move_number: int) -> bool:
    ''' TODO - Determines whether the search should continue exploring deeper moves. 
If a winner is found on the current board, the board is recorded and the search stops for that branch. 
Otherwise, the function returns True so the program continues exploring additional moves.'''
    # TODO: What condition makes us STOP exploring deeper moves?
    # The search stops if a winner is detected on the board because the game has reached a terminal state
    if has_winner(flat_board):
        record_unique_board(flat_board)
        return False
    return True


def record_full_board(flat_board: list[str]) -> None:
    ''' TODO - Handles the case where the board is completely filled after nine moves. 
The board is recorded as a terminal state and counted as a full board. 
The function then updates counters depending on whether X won on the final move or the game ended in a draw. '''
    global full_boards, x_wins_on_full_board, draws_on_full_board

    # TODO: This is a terminal state because the board is full (9 moves).
    # When all 9 moves have been played the board is full, meaning the game must end either in a win or a draw
    record_unique_board(flat_board)
    full_boards += 1

    # TODO: On a full board, either X has won (last move) or it is a draw.
    # If a winner exists on the full board, it must be X since X makes the final move; otherwise the game is a draw
    if has_winner(flat_board):
        x_wins_on_full_board += 1
    else:
        draws_on_full_board += 1


# ----------------------------
# Brute force search (9 nested loops)
# ----------------------------

# TODO: In these loops, where are transitions taking place?
# Transitions occur when moves are placed on the board (e.g., board[x1] = 'X') and when moves are undone (e.g., board[x1] = ' ')
# TODO: Where else do transitions happen?
# Additional transitions occur when counters are updated and when new unique terminal boards are added to unique_seen

# Move 1: X
for x1 in range(9):
    board[x1] = 'X'
    if should_continue(board, 1):

        # Move 2: O
        for o1 in range(9):
            if board[o1] == ' ':
                board[o1] = 'O'
                if should_continue(board, 2):

                    # Move 3: X
                    for x2 in range(9):
                        if board[x2] == ' ':
                            board[x2] = 'X'
                            if should_continue(board, 3):

                                # Move 4: O
                                for o2 in range(9):
                                    if board[o2] == ' ':
                                        board[o2] = 'O'
                                        if should_continue(board, 4):

                                            # Move 5: X
                                            for x3 in range(9):
                                                if board[x3] == ' ':
                                                    board[x3] = 'X'
                                                    if should_continue(board, 5):

                                                        # Move 6: O
                                                        for o3 in range(9):
                                                            if board[o3] == ' ':
                                                                board[o3] = 'O'
                                                                if should_continue(board, 6):

                                                                    # Move 7: X
                                                                    for x4 in range(9):
                                                                        if board[x4] == ' ':
                                                                            board[x4] = 'X'
                                                                            if should_continue(board, 7):

                                                                                # Move 8: O
                                                                                for o4 in range(9):
                                                                                    if board[o4] == ' ':
                                                                                        board[o4] = 'O'
                                                                                        if should_continue(board, 8):

                                                                                            # Move 9: X
                                                                                            for x5 in range(9):
                                                                                                if board[x5] == ' ':
                                                                                                    board[x5] = 'X'

                                                                                                    # Full board reached (terminal)
                                                                                                    record_full_board(board)

                                                                                                    # undo move 9
                                                                                                    board[x5] = ' '

                                                                                        # undo move 8
                                                                                        board[o4] = ' '

                                                                            # undo move 7
                                                                            board[x4] = ' '

                                                                # undo move 6
                                                                board[o3] = ' '

                                                    # undo move 5
                                                    board[x3] = ' '

                                        # undo move 4
                                        board[o2] = ' '

                            # undo move 3
                            board[x2] = ' '

                # undo move 2
                board[o1] = ' '

    # undo move 1
    board[x1] = ' '


print(full_boards)
print(len(unique_seen), x_wins_on_full_board, draws_on_full_board, x_wins, o_wins, ties)


'''
The state of the borard is:

unique_seen = []             # TODO: Stores the standard form of every unique terminal board and it is used to avoid counting rotated or flipped versions of the same board.
board = [' '] * 9            # TODO: Represents the current tic-tac-toe board. A list of 9 positions containing 'X', 'O', or ' '

full_boards = 0              # TODO: Counts how many games reached 9 moves without stopping earlier
x_wins_on_full_board = 0     # TODO: Counts games where X wins on the 9th move
draws_on_full_board = 0      # TODO: Counts games where the board is full and no player wins

x_wins = 0                   # TODO: Counts the number of unique terminal boards where X wins
o_wins = 0                   # TODO: Counts the number of unique terminal boards where O wins
ties = 0                     # TODO: Counts the number of unique terminal boards that end in a tie

Transitions:
Transitions happen in the following places:

When a move is made in the nested loops:
The board state changes when a player places a mark
Example --> board[x1] = 'X' or board[o1] = 'O'

When a move is undone:
After exploring a branch of the game, the program resets the board position to ' ' so other possibilities can be tested
Example--> board[x1] = ' '

When a terminal board is recorded:
In record_unique_board(), the program may add a new board to unique_seen

When counters are updated:
In record_unique_board() and record_full_board(), the program counts variables such as x_wins, o_wins, ties, full_boards, x_wins_on_full_board, and draws_on_full_board

When the program checks whether or not to continue searching:
In should_continue(), the program may stop exploring further moves if a winner has been found, which triggers recording the board



Invariants:
1.)The board never has two marks in the same position. 
A move is only made if the position is empty (if board[o1] == ' ' etc.).
This ensures that no square is overwritten during the game.

2.)Players always alternate turns starting with X.
The nested loops guarentee the move order: X → O → X → O.
This ensures that the number of X moves is always equal to or exactly one greater than O moves.

3.)The program stops exploring a game once there is a winner.
The function should_continue() calls has_winner() and returns False if a winner exists.
This prevents the program from continuing to add moves after a win.

4.)Only unique terminal boards are counted.
record_unique_board() checks if rep not in unique_seen before adding a board.
This ensures rotated or flipped versions of the same board are not counted multiple times.



6.) 
The program sees two boards the same if one can be turned into the other using rotations or reflections.
In tic-tac-toe, the board can be rotated 3 ways: 90°, 180°, or 270°. 
It can also be flipped, producing multiple visual versions of the same position. 
Even though these boards look different in orientation, the placement of X’s and O’s relative to each other is identical. 
Due to this symmetry, counting them separately would overstate the number of unique outcomes. 
The program generates all symmetrical versions of a board and compares them so they can be treated as the same configuration. 
Only one representative version of these symmetric boards is stored in unique_seen. 
This ensures that the program counts every unique terminal board position only once, regardless of how it is rotated or flipped.

7.)
The first number, 127872, represents the total number of complete tic-tac-toe games that reach a full board of 9 moves when the program simulates every possible sequence of moves. 
These are games where all spaces are filled before the program stops.

The second line contains several values:
138 --> The total number of unique terminal boards up to symmetry, meaning rotated or reflected boards are counted only once
81792 --> The number of full boards where X wins on the final move
46080--> The number of full boards that end in a draw (no winner)
91 --> The number of unique terminal boards where X wins when symmetry is considered
44 --> The number of unique terminal boards where O wins when symmetry is considered
3 --> The number of unique terminal boards that end in a tie when symmetry is considered

These numbers summarize both the total outcomes of the brute-force search and the number of unique board configurations when symmetric boards are treated as identical















'''