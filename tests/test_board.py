from board import add_random_tiles, create_board, move_down, move_right, move_up


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
