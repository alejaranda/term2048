import pytest

from game import GameConfig, GameState, apply_move, create_game, undo


def test_apply_move_raises_for_invalid_direction():
    state = GameState(
        board=[[2, 2], [0, 0]],
        score=0,
        won=False,
        game_over=False,
        history=[],
    )
    config = GameConfig(size=2)

    with pytest.raises(ValueError):
        apply_move(state, "diagonal", config)


def test_apply_move_updates_score_and_history():
    state = GameState(
        board=[[2, 2], [0, 0]],
        score=0,
        won=False,
        game_over=False,
        history=[],
    )
    config = GameConfig(size=2, target=8, random_tiles_per_move=0)

    moved = apply_move(state, "left", config)

    assert moved is True
    assert state.board == [[4, 0], [0, 0]]
    assert state.score == 4
    assert len(state.history) == 1


def test_undo_recovers_previous_state():
    state = GameState(
        board=[[2, 2], [0, 0]],
        score=0,
        won=False,
        game_over=False,
        history=[],
    )
    config = GameConfig(size=2, target=8, random_tiles_per_move=0)
    apply_move(state, "left", config)

    restored = undo(state)

    assert restored is True
    assert state.board == [[2, 2], [0, 0]]
    assert state.score == 0
    assert state.history == []


def test_create_game_adds_initial_tiles():
    config = GameConfig(size=4, initial_tiles=2)
    state = create_game(config)

    non_zero_count = sum(1 for row in state.board for value in row if value != 0)
    assert non_zero_count == 2
