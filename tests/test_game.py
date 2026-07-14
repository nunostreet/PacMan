from contracts import GameConfig, GameStatus, Direction
from engine.game import PacmanGame


def make_game(**kwargs) -> PacmanGame:
    config = GameConfig(
        levels=[(15, 11)],
        lives=3,
        pacgum=5,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        ghost_respawn_time=5.0,
        ghost_flee_time=7.0,
        level_max_time=90,
        seed=42,
    )
    for key, val in kwargs.items():
        setattr(config, key, val)
    return PacmanGame(config)


# ── scoring ───────────────────────────────────────────────────────────────────

def test_initial_score_is_zero() -> None:
    game = make_game()
    snap = game.tick(None, 0.0)
    assert snap.score == 0


def test_eating_ghost_adds_points() -> None:
    game = make_game()
    ghost = game._ghosts[0]
    ghost.edible = True
    ghost.flee_timer = 5.0
    px, py = game._pacman.x, game._pacman.y
    ghost.x, ghost.y = px, py

    # tick enough for mid_cell to fire
    game._pacman_timer = game._pacman_interval * 0.6
    snap = game.tick(None, 0.0)
    assert snap.score == 200


def test_time_runs_out_causes_game_over() -> None:
    game = make_game(level_max_time=1)
    game._time_remaining = 0.1
    snap = game.tick(None, 0.2)
    assert snap.status == GameStatus.GAME_OVER


# ── lives and respawn ─────────────────────────────────────────────────────────

def test_losing_life_decrements_lives() -> None:
    game = make_game()
    ghost = game._ghosts[0]
    ghost.edible = False
    px, py = game._pacman.x, game._pacman.y
    ghost.x, ghost.y = px, py

    game._pacman_timer = game._pacman_interval * 0.6
    snap = game.tick(None, 0.0)
    assert snap.lives == 2


def test_losing_last_life_is_game_over() -> None:
    game = make_game(lives=1)
    ghost = game._ghosts[0]
    ghost.edible = False
    px, py = game._pacman.x, game._pacman.y
    ghost.x, ghost.y = px, py

    game._pacman_timer = game._pacman_interval * 0.6
    snap = game.tick(None, 0.0)
    assert snap.status == GameStatus.GAME_OVER


def test_respawn_invincibility_prevents_double_kill() -> None:
    game = make_game()
    game._respawn_timer = 1.0

    ghost = game._ghosts[0]
    ghost.edible = False
    px, py = game._pacman.x, game._pacman.y
    ghost.x, ghost.y = px, py

    before = game._pacman.lives
    game._pacman_timer = game._pacman_interval * 0.6
    game.tick(None, 0.0)
    assert game._pacman.lives == before


def test_add_lives_caps_at_seven() -> None:
    game = make_game(lives=6)
    game.add_lives(5)
    snap = game.tick(None, 0.0)
    assert snap.lives == 7


# ── cheat mode ────────────────────────────────────────────────────────────────

def test_frozen_ghosts_do_not_move() -> None:
    game = make_game()
    game.set_frozen_ghosts(True)
    positions_before = [(g.x, g.y) for g in game._ghosts]
    for _ in range(20):
        game.tick(None, 0.1)
    positions_after = [(g.x, g.y) for g in game._ghosts]
    assert positions_before == positions_after


def test_invincible_pacman_survives_ghost() -> None:
    game = make_game()
    game.set_invincible(True)
    ghost = game._ghosts[0]
    ghost.edible = False
    px, py = game._pacman.x, game._pacman.y
    ghost.x, ghost.y = px, py

    before = game._pacman.lives
    game._pacman_timer = game._pacman_interval * 0.6
    game.tick(None, 0.0)
    assert game._pacman.lives == before


def test_cheat_flag_is_set() -> None:
    game = make_game()
    assert not game.tick(None, 0.0).cheat_used
    game.set_frozen_ghosts(True)
    assert game.tick(None, 0.0).cheat_used


# ── level progression ─────────────────────────────────────────────────────────

def test_win_condition_on_last_level() -> None:
    game = make_game(levels=[(15, 11)])
    for row in game._maze.pacgums:
        row[:] = [0] * len(row)
    # leave one to clear in the tick
    game._maze.pacgums[0][0] = 0

    snap = game.tick(None, 0.0)
    assert snap.status == GameStatus.WIN


def test_skip_level_on_last_triggers_win() -> None:
    game = make_game(levels=[(15, 11)])
    game.skip_level()
    snap = game.tick(None, 0.0)
    assert snap.status == GameStatus.WIN


def test_go_back_level_does_nothing_at_level_1() -> None:
    game = make_game()
    game.go_back_level()
    snap = game.tick(None, 0.0)
    assert snap.level == 1
