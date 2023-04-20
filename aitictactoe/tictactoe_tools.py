import random

_MODES = {'user', 'easy', 'medium', 'hard'}

_DIFFICULTIES = {'easy', 'medium', 'hard'}

_MARKS = {'X', 'O'}

_MOVES = {'1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'}


def menu():
    while True:
        command: str = input("Input command: ")

        if not is_command_correct(command):
            continue
        else:
            command_interpreter(command)


def is_command_correct(command: str) -> bool:
    command_array = command.split()
    if command and command_array[0] == 'exit':
        return True
    if command and len(command_array) == 3 and command_array[0] == 'start' and command_array[1] in _MODES \
            and command_array[2] in _MODES:
        return True
    else:
        print('Bad parameters!')
        return False


def command_interpreter(command):
    command_array = command.split()

    if command_array[0] == 'exit':
        exit()
    elif command_array[0] == 'start':
        setup = {'X': command_array[1], 'O': command_array[2]}
        play(setup)


def play(setup: dict):
    game_on = True

    game_board = initialize_game()
    display_board(game_board)

    while game_on:
        player_or_ai_move(game_board, setup, 'X')
        display_board(game_board)
        game_on = is_game_on(game_board)

        if not game_on:
            break

        player_or_ai_move(game_board, setup, 'O')
        display_board(game_board)
        game_on = is_game_on(game_board)


def initialize_game() -> [[str]]:
    return [['', '', ''], ['', '', ''], ['', '', '']]


def display_board(game_board: [[str]]):
    border: str = "---------"

    line_template = "|       |"
    line1: str = fill_display_template(line_template, game_board[0])
    line2: str = fill_display_template(line_template, game_board[1])
    line3: str = fill_display_template(line_template, game_board[2])

    print(border)
    print(line1)
    print(line2)
    print(line3)
    print(border)


def fill_display_template(template: str, line: [str]) -> str:
    filled_template = template

    for i, row in enumerate(line):
        if row in ('X', 'O'):
            if i == 0:
                filled_template = filled_template[0:2] + row + filled_template[3:]
            elif i == 1:
                filled_template = filled_template[0:4] + row + filled_template[5:]
            elif i == 2:
                filled_template = filled_template[0:6] + row + filled_template[7:]

    return filled_template


def player_or_ai_move(game_board: [[str]], setup: dict, mark: _MARKS):
    if setup[mark] == 'user':
        player_move(game_board, mark)
    elif setup[mark] in _DIFFICULTIES:
        ai_move(game_board, mark, setup[mark])


def player_move(game_board: [[str]], mark: _MARKS):
    move: str = ''
    incorrect_move = True

    while incorrect_move:
        # move = input("Please enter coordinates of the move (each between 1 and 3 and separate by space):\n")
        move = input("Enter the coordinates: ")
        move = ' '.join(move.split())
        incorrect_move = not is_correct_player_move(game_board, move)

    save_move(game_board, move, mark)


def is_correct_player_move(game_board: [[str]], move: _MOVES) -> bool:
    if len(move.split()) == 2:
        row = move.split()[0]
        col = move.split()[1]

        if not row.isnumeric() or not col.isnumeric():
            print("You should enter numbers!")
            return False

        row = int(row)
        col = int(col)

        if row < 1 or row > 3 or col < 1 or col > 3:
            print("Coordinates should be from 1 to 3!")
            return False

        if game_board[row - 1][col - 1]:
            print("This cell is occupied! Choose another one!")
            return False
    elif not move.isnumeric():
        print("You should enter numbers!")
        return False
    else:
        print("You should enter 2 numbers, each between 1 and 3 and separated by a space")
        return False

    return True


def ai_move(game_board: [[str]], mark: _MARKS, difficulty: _DIFFICULTIES):
    move: str = ''

    print(f'Making move level "{difficulty}"')

    if difficulty == 'easy':
        move = play_random(game_board)
    elif difficulty == 'medium':
        if can_win_or_block(game_board, mark, 'win'):
            move = play_to_win_or_block(game_board, mark, 'win')
        elif can_win_or_block(game_board, mark, 'block'):
            move = play_to_win_or_block(game_board, mark, 'block')
        else:
            move = play_random(game_board)
    elif difficulty == 'hard':
        if is_grid_empty(game_board):
            move = '2 2'
        else:
            new_board = board_2d_to_1d(game_board)
            result = minimax_in_1d_board(new_board, mark, mark)
            board_1d_move = result['index']
            move = transpose_index_1d_to2d_board(board_1d_move, game_board)

    save_move(game_board, move, mark)


def transpose_index_1d_to2d_board(move_1d: int, board_2d: [[str]]) -> _MOVES:
    cell_counter = 0
    cell_2d = ""
    for i, line in enumerate(board_2d):
        for j, cell in enumerate(line):
            if cell_counter == move_1d:
                line_index = i + 1
                column_index = j + 1
                cell_2d = f"{line_index} {column_index}"
                return cell_2d
            cell_counter += 1
    return cell_2d


def play_random(game_board: [[str]]) -> _MOVES:
    move: str = ''
    incorrect_move = True
    while incorrect_move:
        move = str(random.randint(1, 3)) + ' ' + str(random.randint(1, 3))
        incorrect_move = not is_correct_ai_move(game_board, move)
    return move


def can_win_or_block(game_board: [[str]], mark: _MARKS, win_or_block: str) -> bool:
    mark = mark if win_or_block == 'win' else opposite_mark(mark)

    for i in range(0, 3):
        if (game_board[i][0] == game_board[i][1] == mark and game_board[i][2] == '') \
                or (game_board[i][0] == game_board[i][2] == mark and game_board[i][1] == '') \
                or (game_board[i][1] == game_board[i][2] == mark and game_board[i][0] == '') \
 \
                or (game_board[0][i] == game_board[1][i] == mark and game_board[2][i] == '') \
                or (game_board[0][i] == game_board[2][i] == mark and game_board[1][i] == '') \
                or (game_board[1][i] == game_board[2][i] == mark and game_board[0][i] == ''):
            return True

    cell_1_1: str = game_board[0][0]
    cell_1_3: str = game_board[0][2]
    cell_2_2: str = game_board[1][1]
    cell_3_1: str = game_board[2][0]
    cell_3_3: str = game_board[2][2]

    if (cell_1_1 == cell_2_2 == mark and cell_3_3 == '') \
            or (cell_1_1 == cell_3_3 == mark and cell_2_2 == '') \
            or (cell_2_2 == cell_3_3 == mark and cell_1_1 == '') \
 \
            or (cell_1_3 == cell_2_2 == mark and cell_3_1 == '') \
            or (cell_1_3 == cell_3_1 == mark and cell_2_2 == '') \
            or (cell_2_2 == cell_3_1 == mark and cell_1_3 == ''):
        return True

    return False


def opposite_mark(mark: _MARKS) -> _MARKS:
    return 'X' if mark == 'O' else 'O'


def play_to_win_or_block(game_board: [[str]], mark: _MARKS, win_or_block: str) -> str:
    mark = mark if win_or_block == 'win' else opposite_mark(mark)

    for i in range(0, 3):
        if game_board[i][0] == game_board[i][1] == mark and game_board[i][2] == '':
            return f'{i + 1} 3'
        elif game_board[i][0] == game_board[i][2] == mark and game_board[i][1] == '':
            return f'{i + 1} 2'
        elif game_board[i][1] == game_board[i][2] == mark and game_board[i][0] == '':
            return f'{i + 1} 1'
        elif game_board[0][i] == game_board[1][i] == mark and game_board[2][i] == '':
            return f'3 {i + 1} '
        elif game_board[0][i] == game_board[2][i] == mark and game_board[1][i] == '':
            return f'2 {i + 1} '
        elif game_board[1][i] == game_board[2][i] == mark and game_board[0][i] == '':
            return f'1 {i + 1} '

    cell_1_1: str = game_board[0][0]
    cell_1_3: str = game_board[0][2]
    cell_2_2: str = game_board[1][1]
    cell_3_1: str = game_board[2][0]
    cell_3_3: str = game_board[2][2]

    if cell_1_1 == cell_2_2 == mark and cell_3_3 == '':
        return '3 3'
    elif cell_1_1 == cell_3_3 == mark and cell_2_2 == '':
        return '2 2'
    elif cell_2_2 == cell_3_3 == mark and cell_1_1 == '':
        return '1 1'
    elif cell_1_3 == cell_2_2 == mark and cell_3_1 == '':
        return '3 1'
    elif cell_1_3 == cell_3_1 == mark and cell_2_2 == '':
        return '2 2'
    elif cell_2_2 == cell_3_1 == mark and cell_1_3 == '':
        return '1 3'

    return ''


def is_correct_ai_move(game_board: [[str]], move: _MOVES) -> bool:
    if len(move.split()) == 2:
        row = move.split()[0]
        col = move.split()[1]

        if not row.isnumeric() or not col.isnumeric():
            return False

        row = int(row)
        col = int(col)

        if row < 1 or row > 3 or col < 1 or col > 3:
            return False

        if game_board[row - 1][col - 1]:
            return False
    elif not move.isnumeric():
        return False
    else:
        return False

    return True


def save_move(game_board: [[str]], move: _MOVES, mark: _MARKS):
    game_board[int(move[0]) - 1][int(move[2]) - 1] = mark


def is_game_on(game_board: [[str]]) -> bool:
    grid_full = True

    for i in range(0, 3):
        if game_board[i][0] and game_board[i][0] == game_board[i][1] == game_board[i][2]:
            print(f"{game_board[i][0]} wins")
            return False
        elif game_board[0][i] and game_board[0][i] == game_board[1][i] == game_board[2][i]:
            print(f"{game_board[0][i]} wins")
            return False
        grid_full = grid_full and all(game_board[i])

    cell_1_1: str = game_board[0][0]
    cell_1_3: str = game_board[0][2]
    cell_2_2: str = game_board[1][1]
    cell_3_1: str = game_board[2][0]
    cell_3_3: str = game_board[2][2]

    if cell_2_2 and (cell_1_1 == cell_2_2 == cell_3_3 or cell_1_3 == cell_2_2 == cell_3_1):
        print(f"{cell_2_2} wins")
        return False

    if grid_full:
        print("Draw")
        return False
    else:
        return True


def is_grid_empty(board: [[str]]) -> bool:
    return sum([bool(cell) for line in board for cell in line]) == 0


def board_2d_to_1d(board_2d: [[str]]) -> [str]:
    cell_counter = 0
    board_1d = []
    for line in board_2d:
        for cell in line:
            if cell:
                board_1d.append(cell)
            else:
                board_1d.append(cell_counter)
            cell_counter += 1

    return board_1d


def empty_indexes_in_1d_board(board: [str]) -> [str]:
    return list(filter(lambda s: s not in _MARKS, board))


def winning_in_1d_board(board: [str], player: _MARKS) -> bool:
    return (board[0] == player and board[1] == player and board[2] == player) \
        or (board[3] == player and board[4] == player and board[5] == player) \
        or (board[6] == player and board[7] == player and board[8] == player) \
        or (board[0] == player and board[3] == player and board[6] == player) \
        or (board[1] == player and board[4] == player and board[7] == player) \
        or (board[2] == player and board[5] == player and board[8] == player) \
        or (board[0] == player and board[4] == player and board[8] == player) \
        or (board[2] == player and board[4] == player and board[6] == player)


def minimax_in_1d_board(new_board: [str], mark: _MARKS, original_mark: _MARKS) -> dict:
    available_spots = empty_indexes_in_1d_board(new_board)
    if winning_in_1d_board(new_board, mark) and mark == original_mark:
        return {'score': 10}
    elif winning_in_1d_board(new_board, mark) and not mark == original_mark:
        return {'score': -10}
    elif len(available_spots) == 0:
        return {'score': 0}

    moves = []

    for spot in available_spots:
        move = {'index': new_board[spot]}

        new_board[spot] = mark

        result = minimax_in_1d_board(new_board, opposite_mark(mark), original_mark)

        move['score'] = result['score']

        new_board[spot] = move['index']

        moves.append(move)

    best_move = None

    if mark == original_mark:
        best_score = -10000
        for move in moves:
            if move['score'] > best_score:
                best_score = move['score']
                best_move = move
    else:
        best_score = 10000
        for move in moves:
            if move['score'] < best_score:
                best_score = move['score']
                best_move = move

    return best_move
