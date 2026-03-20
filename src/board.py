from random import choices, sample
from typing import List, Tuple

Board = List[List[int]]
EmptyPositions = Tuple[int, int]


def create_board(size: int = 4) -> Board:
    """Create a square board depending on the size."""
    return [[0] * size for _ in range(size)]


def empty_position(board: Board) -> List[EmptyPositions]:
    """It goes through each row and column and
    returns the empty positions (row, col) in a tuple."""
    result: List[EmptyPositions] = []
    for idx_row, row in enumerate(board):
        for idx_col, val in enumerate(row):
            if val == 0:
                result.append((idx_row, idx_col))
    return result


def add_random_tiles(board: Board, count: int = 1) -> bool:
    """Add random tiles (2 or 4) to empty board positions."""
    empty_pos = empty_position(board)

    if len(empty_pos) < count:
        return False

    selected_positions = sample(empty_pos, count)

    for row, col in selected_positions:
        tile_value = choices([2, 4], weights=[8, 2])[0]
        board[row][col] = tile_value

    return True


def slide_row(row: List[int]) -> Tuple[List[int], bool]:
    non_zero = [num for num in row if num != 0]
    merged: List[int] = []
    i = 0

    while i < len(non_zero):
        current_tile = non_zero[i]
        has_next_tile = i + 1 < len(non_zero)
        next_tile_equals = has_next_tile and non_zero[i + 1] == current_tile

        if next_tile_equals:
            merged.append(current_tile * 2)
            i += 2
        else:
            merged.append(current_tile)
            i += 1

    result = merged + [0] * (len(row) - len(merged))
    changed = result != row

    return result, changed


def move_left(board: Board) -> Tuple[Board, bool]:
    transformed_board: Board = []
    has_any_movement = False

    for current_row in board:
        transformed_row, row_has_changed = slide_row(current_row)
        transformed_board.append(transformed_row)

        if row_has_changed:
            has_any_movement = True

    return transformed_board, has_any_movement


def _reverse_rows(board: Board) -> Board:
    return [list(reversed(row)) for row in board]


def _transpose(board: Board) -> Board:
    return [list(row) for row in zip(*board)]


def move_right(board: Board) -> Tuple[Board, bool]:
    reversed_board = _reverse_rows(board)
    moved_board, has_moved = move_left(reversed_board)
    return _reverse_rows(moved_board), has_moved


def move_up(board: Board) -> Tuple[Board, bool]:
    transposed_board = _transpose(board)
    moved_board, has_moved = move_left(transposed_board)
    return _transpose(moved_board), has_moved


def move_down(board: Board) -> Tuple[Board, bool]:
    transposed_board = _transpose(board)
    moved_board, has_moved = move_right(transposed_board)
    return _transpose(moved_board), has_moved


def has_won(board: Board, target: int = 2048) -> bool:
    return any(value >= target for row in board for value in row)


def can_move(board: Board) -> bool:
    if any(value == 0 for row in board for value in row):
        return True

    board_size = len(board)

    for row_idx in range(board_size):
        for col_idx in range(board_size):
            current = board[row_idx][col_idx]

            if col_idx + 1 < board_size and board[row_idx][col_idx + 1] == current:
                return True

            if row_idx + 1 < board_size and board[row_idx + 1][col_idx] == current:
                return True

    return False


def is_game_over(board: Board) -> bool:
    return not can_move(board)
