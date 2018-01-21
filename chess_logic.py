from functools import reduce

def empty_board():
    return [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

def fields_attacked_by_queen(queen_coords):
    fields = []
    # horizontal fields
    for i in range(8): fields.append([i, queen_coords[1]])
    # vertical fields
    for i in range(8): fields.append([queen_coords[0], i])
    # ascending diagonal
    x = max(0, queen_coords[0] - queen_coords[1])
    y = max(0, queen_coords[1] - queen_coords[0])
    while x < 8 and y < 8:
        fields.append([x, y])
        x += 1
        y += 1
    # descending diagonal
    x = max(0, queen_coords[0] - (7 - queen_coords[1]))
    y = min(7, queen_coords[0] + queen_coords[1])
    while x < 8 and y >= 0:
        fields.append([x, y])
        x += 1
        y -= 1
    return fields

def apply_attacked_fields(board, fields):
    for f in fields:
        board[f[0]][f[1]] = 1
    return board

def attacked_board(queen_coords):
    return apply_attacked_fields(empty_board(), fields_attacked_by_queen(queen_coords))

def index_to_coord(index):
    return [index // 8, index % 8]

def func_add_cord(coords, index):
    coords.append(index_to_coord(index))
    return coords

def inline_board_to_coords(fields_list):
    return reduce(lambda coords, i: func_add_cord(coords, i) if fields_list[i] == 1 else coords,
                  range(len(fields_list)), [])

def checks_count(inline_board):
    queens_coords = inline_board_to_coords(inline_board)
    checks = 0
    while len(queens_coords) > 1:
        q = queens_coords.pop()
        board = attacked_board(q)
        for q2 in queens_coords:
            if board[q2[0]][q2[1]] == 1:
                checks += 1
    return checks

def get_visualization(inline_board):
    coords = inline_board_to_coords(inline_board)
    board = []
    for row in range(8):
        board.append([])
        for i in range(8):
            board[row].append('+')
    for q in coords:
        board[q[0]][q[1]] = 'Q'
    vis = ""
    for row in board:
        for cell in row:
            vis += cell
        vis += "\n"
    return vis