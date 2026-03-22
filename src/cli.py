import curses
from time import monotonic
from typing import Dict, Optional, Tuple

from game import GameConfig, apply_move, create_game, undo

_TILE_WIDTH = 7
_MIN_TERMINAL_WIDTH = 46
_MIN_TERMINAL_HEIGHT = 20
_MESSAGE_TTL_SECONDS = 1.0
_MOVE_FLASH_SECONDS = 0.12
_TILE_COLOR_RULES: Tuple[Tuple[int, str], ...] = (
    (2, "v2"),
    (4, "v4"),
    (8, "v8"),
    (16, "v16"),
    (32, "v32"),
    (64, "v64"),
    (128, "v128"),
    (256, "v256"),
    (512, "v512"),
    (1024, "v1024"),
)


def key_to_direction(key: int) -> Optional[str]:
    mapping = {
        curses.KEY_LEFT: "left",
        curses.KEY_RIGHT: "right",
        curses.KEY_UP: "up",
        curses.KEY_DOWN: "down",
        ord("a"): "left",
        ord("d"): "right",
        ord("w"): "up",
        ord("s"): "down",
    }
    return mapping.get(key)


def _init_colors() -> Dict[str, int]:
    if not curses.has_colors():
        return {}

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_YELLOW)  # 2
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_CYAN)  # 4
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # 8
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_MAGENTA)  # 16
    curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_BLUE)  # 32
    curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_RED)  # 64
    curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_MAGENTA)  # 128
    curses.init_pair(11, curses.COLOR_CYAN, curses.COLOR_RED)  # 256
    curses.init_pair(12, curses.COLOR_RED, curses.COLOR_YELLOW)  # 512
    curses.init_pair(13, curses.COLOR_BLUE, curses.COLOR_CYAN)  # 1024
    curses.init_pair(14, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)  # 2048+
    return {
        "text": 1,
        "frame": 2,
        "empty": 3,
        "v2": 4,
        "v4": 5,
        "v8": 6,
        "v16": 7,
        "v32": 8,
        "v64": 9,
        "v128": 10,
        "v256": 11,
        "v512": 12,
        "v1024": 13,
        "v2048": 14,
    }


def _tile_attr(value: int, color_map: Dict[str, int]) -> int:
    if not color_map:
        return curses.A_BOLD
    if value == 0:
        return curses.color_pair(color_map["empty"]) | curses.A_DIM

    pair_key = "v2048"
    for max_value, key in _TILE_COLOR_RULES:
        if value <= max_value:
            pair_key = key
            break
    pair_id = color_map[pair_key]

    return curses.color_pair(pair_id) | curses.A_BOLD


def _frame_attr(color_map: Dict[str, int], flash: bool) -> int:
    if not color_map:
        return curses.A_BOLD if flash else curses.A_DIM
    attr = curses.color_pair(color_map["frame"]) | curses.A_DIM
    if flash:
        attr |= curses.A_BOLD
    return attr


def _separator(cell_count: int, left: str, mid: str, right: str) -> str:
    return left + mid.join(["─" * _TILE_WIDTH] * cell_count) + right


def _draw_board(
    stdscr,
    top: int,
    left: int,
    board,
    color_map: Dict[str, int],
    flash: bool,
) -> None:
    size = len(board)
    top_line = _separator(size, "┌", "┬", "┐")
    mid_line = _separator(size, "├", "┼", "┤")
    bottom_line = _separator(size, "└", "┴", "┘")
    frame_attr = _frame_attr(color_map, flash)

    stdscr.addstr(top, left, top_line, frame_attr)

    for row_idx, row in enumerate(board):
        content_y = top + 1 + row_idx * 2
        row_template = "│" + (" " * _TILE_WIDTH + "│") * size
        stdscr.addstr(content_y, left, row_template, frame_attr)

        for col_idx, value in enumerate(row):
            cell_left = left + 1 + col_idx * (_TILE_WIDTH + 1)
            attr = _tile_attr(value, color_map)
            fill = " " * _TILE_WIDTH
            label = str(value) if value else "·"
            label_x = cell_left + (_TILE_WIDTH - len(label)) // 2
            stdscr.addstr(content_y, cell_left, fill, attr)
            stdscr.addstr(content_y, label_x, label, attr)

        if row_idx < size - 1:
            stdscr.addstr(content_y + 1, left, mid_line, frame_attr)
        else:
            stdscr.addstr(content_y + 1, left, bottom_line, frame_attr)


def _draw(
    stdscr,
    game_state,
    message: str,
    color_map: Dict[str, int],
    flash: bool,
) -> None:
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    if rows < _MIN_TERMINAL_HEIGHT or cols < _MIN_TERMINAL_WIDTH:
        stdscr.addstr(0, 0, "Resize terminal to at least 46x20 to play.")
        stdscr.refresh()
        return

    board_size = len(game_state.board)
    board_width = 1 + board_size * (_TILE_WIDTH + 1)
    board_height = 2 * board_size + 1
    board_left = max(0, (cols - board_width) // 2)
    board_top = max(4, (rows - board_height) // 2)

    title = "2048"
    info = f"SCORE {game_state.score}"
    stdscr.addstr(0, max(0, (cols - len(title)) // 2), title, curses.A_BOLD)
    stdscr.addstr(1, max(0, (cols - len(info)) // 2), info, curses.A_DIM)

    _draw_board(stdscr, board_top, board_left, game_state.board, color_map, flash)

    status_line = board_top + board_height + 1
    if game_state.won:
        stdscr.addstr(
            status_line,
            max(0, (cols - 14) // 2),
            "TARGET REACHED",
            curses.A_BOLD,
        )
        status_line += 1
    if game_state.game_over:
        stdscr.addstr(status_line, max(0, (cols - 9) // 2), "GAME OVER", curses.A_BOLD)
        status_line += 1
    if message:
        stdscr.addstr(
            status_line,
            max(0, (cols - len(message)) // 2),
            message,
            curses.A_DIM,
        )

    controls = "u undo  ·  q quit"
    stdscr.addstr(rows - 1, max(0, (cols - len(controls)) // 2), controls)

    stdscr.refresh()


def _run_loop(stdscr) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(50)
    color_map = _init_colors()

    config = GameConfig()
    state = create_game(config)
    message = ""
    message_until = 0.0
    flash_until = 0.0

    while True:
        visible_message = message if monotonic() < message_until else ""
        flash = monotonic() < flash_until
        _draw(stdscr, state, visible_message, color_map, flash)
        key = stdscr.getch()

        if key == -1:
            continue
        if key == curses.KEY_RESIZE:
            continue

        if key in (ord("q"), ord("Q")):
            return

        if key in (ord("u"), ord("U")):
            if not undo(state):
                message = "nothing to undo"
                message_until = monotonic() + _MESSAGE_TTL_SECONDS
            continue

        direction = key_to_direction(key)
        if not direction:
            continue

        moved = apply_move(state, direction, config)
        if not moved:
            message = "blocked"
            message_until = monotonic() + _MESSAGE_TTL_SECONDS
        else:
            flash_until = monotonic() + _MOVE_FLASH_SECONDS


def run() -> None:
    curses.wrapper(_run_loop)


if __name__ == "__main__":
    run()
