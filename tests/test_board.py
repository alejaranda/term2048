from board import (
    add_random_tiles,
    can_move,
    create_board,
    has_won,
    is_game_over,
    move_down,
    move_right,
    move_up,
)


def test_add_random_tiles_return_false():
    board = create_board(size=2)
    board[0][0] = 2
    board[0][1] = 4
    board[1][0] = 8
    board[1][1] = 16

    result = add_random_tiles(board)

    assert result is False, "should return false because the board is complete"


def test_move_right_merges_and_moves_tiles():
    board = [
        [2, 0, 2, 2],
        [0, 4, 0, 4],
        [2, 2, 2, 2],
        [0, 0, 0, 0],
    ]

    moved, has_moved = move_right(board)

    assert moved == [
        [0, 0, 2, 4],
        [0, 0, 0, 8],
        [0, 0, 4, 4],
        [0, 0, 0, 0],
    ]
    assert has_moved is True


def test_move_up_merges_tiles_by_column():
    board = [
        [2, 0, 2, 0],
        [2, 2, 0, 0],
        [0, 2, 2, 0],
        [0, 0, 2, 0],
    ]

    moved, has_moved = move_up(board)

    assert moved == [
        [4, 4, 4, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert has_moved is True


def test_move_down_without_change_returns_false():
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [2, 4, 8, 16],
        [4, 8, 16, 32],
    ]

    moved, has_moved = move_down(board)

    assert moved == board
    assert has_moved is False


def test_has_won_returns_true_when_target_is_reached():
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2048, 0],
        [0, 0, 0, 0],
    ]

    assert has_won(board) is True


def test_can_move_returns_true_when_zero_exists():
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 32, 0],
    ]

    assert can_move(board) is True


def test_can_move_returns_true_when_adjacent_merge_exists():
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 16, 32],
    ]

    assert can_move(board) is True


def test_is_game_over_returns_true_when_no_moves_available():
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 32, 64],
    ]

    assert is_game_over(board) is True
