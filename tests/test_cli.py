import curses
from unittest.mock import patch

from cli import key_to_direction
from cli import main


def test_key_to_direction_supports_arrow_keys():
    assert key_to_direction(curses.KEY_LEFT) == "left"
    assert key_to_direction(curses.KEY_RIGHT) == "right"
    assert key_to_direction(curses.KEY_UP) == "up"
    assert key_to_direction(curses.KEY_DOWN) == "down"


def test_key_to_direction_supports_wasd_and_unknown():
    assert key_to_direction(ord("a")) == "left"
    assert key_to_direction(ord("d")) == "right"
    assert key_to_direction(ord("w")) == "up"
    assert key_to_direction(ord("s")) == "down"
    assert key_to_direction(ord("x")) is None


def test_main_returns_zero_on_keyboard_interrupt():
    with patch("cli.sys.stdin.isatty", return_value=True), patch(
        "cli.sys.stdout.isatty", return_value=True
    ), patch("cli.run", side_effect=KeyboardInterrupt):
        assert main([]) == 0
