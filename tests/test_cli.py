import curses

from cli import key_to_direction


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
