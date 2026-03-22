from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from board import (
    Board,
    add_random_tiles,
    create_board,
    has_won,
    is_game_over,
    move_down_with_score,
    move_left_with_score,
    move_right_with_score,
    move_up_with_score,
)

Direction = str
_MOVES: Dict[Direction, Callable[[Board], Tuple[Board, bool, int]]] = {
    "left": move_left_with_score,
    "right": move_right_with_score,
    "up": move_up_with_score,
    "down": move_down_with_score,
}


@dataclass(frozen=True)
class GameConfig:
    size: int = 4
    target: int = 2048
    initial_tiles: int = 2
    random_tiles_per_move: int = 1


@dataclass
class GameState:
    board: Board
    score: int
    won: bool
    game_over: bool
    history: List[Tuple[Board, int, bool, bool]]


def _copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def create_game(config: GameConfig = GameConfig()) -> GameState:
    board = create_board(config.size)
    add_random_tiles(board, count=config.initial_tiles)
    return GameState(
        board=board,
        score=0,
        won=has_won(board, config.target),
        game_over=is_game_over(board),
        history=[],
    )


def apply_move(state: GameState, direction: Direction, config: GameConfig) -> bool:
    if direction not in _MOVES:
        allowed = ", ".join(sorted(_MOVES.keys()))
        raise ValueError(f"Invalid direction '{direction}'. Allowed: {allowed}")

    move_fn = _MOVES[direction]
    moved_board, moved, score_delta = move_fn(state.board)

    if not moved:
        return False

    state.history.append((state.board, state.score, state.won, state.game_over))
    state.board = moved_board
    state.score += score_delta
    if not add_random_tiles(state.board, count=config.random_tiles_per_move):
        raise RuntimeError("Failed to add random tiles after a successful move.")
    state.won = has_won(state.board, config.target)
    state.game_over = is_game_over(state.board)
    return True


def undo(state: GameState) -> bool:
    if not state.history:
        return False

    (
        previous_board,
        previous_score,
        previous_won,
        previous_game_over,
    ) = state.history.pop()
    state.board = _copy_board(previous_board)
    state.score = previous_score
    state.won = previous_won
    state.game_over = previous_game_over
    return True
