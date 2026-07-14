import pytest
from config.parser import Parser

VALID_LEVELS = [{"width": 15, "height": 11}]


def parse(overrides: dict) -> dict:
    base = {
        "lives": 3,
        "seed": 42,
        "level_max_time": 90,
        "pacgum": 10,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "ghost_respawn_time": 5.0,
        "ghost_flee_time": 7.0,
        "highscore_filename": "highscores.json",
        "levels": VALID_LEVELS,
    }
    base.update(overrides)
    return Parser().parse_keys(base)


# ── lives ──────────────────────────────────────────────────────────────────

def test_lives_valid() -> None:
    assert parse({"lives": 5})["lives"] == 5


def test_lives_zero_falls_to_default() -> None:
    assert parse({"lives": 0})["lives"] == Parser.DEFAULTS["lives"]


def test_lives_negative_falls_to_default() -> None:
    assert parse({"lives": -1})["lives"] == Parser.DEFAULTS["lives"]


def test_lives_string_falls_to_default() -> None:
    assert parse({"lives": "three"})["lives"] == Parser.DEFAULTS["lives"]


# ── ghost timers ────────────────────────────────────────────────────────────

def test_ghost_respawn_time_int_accepted() -> None:
    result = parse({"ghost_respawn_time": 5})
    assert result["ghost_respawn_time"] == 5.0
    assert isinstance(result["ghost_respawn_time"], float)


def test_ghost_flee_time_int_accepted() -> None:
    result = parse({"ghost_flee_time": 7})
    assert result["ghost_flee_time"] == 7.0
    assert isinstance(result["ghost_flee_time"], float)


def test_ghost_respawn_time_invalid_falls_to_default() -> None:
    result = parse({"ghost_respawn_time": -1})
    assert result["ghost_respawn_time"] == Parser.DEFAULTS["ghost_respawn_time"]


def test_ghost_flee_time_string_falls_to_default() -> None:
    result = parse({"ghost_flee_time": "long"})
    assert result["ghost_flee_time"] == Parser.DEFAULTS["ghost_flee_time"]


# ── highscore_filename ──────────────────────────────────────────────────────

def test_highscore_filename_valid() -> None:
    assert parse({"highscore_filename": "scores.json"})["highscore_filename"] \
        == "scores.json"


def test_highscore_filename_not_json_falls_to_default() -> None:
    result = parse({"highscore_filename": "scores.txt"})
    assert result["highscore_filename"] == \
        Parser.DEFAULTS["highscore_filename"]


def test_highscore_filename_int_falls_to_default() -> None:
    result = parse({"highscore_filename": 42})
    assert result["highscore_filename"] == \
        Parser.DEFAULTS["highscore_filename"]


# ── levels ──────────────────────────────────────────────────────────────────

def test_levels_null_falls_to_default() -> None:
    result = parse({"levels": None})
    assert result["levels"] == Parser.DEFAULTS["levels"]


def test_levels_empty_list_falls_to_default() -> None:
    result = parse({"levels": []})
    assert result["levels"] == Parser.DEFAULTS["levels"]


def test_levels_non_list_falls_to_default() -> None:
    result = parse({"levels": "big"})
    assert result["levels"] == Parser.DEFAULTS["levels"]


def test_level_invalid_width_falls_to_default() -> None:
    result = parse({"levels": [{"width": -1, "height": 11}]})
    assert result["levels"][0]["width"] == Parser.DEFAULTS["levels"][0]["width"]


def test_level_missing_key_falls_to_default() -> None:
    result = parse({"levels": [{"height": 11}]})
    assert result["levels"][0]["width"] == Parser.DEFAULTS["levels"][0]["width"]


def test_level_not_dict_replaced_with_default() -> None:
    result = parse({"levels": [None]})
    assert isinstance(result["levels"][0], dict)
    assert "width" in result["levels"][0]


# ── read_file ────────────────────────────────────────────────────────────────

def test_read_file_valid_json() -> None:
    result = Parser().read_file('{"lives": 3}')
    assert result["lives"] == 3


def test_read_file_invalid_json_raises() -> None:
    with pytest.raises(Exception, match="Invalid JSON"):
        Parser().read_file("{bad json}")


def test_read_file_json_array_raises() -> None:
    with pytest.raises(Exception, match="JSON object"):
        Parser().read_file("[1, 2, 3]")


# ── format_file ──────────────────────────────────────────────────────────────

def test_format_file_strips_comments() -> None:
    raw = '# comment\n{"lives": 3}'
    result = Parser().format_file(raw)
    assert "#" not in result
    assert '"lives"' in result


def test_format_file_keeps_non_comments() -> None:
    raw = '{"lives": 3}\n{"seed": 42}'
    assert Parser().format_file(raw) == raw


# ── open_file ────────────────────────────────────────────────────────────────

def test_open_file_not_found_raises() -> None:
    with pytest.raises(Exception, match="not found"):
        Parser().open_file("nonexistent_file.json")
